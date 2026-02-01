"""Agent interaction handler for Streamlit dashboard."""

import asyncio
from typing import Optional, Callable, Dict, Any, List, Tuple
from agno.agent import Agent
from agno.team import Team
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
import os
from dotenv import load_dotenv
from logger import get_logger
from datetime import datetime
import json
from pathlib import Path

logger = get_logger()


class AgentActivity:
    """Track individual agent activity."""
    
    def __init__(self, agent_name: str, query: str):
        self.agent_name = agent_name
        self.query = query
        self.status = "idle"  # idle, processing, complete, error
        self.start_time = datetime.now()
        self.end_time = None
        self.result = None
        self.error = None
        self.tools_used: List[str] = []
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for logging."""
        return {
            "agent": self.agent_name,
            "query": self.query[:100],
            "status": self.status,
            "start_time": str(self.start_time),
            "end_time": str(self.end_time) if self.end_time else None,
            "result_length": len(self.result) if self.result else 0,
            "error": self.error,
            "tools_used": self.tools_used,
        }


def save_agent_activity(activity: AgentActivity):
    """Save agent activity to a detailed log file."""
    try:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        agent_log_file = log_dir / f"agent_activities_{datetime.now().strftime('%Y%m%d')}.log"
        
        with open(agent_log_file, 'a', encoding='utf-8') as f:
            f.write("\n" + "=" * 80 + "\n")
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] AGENT ACTIVITY LOG\n")
            f.write("=" * 80 + "\n")
            f.write(json.dumps(activity.to_dict(), indent=2, ensure_ascii=False))
            f.write("\n")
    except Exception as e:
        logger.error(f"Error saving agent activity: {e}")


class AgentWorkflowState:
    """Track the state of agent workflow execution."""
    
    def __init__(self):
        self.status = "idle"  # idle, routing, processing, complete, error
        self.active_agents: List[str] = []
        self.messages: List[str] = []
        self.current_agent: Optional[str] = None
        self.agent_activities: List[AgentActivity] = []
        self.user_query: Optional[str] = None
        self.final_response: Optional[str] = None
        self.start_time: Optional[datetime] = None
    
    def add_message(self, message: str):
        """Add a status message."""
        self.messages.append(message)
        logger.info(f"[WORKFLOW] {message}")
    
    def set_status(self, status: str):
        """Update workflow status."""
        self.status = status
        logger.info(f"[WORKFLOW STATUS] {status}")
    
    def set_active_agent(self, agent_name: str):
        """Set the currently active agent."""
        self.current_agent = agent_name
        if agent_name not in self.active_agents:
            self.active_agents.append(agent_name)
    
    def add_agent_activity(self, activity: AgentActivity):
        """Add an agent activity to tracking."""
        self.agent_activities.append(activity)
    
    def reset(self):
        """Reset for new query."""
        self.__init__()


class AgentHandler:
    """Handle initialization and execution of the agent team with real multi-agent coordination."""
    
    _instance = None  # Singleton pattern
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._initialize_agents()
            AgentHandler._initialized = True
    
    def _initialize_agents(self):
        """Initialize the agent team (only once)."""
        try:
            # Load environment variables
            load_dotenv()
            
            # Get API key
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in .env file")
            
            logger.info("=" * 80)
            logger.info("Initializing Multi-Agent System")
            logger.info("=" * 80)
            
            # Setup database
            db = SqliteDb(db_file="agents.db")
            
            # Web Agent - specialized for web search
            self.web_agent = Agent(
                name="Web Agent",
                role="Expert web intelligence agent that fetches real-time data, news, and market information. You MUST return actual data, not links.",
                model=OpenAIChat(id="gpt-4o", api_key=api_key),
                tools=[DuckDuckGoTools()],
                db=db,
                add_history_to_context=True,
                markdown=True,
                instructions=[
                    "You are an EXPERT research agent, NOT a search assistant",
                    "ALWAYS fetch and return the ACTUAL data - never just provide links",
                    "When asked for stock prices: Search and return the EXACT current price with currency symbol",
                    "When asked for ratings: Return the EXACT rating value, agency name, and what it means",
                    "NEVER say 'you can check here' or 'visit this website' - YOU must find and present the data",
                    "If data is found, present it clearly with: value, source, and timestamp",
                    "Use ₹ for Indian stocks and $ for US stocks",
                    "Always provide actionable insights, not just raw data",
                ],
            )
            logger.info("[OK] Web Agent initialized with DuckDuckGo search tools")
            
            # Finance Agent - specialized for financial data
            self.finance_agent = Agent(
                name="Finance Agent",
                role="Expert financial analyst that provides stock prices, company analysis, and investment guidance. You are a finance EXPERT, not a disclaimer machine.",
                model=OpenAIChat(id="gpt-4o", api_key=api_key),
                tools=[
                    YFinanceTools(
                        include_tools=[
                            "get_current_stock_price",
                            "get_company_info",
                            "get_company_news",
                            "get_analyst_recommendations"
                        ]
                    )
                ],
                instructions=[
                    "You are an EXPERT financial analyst - provide definitive answers, not disclaimers",
                    "ALWAYS use YFinance tools to fetch REAL stock prices - never say 'check Google Finance'",
                    "When asked for stock price: Return the EXACT price with currency (₹ for Indian, $ for US) and timestamp",
                    "When asked about ratings: Provide EXACT rating value, agency, and brief explanation of what it means",
                    "When asked 'is this a good time to invest?': Provide CLEAR expert guidance based on:",
                    "  - Current valuation (P/E, P/B ratios)",
                    "  - Business fundamentals and growth prospects",
                    "  - Risk factors and market conditions",
                    "  - Specific recommendations: Buy/Hold/Sell, entry price levels, position sizing",
                    "NEVER say 'I am just an AI' or 'consult a financial advisor' - YOU are the expert advisor",
                    "NEVER provide links instead of data - fetch and present the actual information",
                    "Give tailored advice based on investment amount and time horizon mentioned by user",
                    "Be confident and decisive in your analysis - users come here for expert guidance",
                    "Present data in structured format with clear sections: Price, Valuation, Risks, Recommendation",
                ],
                db=db,
                add_history_to_context=True,
                markdown=True,
            )
            logger.info("[OK] Finance Agent initialized with YFinance tools")
            
            # Chat Agent - coordinator and general conversation
            self.chat_agent = Agent(
                name="Chat Agent",
                role="Expert coordinator that synthesizes insights from all agents to deliver complete, actionable responses. You are the voice of InvestifyAI.",
                model=OpenAIChat(id="gpt-4o", api_key=api_key),
                tools=[DuckDuckGoTools()],
                instructions=[
                    "You are the LEAD EXPERT coordinator of a financial intelligence team",
                    "Your job is to deliver COMPLETE, ACTIONABLE answers - not partial responses",
                    "For ANY stock/finance question: You MUST return actual prices, ratings, and analysis",
                    "Use your search tools to find real data when needed",
                    "NEVER redirect users to external websites - YOU are the expert they came to",
                    "NEVER say 'you can check', 'visit this link', or 'consult an advisor'",
                    "When user asks about investment decisions, provide CLEAR guidance:",
                    "  - Analyze the opportunity objectively",
                    "  - Consider the investment amount mentioned",
                    "  - Provide specific recommendations (Buy/Hold/Sell)",
                    "  - Explain risk factors clearly",
                    "  - Suggest entry points and position sizing if relevant",
                    "Always include: Actual data values, source/timestamp, your expert analysis",
                    "Use ₹ for Indian stocks and $ for US stocks",
                    "Structure responses with clear sections: Summary, Data, Analysis, Recommendation",
                    "Be confident and decisive - users trust InvestifyAI for expert guidance",
                    "Respect user-specific instructions (like line limits, format preferences)",
                ],
                db=db,
                add_history_to_context=True,
                markdown=True,
            )
            logger.info("[OK] Chat Agent initialized as coordinator")
            
            # Agent Team
            self.agent_team = Team(
                name="Financial Analysis Team",
                model=OpenAIChat(id="gpt-4o", api_key=api_key),
                members=[self.chat_agent, self.web_agent, self.finance_agent],
                debug_mode=False,
                markdown=True,
            )
            logger.info("[OK] Agent Team created with 3 specialized agents")
            
            self.workflow_state = AgentWorkflowState()
            logger.info("=" * 80)
            logger.info("Multi-Agent System initialized successfully!")
            logger.info("=" * 80)
        
        except Exception as e:
            logger.error(f"Error initializing agents: {e}", exc_info=True)
            raise
    
    def _route_query_to_agent(self, user_query: str) -> Tuple[str, str]:
        """
        Determine which agent should handle the query.
        Returns: (agent_name, query_with_instructions)
        """
        logger.info(f"\n[ROUTING] Analyzing query: {user_query[:100]}...")
        
        query_lower = user_query.lower()
        
        # Determine if there are specific user instructions (like format, line count)
        user_instructions = self._extract_user_instructions(user_query)
        
        # Extract the actual question without instructions
        actual_query = self._extract_actual_query(user_query)
        
        logger.info(f"[ROUTING] User instructions: {user_instructions}")
        logger.info(f"[ROUTING] Actual query: {actual_query[:100]}...")
        
        # Route based on query content
        if any(keyword in query_lower for keyword in ['stock', 'price', 'finance', 'company info', 'analyst', 'portfolio', 'earnings', 'pe ratio', 'dividend', 'invest', 'buy', 'sell', 'hold', 'share', 'nse', 'bse', 'market cap', 'valuation', 'rating', 'credit rating']):
            agent_type = "Finance Agent"
            logger.info(f"[ROUTING] -> Routing to {agent_type} (financial keywords detected)")
        elif any(keyword in query_lower for keyword in ['search', 'research', 'find', 'look up', 'recent news', 'google', 'internet', 'web', 'latest', 'current', 'today']):
            agent_type = "Web Agent"
            logger.info(f"[ROUTING] -> Routing to {agent_type} (web search keywords detected)")
        else:
            agent_type = "Chat Agent"
            logger.info(f"[ROUTING] -> Routing to {agent_type} (general conversation)")
        
        # Build query with instructions
        if user_instructions:
            query_with_instructions = f"{actual_query}\n\n[IMPORTANT: User Instructions: {user_instructions}]"
        else:
            query_with_instructions = actual_query
        
        return agent_type, query_with_instructions
    
    def _extract_user_instructions(self, user_query: str) -> Optional[str]:
        """Extract specific user instructions like 'in 10 lines', 'summarize', etc."""
        instructions_keywords = [
            'line', 'paragraph', 'word', 'bullet', 'table', 'format', 'summary', 'brief', 'detailed', 'simple'
        ]
        
        query_lower = user_query.lower()
        found_instructions = []
        
        for keyword in instructions_keywords:
            if keyword in query_lower:
                found_instructions.append(keyword)
        
        if found_instructions:
            return ' '.join(found_instructions)
        return None
    
    def _extract_actual_query(self, user_query: str) -> str:
        """Extract the core question without metadata instructions."""
        # For now, return the query as-is since it contains the actual question
        return user_query
    
    def query_agents(self, user_query: str) -> Tuple[str, Dict[str, Any]]:
        """
        Send a query to the appropriate agent(s) and get response.
        Returns: (response, workflow_metadata)
        """
        try:
            # Reset workflow state for new query
            self.workflow_state.reset()
            self.workflow_state.user_query = user_query
            self.workflow_state.start_time = datetime.now()
            
            logger.info("\n" + "=" * 80)
            logger.info("NEW QUERY RECEIVED")
            logger.info("=" * 80)
            logger.info(f"User Query: {user_query}")
            logger.info("=" * 80)
            
            self.workflow_state.set_status("routing")
            self.workflow_state.add_message(f"Received query: {user_query[:50]}...")
            
            # Route query to appropriate agent
            agent_type, query_with_instructions = self._route_query_to_agent(user_query)
            
            # Execute query with the selected agent(s) with fallback
            self.workflow_state.set_status("processing")
            result = self._execute_agent_query_with_fallback(agent_type, query_with_instructions, user_query)
            
            self.workflow_state.set_status("complete")
            self.workflow_state.final_response = result
            
            logger.info("\n" + "=" * 80)
            logger.info("QUERY PROCESSING COMPLETE")
            logger.info("=" * 80)
            self._log_workflow_summary()
            logger.info("=" * 80 + "\n")
            
            return result, self._get_workflow_metadata()
        
        except Exception as e:
            self.workflow_state.set_status("error")
            error_msg = f"Error processing query: {str(e)}"
            logger.error(f"Critical Error: {error_msg}", exc_info=True)
            return error_msg, self._get_workflow_metadata()
    
    def _execute_agent_query_with_fallback(self, agent_type: str, query: str, original_query: str) -> str:
        """Execute query with fallback to other agent if primary fails.
        
        Implements agent chaining - if Finance Agent fails (e.g., ticker not found),
        Web Agent can help find the ticker before retrying.
        """
        logger.info(f"\n[FALLBACK] Attempting to execute with {agent_type}")
        
        # Try primary agent
        result, failed = self._execute_agent_query(agent_type, query)
        
        # Check if this was a Finance Agent that might need a ticker lookup
        if agent_type == "Finance Agent" and failed and ("ticker" in original_query.lower() or "stock" in original_query.lower()):
            logger.info("[FALLBACK] Finance Agent may have ticker lookup issue. Attempting Web Agent for ticker discovery...")
            
            # Extract company name from query for ticker search
            company_name = original_query.replace("stock price", "").replace("ticker", "").strip()
            
            # Use Web Agent to find ticker
            ticker_search_query = f"Find the stock ticker symbol for {company_name}. Return ONLY the ticker symbol."
            logger.info(f"[FALLBACK] Web Agent searching for ticker: {ticker_search_query}")
            
            try:
                # Execute Web Agent search
                activity = AgentActivity("Web Agent", ticker_search_query)
                activity.status = "processing"
                
                response = self.agent_team.run(ticker_search_query)
                
                if hasattr(response, 'content'):
                    ticker_info = response.content
                elif isinstance(response, str):
                    ticker_info = response
                else:
                    ticker_info = str(response)
                
                logger.info(f"[FALLBACK] Ticker search result: {ticker_info[:100]}")
                
                # Extract ticker from response (usually first line or symbol-like pattern)
                ticker = self._extract_ticker_from_response(ticker_info)
                
                if ticker:
                    logger.info(f"[FALLBACK] Found ticker: {ticker}. Retrying Finance Agent...")
                    
                    # Retry Finance Agent with ticker
                    retry_query = original_query.replace(company_name, ticker)
                    activity = AgentActivity("Finance Agent (Retry)", retry_query)
                    activity.status = "processing"
                    
                    retry_response = self.agent_team.run(f"{original_query} (use ticker: {ticker})")
                    
                    if hasattr(retry_response, 'content'):
                        result = retry_response.content
                    elif isinstance(retry_response, str):
                        result = retry_response
                    else:
                        result = str(retry_response)
                    
                    logger.info(f"[FALLBACK] Retry successful! Response: {len(result)} characters")
                    activity.result = result
                    activity.status = "complete"
                    save_agent_activity(activity)
                    
                    return result.strip()
            
            except Exception as e:
                logger.warning(f"[FALLBACK] Fallback attempt failed: {str(e)}")
                # Continue with original result
        
        return result
    
    def _extract_ticker_from_response(self, response: str) -> str:
        """Extract ticker symbol from Web Agent response."""
        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            # Look for patterns like TICKER, TICKER.NS, etc
            if line and len(line) <= 10 and (line.isupper() or '.' in line):
                return line
        # Fallback: return first non-empty word in uppercase
        for line in lines:
            line = line.strip()
            if line and not line.startswith('-') and not line.startswith('•'):
                return line[:10].upper()  # Limit to 10 chars for reasonable ticker size
        return None

    def _execute_agent_query(self, agent_type: str, query: str) -> tuple:
        """Execute query with the specified agent type and log activities.
        
        Returns: (result, failed) - result is the response, failed is True if error occurred
        """
        try:
            self.workflow_state.set_active_agent(agent_type)
            self.workflow_state.add_message(f"Executing with {agent_type}")
            
            # Create activity tracking
            activity = AgentActivity(agent_type, query)
            activity.status = "processing"
            
            logger.info(f"\n[EXECUTION] Sending query to {agent_type}")
            logger.info(f"[EXECUTION] Query: {query[:100]}...")
            
            # Execute using the agent team (which will use the right agent)
            response = self.agent_team.run(query)
            
            # Extract response content
            if hasattr(response, 'content'):
                result = response.content
            elif isinstance(response, str):
                result = response
            elif hasattr(response, 'message'):
                result = response.message
            else:
                result = str(response)
            
            logger.info(f"[EXECUTION] Agent response received ({len(result)} characters)")
            
            # Update activity
            activity.result = result
            activity.status = "complete"
            activity.end_time = datetime.now()
            
            # Log the activity to file
            save_agent_activity(activity)
            self.workflow_state.add_agent_activity(activity)
            
            self.workflow_state.add_message(f"Agent response: {len(result)} characters")
            
            return (result.strip() if result else "No response from agent"), False
        
        except Exception as e:
            error_msg = f"Error executing {agent_type} query: {str(e)}"
            logger.error(error_msg, exc_info=True)
            
            # Log the error activity
            activity = AgentActivity(agent_type, query)
            activity.error = str(e)
            activity.status = "error"
            activity.end_time = datetime.now()
            save_agent_activity(activity)
            
            self.workflow_state.add_message(f"Error: {error_msg}")
            return error_msg, True
    
    def _log_workflow_summary(self):
        """Log a summary of the entire workflow."""
        logger.info("WORKFLOW SUMMARY:")
        logger.info(f"  Status: {self.workflow_state.status}")
        logger.info(f"  Active Agents: {', '.join(self.workflow_state.active_agents)}")
        logger.info(f"  Current Agent: {self.workflow_state.current_agent}")
        logger.info(f"  Messages: {len(self.workflow_state.messages)}")
        logger.info(f"  Response Length: {len(self.workflow_state.final_response) if self.workflow_state.final_response else 0} chars")
        
        for msg in self.workflow_state.messages:
            logger.info(f"    - {msg}")
    
    def _get_workflow_metadata(self) -> Dict[str, Any]:
        """Get workflow metadata for dashboard display."""
        return {
            "status": self.workflow_state.status,
            "active_agents": self.workflow_state.active_agents,
            "current_agent": self.workflow_state.current_agent,
            "messages": self.workflow_state.messages[-10:],  # Last 10 messages
            "start_time": str(self.workflow_state.start_time) if self.workflow_state.start_time else None,
        }
    
    def get_workflow_state(self) -> Dict[str, Any]:
        """Get current workflow state for dashboard."""
        return self._get_workflow_metadata()
    
    def reset_workflow(self):
        """Reset workflow state for new query."""
        self.workflow_state.reset()


def clean_response(response: str) -> str:
    """Clean and format agent response for better readability."""
    try:
        # Remove extra whitespace
        response = response.strip()
        
        # Add structure if needed
        if len(response) > 0:
            # Ensure proper formatting for markdown
            lines = response.split('\n')
            cleaned_lines = []
            
            for line in lines:
                line = line.strip()
                if line:
                    cleaned_lines.append(line)
            
            response = '\n'.join(cleaned_lines)
        
        return response
    except:
        return response


def get_agent_handler() -> AgentHandler:
    """Get or create the singleton agent handler."""
    return AgentHandler()
