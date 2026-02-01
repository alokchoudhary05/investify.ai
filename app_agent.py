import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.team import Team
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from agno.os import AgentOS

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

# Setup database for storage
db = SqliteDb(db_file="agents.db")

web_agent = Agent(
    name="Web Agent",
    role="Search the web for information",
    model=OpenAIChat(id="gpt-4o", api_key=api_key),
    tools=[DuckDuckGoTools()],
    db=db,
    add_history_to_context=True,
    markdown=True,
)

finance_agent = Agent(
    name="Finance Agent",
    role="Get financial data",
    model=OpenAIChat(id="gpt-4o", api_key=api_key),
    tools=[YFinanceTools(include_tools=["get_current_stock_price", "get_company_info", "get_company_news", "get_analyst_recommendations"])],
    instructions=["Always use tables to display data"],
    db=db,
    add_history_to_context=True,
    markdown=True,
)

chat_agent = Agent(
    name="Chat Agent",
    role="Provide general conversation and coordinate queries to specialized agents",
    model=OpenAIChat(id="gpt-4o", api_key=api_key),
    tools=[],
    instructions=[
        "Engage in helpful and friendly conversation",
        "Provide clear explanations on various topics",
        "Route financial questions to the Finance Agent",
        "Route research questions to the Web Agent",
        "Be conversational and easy to understand"
    ],
    db=db,
    add_history_to_context=True,
    markdown=True,
)

agent_team = Team(
    name="Agent Team (Web+Finance+Chat)",
    model=OpenAIChat(id="gpt-4o", api_key=api_key),
    members=[chat_agent, web_agent, finance_agent],
    debug_mode=True,
    markdown=True,
)

agent_os = AgentOS(teams=[agent_team])
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app="app_agent:app", reload=True)