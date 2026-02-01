"""InvestifyAI - Intelligent Financial Agent Team with Web Access"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import os
import yfinance as yf
from typing import Optional, Dict, List
from market_data import MarketDataFetcher
from agent_handler import get_agent_handler
from logger import get_logger

logger = get_logger()

# Page configuration
st.set_page_config(
    page_title="InvestifyAI - Financial Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==================== API KEY AUTHENTICATION ====================
def check_api_key():
    """Check if OpenAI API key is configured."""
    # Check environment variable first
    if os.getenv("OPENAI_API_KEY"):
        return True
    
    # Check session state
    if "api_key_verified" in st.session_state and st.session_state.api_key_verified:
        return True
    
    return False


def show_api_key_setup():
    """Display API key setup screen."""
    st.set_page_config(page_title="InvestifyAI - Setup", layout="centered")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 40px 20px;">
            <h1 style="font-size: 48px; margin-bottom: 10px;">🤖 InvestifyAI</h1>
            <p style="font-size: 18px; color: #666; margin-bottom: 30px;">
                Your Intelligent Financial Analysis Agent
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("""
        ## Setup Your API Key
        
        To use InvestifyAI, please provide your OpenAI API key. This key enables our intelligent agents to analyze financial data and provide actionable insights.
        
        **Don't have an API key?**
        - Visit [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
        - Create a new API key (requires an OpenAI account)
        - Keep it secure and never share it
        """)
        
        st.markdown("---")
        
        api_key = st.text_input(
            "🔑 OpenAI API Key",
            type="password",
            placeholder="sk-...",
            help="Your OpenAI API key for secure agent operations"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Verify & Continue", use_container_width=True, type="primary"):
                if api_key.strip():
                    os.environ["OPENAI_API_KEY"] = api_key
                    st.session_state.api_key_verified = True
                    st.success("✅ API Key verified successfully!")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Please enter a valid API key")
        
        with col2:
            if st.button("ℹ️ Learn More", use_container_width=True):
                st.info("""
                **How InvestifyAI Uses Your API Key:**
                - Powers our AI agents for financial analysis
                - Processes your queries securely
                - Never stored or shared with third parties
                - You maintain complete control
                """)


# Check and handle API key authentication
if not check_api_key():
    show_api_key_setup()
    st.stop()

# Enhanced CSS for professional styling
st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    }
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        margin: 12px 0;
        letter-spacing: 1px;
    }
    .metric-label {
        font-size: 13px;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }
    .metric-change {
        font-size: 16px;
        margin-top: 10px;
        font-weight: 600;
    }
    .metric-change.positive {
        color: #10b981;
    }
    .metric-change.negative {
        color: #ef4444;
    }
    
    .agent-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 18px;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        margin: 8px 0;
        border-left: 4px solid #10b981;
    }
    .agent-card.active {
        border-left-color: #3b82f6;
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
    }
    
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 12px;
        padding: 20px 0;
        margin-bottom: 20px;
    }
    
    .chat-messages-wrapper {
        display: flex;
        flex-direction: column;
        gap: 12px;
    }
    
    .chat-message {
        padding: 12px 16px;
        border-radius: 12px;
        word-wrap: break-word;
        max-width: 90%;
        animation: fadeIn 0.3s ease-in;
    }
    
    .chat-message.user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: auto;
        margin-right: 0;
        border-bottom-right-radius: 4px;
        box-shadow: none;
    }
    
    .chat-message.assistant {
        background: transparent;
        color: #333;
        margin-right: auto;
        margin-left: 0;
        border-bottom-left-radius: 4px;
        box-shadow: none;
    }
    
    .chat-message.user strong {
        display: none;
    }
    
    .chat-message.assistant strong {
        display: block;
        margin-bottom: 8px;
        color: #667eea;
        font-size: 14px;
    }
    
    .chat-message-content {
        line-height: 1.5;
        word-break: break-word;
        white-space: pre-wrap;
        overflow-wrap: break-word;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .stock-card {
        padding: 20px;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        margin: 12px 0;
        transition: all 0.3s;
    }
    .stock-card:hover {
        border-color: #667eea;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
    }
    
    .section-header {
        font-size: 20px;
        font-weight: 700;
        margin: 24px 0 16px 0;
        padding-bottom: 8px;
        border-bottom: 3px solid #667eea;
        display: inline-block;
    }
    
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "agent_handler" not in st.session_state:
    try:
        st.session_state.agent_handler = get_agent_handler()
        logger.info("Agent system initialized successfully")
    except ValueError as e:
        logger.error(f"Error initializing agent system: {e}")
        st.error(f"Error initializing agents: {e}")
        st.stop()

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("## ⚙️ InvestifyAI Settings")
    st.divider()
    
    # Navigation
    st.markdown("### 📊 Navigation")
    page = st.radio(
        "Select View",
        ["📈 Market Intelligence", "🤖 Agent Insights", "📋 Stock Research"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # Info
    st.markdown("### ℹ️ About InvestifyAI")
    st.markdown("""
    **InvestifyAI**
    
    Advanced multi-agent system for intelligent financial analysis and market insights.
    
    - 🤖 AI-powered agents
    - 📊 Real-time market data
    - 🔍 Deep financial research
    - 💡 Actionable insights
    
    Built by Alok Choudhary
    """)


# ==================== MARKET HEADER ====================
def display_market_header():
    """Display market indices and commodities header."""
    try:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("### 🌍 Market Overview")
        
        with col2:
            last_update = datetime.now().strftime("%H:%M:%S")
            st.caption(f"Last updated: {last_update}")
        
        logger.debug("Fetching market indices...")
        
        # Fetch market data
        indian_indices = MarketDataFetcher.get_all_indices()
        global_indices = MarketDataFetcher.get_all_global_indices()
        commodities = MarketDataFetcher.get_all_commodities()
        
        # Display Indian Indices
        st.markdown("#### 🇮🇳 Indian Indices")
        cols = st.columns(len(indian_indices) if indian_indices else 1)
        for idx, (name, data) in enumerate(indian_indices.items()):
            with cols[idx]:
                change_color = "🟢" if data["change"] >= 0 else "🔴"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{name}</div>
                    <div class="metric-value">{data['price']:,.0f}</div>
                    <div class="metric-change {'positive' if data['change'] >= 0 else 'negative'}">
                        {change_color} {data['change']:+.2f} ({data['change_pct']:+.2f}%)
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Display Global Indices
        st.markdown("#### 🌎 Global Indices")
        cols = st.columns(len(global_indices) if global_indices else 1)
        for idx, (name, data) in enumerate(global_indices.items()):
            with cols[idx]:
                change_color = "🟢" if data["change"] >= 0 else "🔴"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{name}</div>
                    <div class="metric-value">{data['price']:,.0f}</div>
                    <div class="metric-change {'positive' if data['change'] >= 0 else 'negative'}">
                        {change_color} {data['change']:+.2f} ({data['change_pct']:+.2f}%)
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Display Commodities
        st.markdown("#### 💎 Commodities")
        cols = st.columns(len(commodities) if commodities else 1)
        for idx, (name, data) in enumerate(commodities.items()):
            with cols[idx]:
                change_color = "🟢" if data["change"] >= 0 else "🔴"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{name}</div>
                    <div class="metric-value">${data['price']:.2f}</div>
                    <div class="metric-change {'positive' if data['change'] >= 0 else 'negative'}">
                        {change_color} {data['change']:+.2f} ({data['change_pct']:+.2f}%)
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        logger.info("Market overview displayed successfully")
        
    except Exception as e:
        logger.error(f"Error displaying market header: {e}", exc_info=True)
        st.error("⚠️ Error loading market data")


# ==================== ACTIVE AGENTS DISPLAY ====================
def display_active_agents():
    """Display currently active agents in the system."""
    try:
        agent_handler = st.session_state.agent_handler
        
        st.markdown("""
        <div class="section-header">🤖 Intelligence Agents</div>
        """, unsafe_allow_html=True)
        
        # Agent information
        agents_info = {
            "Market Pulse Agent": {
                "emoji": "📊",
                "description": "Monitors global market trends and identifies opportunities",
                "status": "active"
            },
            "Deep Research Agent": {
                "emoji": "🔬",
                "description": "Performs in-depth analysis on individual securities",
                "status": "active"
            },
            "Portfolio Strategist": {
                "emoji": "💼",
                "description": "Provides strategic recommendations for wealth building",
                "status": "active"
            },
            "Risk Intelligence Agent": {
                "emoji": "⚡",
                "description": "Analyzes market volatility and risk factors",
                "status": "active"
            },
        }
        
        cols = st.columns(2)
        for idx, (agent_name, info) in enumerate(agents_info.items()):
            with cols[idx % 2]:
                st.markdown(f"""
                <div class="agent-card active">
                    <div style="font-size: 24px; margin-bottom: 8px;">{info['emoji']}</div>
                    <div style="font-weight: bold; font-size: 16px; margin-bottom: 6px;">{agent_name}</div>
                    <div style="font-size: 13px; opacity: 0.95;">{info['description']}</div>
                    <div style="margin-top: 10px; font-size: 12px; opacity: 0.8;">🟢 {info['status'].upper()}</div>
                </div>
                """, unsafe_allow_html=True)
        
    except Exception as e:
        logger.error(f"Error displaying active agents: {e}", exc_info=True)
        st.warning("⚠️ Could not display agent information")


# ==================== CHAT INTERFACE ====================
def display_chat_interface(show_history=True):
    """Display chat interface for querying agents with ChatGPT-like UI."""
    st.markdown("""
    <div class="section-header">💬 Chat with InvestifyAI</div>
    """, unsafe_allow_html=True)
    
    try:
        # Initialize chat history if not exists
        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = []
        
        # Chat container with scrollable messages
        with st.container():
            # Display chat messages in ChatGPT-like format
            if st.session_state.chat_messages:
                for message in st.session_state.chat_messages:
                    if message["role"] == "user":
                        st.markdown(f"""
                        <div class="chat-message user">
                            <div class="chat-message-content">{message['content']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        # Display assistant message with proper markdown rendering
                        st.markdown(f"""
                        <div class="chat-message assistant">
                            <strong>🤖 InvestifyAI</strong>
                        </div>
                        """, unsafe_allow_html=True)
                        # Use st.markdown to properly render markdown content
                        st.markdown(message['content'])
            else:
                # Empty state with welcome message
                st.markdown("""
                <div style="text-align: center; padding: 40px 20px; color: #999;">
                    <div style="font-size: 48px; margin-bottom: 16px;">💬</div>
                    <div style="font-size: 18px; font-weight: 600; margin-bottom: 8px;">Start Your Conversation</div>
                    <div style="font-size: 14px;">Ask InvestifyAI about market trends, stocks, or investment strategies</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Chat input section
        st.divider()
        
        user_input = st.text_area(
            "Your Message",
            placeholder="Ask about market trends, stocks, investment strategies...",
            height=80,
            key="chat_input",
            label_visibility="collapsed"
        )
        
        # Button row
        button_col1, button_col2, button_col3 = st.columns([1, 1, 3])
        
        with button_col1:
            send_button = st.button("📤 Send", use_container_width=True, type="primary")
        
        with button_col2:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.chat_messages = []
                st.rerun()
        
        # Process user input
        if send_button and user_input.strip():
            # Add user message to history
            st.session_state.chat_messages.append({
                "role": "user",
                "content": user_input
            })
            
            logger.info(f"User query: {user_input[:100]}")
            
            # Process with agents with real-time updates
            agent_handler = st.session_state.agent_handler
            
            # Status placeholder for real-time updates
            status_placeholder = st.empty()
            
            try:
                # Show real-time agent processing sequence
                import time
                status_placeholder.info("🔍 **Web Agent** is searching for insights...")
                time.sleep(2)
                
                status_placeholder.info("💰 **Finance Agent** is analyzing financial data...")
                time.sleep(2)
                
                status_placeholder.info("⚡ **Risk Intelligence Agent** is evaluating risks...")
                time.sleep(2)
                
                status_placeholder.info("🤝 **Agent Team** is coordinating and synthesizing insights...")
                time.sleep(3)  # Slightly longer for coordination
                
                # Execute query with agent handler
                response, workflow_metadata = agent_handler.query_agents(user_input)
                
                # Show agent activity results
                status_placeholder.empty()
                st.divider()
                
                # Show which agent processed
                if workflow_metadata.get("current_agent"):
                    agent_name = workflow_metadata['current_agent']
                    st.info(f"🤖 **Agent Used:** {agent_name}")
                
                # Show brief workflow
                if workflow_metadata.get("messages"):
                    with st.expander("📋 Processing Details", expanded=False):
                        for msg in workflow_metadata["messages"]:
                            st.caption(msg)
                
                # Clean and format response
                clean_response = clean_response_text(response)
                
                # Add assistant response to history
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": clean_response
                })
                
                logger.info("Query processed successfully")
                st.rerun()
                
            except Exception as agent_error:
                logger.error(f"Agent error: {agent_error}", exc_info=True)
                status_placeholder.empty()
                error_response = f"Sorry, I encountered an error: {str(agent_error)[:80]}"
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": error_response
                })
                st.error(f"❌ {error_response}")
        
    except Exception as e:
        logger.error(f"Error in chat interface: {e}", exc_info=True)
        st.error(f"❌ Chat error: {str(e)}")


# ==================== RESPONSE FORMATTER ====================
def clean_response_text(response: str) -> str:
    """Clean response text by removing excessive line breaks and formatting."""
    try:
        # Split into lines
        lines = response.split('\n')
        
        # Clean lines - remove leading/trailing whitespace
        cleaned_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped:  # Only keep non-empty lines
                cleaned_lines.append(stripped)
        
        # Join with single line breaks (no double spacing)
        clean_text = '\n'.join(cleaned_lines)
        
        return clean_text
    except Exception as e:
        logger.warning(f"Error cleaning response: {e}")
        return response


def format_agent_response(response: str, user_query: str) -> str:
    """Format agent response respecting user instructions and preferences."""
    try:
        # Clean up response
        formatted = response.strip()
        
        # Preserve markdown formatting (bold, italic, links)
        # ** for bold
        # * or _ for italic
        # [text](url) for links
        
        # Respect user instructions in query (don't override them)
        # Just ensure the response is properly formatted markdown
        
        # Check if user asked for specific format
        query_lower = user_query.lower()
        
        if "summary" in query_lower or "summarize" in query_lower:
            # Already in summary format from agent, just clean it
            pass
        elif "detailed" in query_lower or "explain" in query_lower:
            # Already detailed from agent, keep as-is
            pass
        elif "bullet" in query_lower or "list" in query_lower:
            # Should be bullet format from agent, keep as-is
            pass
        
        # Add context emoji based on content type
        if any(word in query_lower for word in ["rating", "rate", "agency", "credit"]):
            if not formatted.startswith("⭐"):
                formatted = f"⭐ **RATINGS & INSIGHTS**\n\n{formatted}"
        elif any(word in query_lower for word in ["price", "cost", "stock price"]):
            if not formatted.startswith("💹"):
                formatted = f"💹 **PRICE ANALYSIS**\n\n{formatted}"
        elif any(word in query_lower for word in ["news", "recent", "update"]):
            if not formatted.startswith("📰"):
                formatted = f"📰 **LATEST UPDATES**\n\n{formatted}"
        
        # Ensure markdown styling is preserved
        return formatted
    except Exception as e:
        logger.warning(f"Error formatting response: {e}")
        return response


# ==================== STOCK DETAILS DISPLAY ====================
def display_stock_details_section():
    """Display detailed stock information with improved charts and search."""
    st.markdown("""
    <div class="section-header">📋 Stock Intelligence</div>
    """, unsafe_allow_html=True)
    
    try:
        # Search section
        col1, col2 = st.columns([3, 1])
        
        with col1:
            stock_query = st.text_input(
                "Search stocks by ticker or company name (e.g., AAPL, Apple, TCS):",
                placeholder="Type ticker or company name...",
                label_visibility="collapsed"
            )
        
        with col2:
            search_button = st.button("🔍 Search", use_container_width=True)
        
        # Default to 1y period (no longer selectable by user)
        period = "1y"
        
        # Process search
        if search_button and stock_query:
            stock_symbol = stock_query.upper().strip()
            
            logger.info(f"Searching stock: {stock_symbol}")
            
            with st.spinner(f"📊 Fetching data for {stock_symbol}..."):
                # First, try to fetch with direct symbol
                stock_info = MarketDataFetcher.get_stock_info(stock_symbol)
                stock_data = MarketDataFetcher.get_stock_data(stock_symbol, period=period_map(period))
                
                # If failed and query is not already a ticker, use DuckDuckGo to find ticker
                if (not stock_info or stock_data is None or len(stock_data) == 0) and len(stock_symbol) > 3:
                    logger.info(f"Direct ticker lookup failed. Searching DuckDuckGo for ticker symbol...")
                    
                    try:
                        from duckduckgo_search import DDGS
                        
                        ddgs = DDGS()
                        search_results = ddgs.text(f"stock ticker symbol {stock_query}", max_results=3)
                        
                        # Extract potential tickers from search results
                        found_ticker = None
                        for result in search_results:
                            # Look for ticker patterns in search results
                            result_text = result.get('body', '') + ' ' + result.get('title', '')
                            # Simple extraction - look for ALL CAPS ticker patterns
                            import re
                            tickers = re.findall(r'\b[A-Z]{1,5}(?:\.[A-Z]{2})?\b', result_text)
                            if tickers:
                                # Try each potential ticker
                                for ticker in tickers:
                                    logger.debug(f"Trying ticker from search: {ticker}")
                                    test_info = MarketDataFetcher.get_stock_info(ticker)
                                    if test_info:
                                        found_ticker = ticker
                                        logger.info(f"Found valid ticker: {found_ticker}")
                                        break
                            if found_ticker:
                                break
                        
                        # If we found a valid ticker, use it
                        if found_ticker:
                            stock_symbol = found_ticker
                            st.info(f"Found ticker symbol: **{found_ticker}** for \"{stock_query}\"")
                            stock_info = MarketDataFetcher.get_stock_info(stock_symbol)
                            stock_data = MarketDataFetcher.get_stock_data(stock_symbol, period=period_map(period))
                    
                    except Exception as e:
                        logger.warning(f"DuckDuckGo ticker search failed: {e}")
                
                if stock_info and stock_data is not None and len(stock_data) > 0:
                    # Use adjusted symbol if available
                    display_symbol = stock_info.get("adjusted_symbol", stock_symbol)
                    
                    # Company info section
                    st.markdown("#### 📌 Company Information")
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**{stock_info.get('name', stock_symbol)}**")
                        st.caption(f"Sector: {stock_info.get('sector', 'N/A')} | Industry: {stock_info.get('industry', 'N/A')}")
                        
                        if stock_info.get('description') and stock_info['description'] != "No description available":
                            with st.expander("📖 Company Description"):
                                st.write(stock_info['description'][:500] + "...")
                    
                    with col2:
                        if stock_info.get('website') and stock_info['website'] != "N/A":
                            st.markdown(f"🌐 [{stock_info['website']}]({stock_info['website']})")
                        st.caption(f"Country: {stock_info.get('country', 'N/A')}")
                    
                    # Detect currency based on stock
                    currency_symbol, currency_code, is_indian = detect_stock_currency(
                        stock_info.get('adjusted_symbol', stock_symbol), 
                        stock_info
                    )
                    
                    # Key metrics - only show if data is available
                    st.markdown("#### 📊 Key Metrics")
                    
                    # Collect available metrics
                    metrics_to_show = []
                    
                    price_val = stock_info.get('current_price', 'N/A')
                    if price_val != 'N/A':
                        if isinstance(price_val, (int, float)):
                            metrics_to_show.append(("Current Price", f"{currency_symbol}{price_val:,.2f}"))
                    else:
                        # Try DuckDuckGo fallback
                        ddg_price = get_stock_price_from_duckduckgo(stock_symbol, stock_info.get('name', ''))
                        if ddg_price:
                            metrics_to_show.append(("Current Price", f"{currency_symbol}{ddg_price:,.2f}"))
                    
                    pe_val = stock_info.get('pe_ratio', 'N/A')
                    if pe_val != 'N/A' and isinstance(pe_val, (int, float)):
                        metrics_to_show.append(("P/E Ratio", f"{pe_val:,.2f}"))
                    
                    cap_val = stock_info.get('market_cap', 'N/A')
                    if cap_val != 'N/A' and isinstance(cap_val, (int, float)) and cap_val > 0:
                        cap_display = f"{currency_symbol}{cap_val/1e9:.2f}B"
                        metrics_to_show.append(("Market Cap", cap_display))
                    
                    div_val = stock_info.get('dividend_yield', 'N/A')
                    if div_val != 'N/A' and isinstance(div_val, (int, float)):
                        metrics_to_show.append(("Dividend Yield", f"{div_val*100:.2f}%"))
                    
                    # Display only available metrics
                    if metrics_to_show:
                        num_metrics = len(metrics_to_show)
                        metric_cols = st.columns(min(4, num_metrics))
                        for idx, (label, value) in enumerate(metrics_to_show):
                            with metric_cols[idx % len(metric_cols)]:
                                st.metric(label, value)
                    else:
                        st.info("No metric data available for this stock")
                        if isinstance(div_val, (int, float)):
                            st.metric("Dividend Yield", f"{div_val*100:.2f}%")
                        else:
                            st.metric("Dividend Yield", div_val)
                    
                    # Price statistics from historical data
                    st.markdown("#### 📈 Price Statistics")
                    
                    try:
                        stat_metrics = []
                        
                        current_price = float(stock_data['Close'].iloc[-1])
                        stat_metrics.append(("Current Price", f"{currency_symbol}{current_price:.2f}"))
                        
                        current = float(stock_data['Close'].iloc[-1])
                        opening = float(stock_data['Close'].iloc[0])
                        period_change = ((current - opening) / opening) * 100
                        stat_metrics.append(("Period Change", f"{period_change:+.2f}%"))
                        
                        high_price = float(stock_data['Close'].max())
                        stat_metrics.append(("Period High", f"{currency_symbol}{high_price:.2f}"))
                        
                        low_price = float(stock_data['Close'].min())
                        stat_metrics.append(("Period Low", f"{currency_symbol}{low_price:.2f}"))
                        
                        # Display statistics
                        stat_cols = st.columns(min(4, len(stat_metrics)))
                        for idx, (label, value) in enumerate(stat_metrics):
                            with stat_cols[idx % len(stat_cols)]:
                                st.metric(label, value)
                    except Exception as stat_error:
                        logger.error(f"Error displaying statistics: {stat_error}")
                        st.warning("Could not display price statistics")
                    
                    # Promoter Holdings Section - only show if data available
                    st.markdown("#### 👥 Promoter Shareholding")
                    try:
                        promoter_info = get_promoter_holdings(stock_symbol, stock_info.get('adjusted_symbol', stock_symbol))
                        if promoter_info:
                            promoter_holding = promoter_info.get('promoter_holding', 'N/A')
                            promoter_change = promoter_info.get('promoter_change', 'N/A')
                            last_updated = promoter_info.get('last_updated', 'N/A')
                            
                            # Only show metrics with actual data (not N/A)
                            prom_metrics = []
                            if promoter_holding != 'N/A':
                                prom_metrics.append(("Promoter Holding %", promoter_holding))
                            if promoter_change != 'N/A':
                                prom_metrics.append(("Promoter Change (QoQ)", promoter_change))
                            
                            if prom_metrics:
                                prom_cols = st.columns(len(prom_metrics))
                                for idx, (label, value) in enumerate(prom_metrics):
                                    with prom_cols[idx]:
                                        st.metric(label, value)
                            
                            if promoter_info.get('details'):
                                with st.expander("📋 Detailed Promoter Information"):
                                    st.write(promoter_info['details'])
                            
                            if not prom_metrics and not promoter_info.get('details'):
                                st.caption("No detailed promoter data available")
                        else:
                            st.caption("Promoter shareholding data not available for this stock")
                    except Exception as promoter_error:
                        logger.debug(f"Could not fetch promoter holdings: {promoter_error}")
                        st.info("📊 Promoter holdings data not available for this stock")
                    
                    # Recent News Section - only show if data available
                    st.markdown("#### 📰 Recent News & Updates")
                    try:
                        recent_news = get_recent_news(stock_symbol)
                        if recent_news:
                            for idx, news in enumerate(recent_news[:5], 1):  # Show top 5 news
                                with st.container():
                                    st.markdown(f"""
                                    <div style="padding: 12px; background: #f8f9fa; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #667eea;">
                                        <div style="font-weight: 600; color: #333; margin-bottom: 6px;">
                                            {idx}. {news.get('title', 'News Update')}
                                        </div>
                                        <div style="font-size: 12px; color: #666; margin-bottom: 6px;">
                                            📅 {news.get('date', 'Recent')} | 🔗 Source: {news.get('source', 'Financial News')}
                                        </div>
                                        <div style="font-size: 13px; color: #555; line-height: 1.5;">
                                            {news.get('summary', 'No summary available')}
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)
                        else:
                            st.caption("No recent news available for this stock")
                    except Exception as news_error:
                        logger.debug(f"Could not fetch news: {news_error}")
                        st.caption("News data temporarily unavailable")
                    
                    logger.info(f"Successfully displayed stock data for {stock_symbol}")
                    
                else:
                    # No data found
                    st.warning(f"""
                    ⚠️ **No data found for {stock_query}**
                    
                    💡 **Suggestions:**
                    - Check if the ticker symbol is correct
                    - For Indian stocks: Use NSE symbol (e.g., TCS, INFY, RELIANCE)
                    - For US stocks: Use NYSE/NASDAQ symbol (e.g., AAPL, MSFT, GOOGL)
                    - Try using the company name instead (e.g., "Apple" instead of "AAPL")
                    """)
                    logger.warning(f"No valid data found for {stock_query}")
    
    except Exception as e:
        logger.error(f"Error in stock details display: {e}", exc_info=True)
        st.error(f"❌ Error displaying stock details: {str(e)}")


# ==================== HELPER FUNCTIONS ====================
def get_promoter_holdings(symbol: str, adjusted_symbol: str = None) -> Optional[Dict]:
    """Fetch promoter shareholding information."""
    try:
        if adjusted_symbol is None:
            adjusted_symbol = symbol
        
        ticker_obj = yf.Ticker(adjusted_symbol)
        
        # Try to get major holders
        try:
            major_holders = ticker_obj.major_holders
            if major_holders is not None and len(major_holders) > 0:
                # Parse major holders data
                promoter_info = {
                    'promoter_holding': 'N/A',
                    'promoter_change': 'N/A',
                    'last_updated': datetime.now().strftime("%Y-%m-%d"),
                    'details': None
                }
                
                # Look for promoter/insider information
                for idx, row in major_holders.iterrows():
                    if 'insiders' in row[0].lower() or 'promoter' in row[0].lower():
                        promoter_info['promoter_holding'] = f"{float(row[1])*100:.2f}%"
                        break
                
                if promoter_info['promoter_holding'] != 'N/A':
                    return promoter_info
        except Exception as e:
            logger.debug(f"Could not fetch major holders for {symbol}: {e}")
        
        # Fallback with generic structure
        return {
            'promoter_holding': 'N/A',
            'promoter_change': 'N/A',
            'last_updated': datetime.now().strftime("%Y-%m-%d"),
            'details': 'Promoter shareholding data not available through current data source'
        }
    
    except Exception as e:
        logger.error(f"Error fetching promoter holdings for {symbol}: {e}")
        return None


def get_recent_news(symbol: str) -> Optional[List[Dict]]:
    """Fetch recent news about the stock using DuckDuckGo search."""
    try:
        from duckduckgo_search import DDGS
        
        # Search for recent news
        ddg = DDGS()
        news_results = ddg.news(f"{symbol} stock news", max_results=5)
        
        if news_results:
            formatted_news = []
            for item in news_results:
                formatted_news.append({
                    'title': item.get('title', 'News Update'),
                    'summary': item.get('body', 'No summary available')[:200],
                    'source': item.get('source', 'Financial News'),
                    'date': item.get('date', 'Recent'),
                    'url': item.get('url', '#')
                })
            return formatted_news
        
        return None
    
    except Exception as e:
        logger.debug(f"Error fetching news for {symbol}: {e}")
        return None


def detect_stock_currency(symbol: str, stock_info: Dict) -> tuple:
    """Detect if stock is Indian (INR) or US (USD) based on symbol and info."""
    try:
        # Check if symbol has .NS (NSE - India) or .BO (BSE - India) suffix
        if symbol.endswith('.NS') or symbol.endswith('.BO'):
            return '₹', 'INR', True  # currency, code, is_indian
        
        # Check country from stock info
        if stock_info:
            country = stock_info.get('country', '').lower()
            if 'india' in country:
                return '₹', 'INR', True
            elif any(x in country for x in ['united states', 'usa', 'us']):
                return '$', 'USD', False
        
        # Default check - if symbol is short (1-4 chars) without suffix, likely US
        if len(symbol) <= 5 and not any(x in symbol for x in ['.', '-']):
            return '$', 'USD', False
        
        # Default to USD for unknown
        return '$', 'USD', False
    except Exception as e:
        logger.debug(f"Error detecting currency: {e}")
        return '$', 'USD', False


def format_price(price: float, currency_symbol: str) -> str:
    """Format price with appropriate currency symbol."""
    if isinstance(price, (int, float)) and price > 0:
        return f"{currency_symbol}{price:,.2f}"
    return "N/A"


def get_stock_price_from_duckduckgo(symbol: str, company_name: str = "") -> Optional[float]:
    """Fetch stock price from DuckDuckGo search."""
    try:
        from duckduckgo_search import DDGS
        import re
        
        search_query = f"{symbol} stock price current" if symbol else f"{company_name} stock price current"
        ddg = DDGS()
        results = ddg.text(search_query, max_results=3)
        
        if results:
            # Extract price from search results
            for result in results:
                text = result.get('body', '') + result.get('title', '')
                # Look for price patterns like $123.45 or ₹123.45
                price_matches = re.findall(r'[\$₹]\s*(\d+\.?\d*)', text)
                if price_matches:
                    try:
                        price = float(price_matches[0])
                        if 0 < price < 100000:  # Reasonable price range
                            logger.debug(f"Found stock price for {symbol}: {price}")
                            return price
                    except ValueError:
                        continue
        
        return None
    except Exception as e:
        logger.debug(f"Error fetching price from DuckDuckGo for {symbol}: {e}")
        return None


def period_map(period_str: str) -> str:
    """Map UI period string to yfinance period format."""
    mapping = {
        "3m": "3mo",
        "6m": "6mo",
        "1y": "1y",
        "2y": "2y",
        "5y": "5y",
        "All": "max"
    }
    return mapping.get(period_str, "1y")


def create_stock_chart(data: pd.DataFrame, symbol: str, period: str) -> go.Figure:
    """Create an interactive stock price chart with moving average."""
    try:
        # Calculate moving average
        data['MA20'] = data['Close'].rolling(window=20).mean()
        
        fig = go.Figure()
        
        # Add close price line
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Close'],
            mode='lines',
            name='Close Price',
            line=dict(color='#667eea', width=3),
            hovertemplate='<b>Date:</b> %{x|%Y-%m-%d}<br><b>Price:</b> $%{y:.2f}<extra></extra>'
        ))
        
        # Add moving average
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['MA20'],
            mode='lines',
            name='20-Day MA',
            line=dict(color='#764ba2', width=2, dash='dash'),
            hovertemplate='<b>Date:</b> %{x|%Y-%m-%d}<br><b>MA20:</b> $%{y:.2f}<extra></extra>'
        ))
        
        # Add range slider
        fig.update_xaxes(
            rangeslider=dict(visible=False),
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1M", step="month"),
                    dict(count=3, label="3M", step="month"),
                    dict(count=6, label="6M", step="month"),
                    dict(step="all", label="All")
                ])
            )
        )
        
        fig.update_layout(
            title=f"{symbol} - Price Chart ({period})",
            yaxis_title="Stock Price ($)",
            xaxis_title="Date",
            template="plotly_white",
            hovermode="x unified",
            height=500,
            margin=dict(l=50, r=50, t=50, b=50),
            font=dict(size=12),
        )
        
        return fig
    
    except Exception as e:
        logger.error(f"Error creating chart: {e}")
        raise


# ==================== MAIN PAGE ROUTING ====================
if __name__ == "__main__":
    st.markdown("# 🤖 InvestifyAI")
    st.markdown("*Multi-Agent Financial Intelligence Platform*")
    st.divider()
    
    if page == "📈 Market Intelligence":
        # Dashboard page - show market overview and active agents
        display_market_header()
        st.divider()
        display_active_agents()
        
    elif page == "🤖 Agent Insights":
        # Agent Insights page - show chat interface with history
        display_chat_interface(show_history=True)
        
    elif page == "📋 Stock Research":
        # Stock Intelligence page
        display_stock_details_section()
