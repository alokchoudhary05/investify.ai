# InvestifyAI - Intelligent Financial Agent Team with Web Access

A production-ready multi-agent AI system for advanced financial analysis, real-time market intelligence, and institutional-grade investment insights. InvestifyAI orchestrates specialized agents to deliver comprehensive market analysis, deep research, and strategic recommendations.

---

## Project Overview

### What is InvestifyAI?

InvestifyAI is an intelligent financial intelligence platform built on a collaborative multi-agent architecture. Rather than relying on a single monolithic model, it deploys specialized agents—each with distinct roles and expertise—that work together to deliver comprehensive financial insights.

The system combines:
- **Real-time market data** from financial APIs
- **Web intelligence** for emerging market trends and news using Duckduckgo Search
- **AI-driven analysis** through OpenAI GPT-4
- **Multi-agent collaboration** for holistic decision-making

### Problem Solved

Financial decision-making traditionally requires:
1. Manually aggregating data from multiple sources
2. Synthesizing conflicting market signals
3. Understanding complex risk/reward trade-offs
4. Keeping pace with emerging news and trends

**InvestifyAI automates this workflow** by orchestrating intelligent agents that simultaneously gather data, analyze fundamentals, assess risks, and synthesize actionable recommendations.

### Who It's Built For

- **Individual Investors**: Research stocks and make informed decisions with institutional-grade analysis
- **Financial Advisors**: Enhance client meetings with data-driven insights
- **Portfolio Managers**: Accelerate market monitoring and opportunity identification
- **FinTech Companies**: Integrate advanced financial intelligence into existing platforms
- **Developers & Researchers**: Extend the platform with custom agents and data sources

---

## Key Features

### 1. **Agent-Based Stock Research**
- Decompose complex financial questions into specialized agent tasks
- Each agent handles its domain of expertise autonomously
- Leverages web search and financial APIs for comprehensive data gathering

### 2. **Multi-Agent Collaboration**
- Agents work together seamlessly through a coordinator
- Share context and insights across analysis phases
- No single point of failure—graceful degradation if one agent struggles

### 3. **Real-Time Financial Insights**
- Live stock pricing and market data via YFinance
- News aggregation and trend analysis via web search
- Support for multiple asset classes: equities, indices, commodities

### 4. **Decision-Oriented Investment Guidance**
- Structured output combining fundamental analysis, technical factors, and risk assessment
- Actionable recommendations backed by data
- Clear confidence levels and caveats for transparency

### 5. **Interactive Dashboard**
- Streamlit-based UI for intuitive agent interaction
- Real-time streaming responses from agents
- Activity tracking and history management
- Multi-agent chat interface for complex queries

---
## Prototype (Date: February 3, 2026)
### Landing Page
<img width="1919" height="907" alt="image" src="https://github.com/user-attachments/assets/787a1323-4604-4fb8-8fb6-1ed479033638" />

### Market Overview
<img width="1912" height="907" alt="image" src="https://github.com/user-attachments/assets/eb472a9f-7fd1-49c8-bce3-e1f2ab7b701a" />
<img width="1909" height="908" alt="image" src="https://github.com/user-attachments/assets/23008fb5-e85f-481f-b3c0-a1ee59f29868" />

### Multi-Agent Collaboration Team
<img width="1909" height="907" alt="image" src="https://github.com/user-attachments/assets/823075a7-52eb-4e86-9179-24378de566e2" />

### Agent-Team Insights
<img width="1916" height="917" alt="image" src="https://github.com/user-attachments/assets/e2ab621b-83be-44bf-8571-6c5cd40c8617" />
<img width="1913" height="903" alt="image" src="https://github.com/user-attachments/assets/4af961ee-2a33-429c-a7f1-54861634cb91" />

<img width="1896" height="908" alt="image" src="https://github.com/user-attachments/assets/40689aa2-f23c-4573-a1bd-1695e29a6aa8" />
<img width="1919" height="910" alt="image" src="https://github.com/user-attachments/assets/e7f3ad9e-6fbe-45fd-89ab-0e05c6eb063e" />
<img width="1907" height="893" alt="image" src="https://github.com/user-attachments/assets/e3e2e2be-14bc-4c84-866e-72a9cde6a97d" />

### Stock Research Features
<img width="1909" height="904" alt="image" src="https://github.com/user-attachments/assets/a9124945-8e61-442f-a1de-1fd4101f1291" />

---
## System Design

### High-Level Architecture

```
┌─────────────────────────────────────┐
│   User Interface (Streamlit)        │
│   - API Configuration               │
│   - Chat Interface                  │
│   - Market Intelligence Views       │
└─────────────────┬───────────────────┘
                  │
         ┌────────▼─────────┐
         │  Agent Handler   │
         │ (Orchestration)  │
         └────────┬─────────┘
                  │
    ┌─────────────┼──────────────┐
    │             │              │
┌───▼────┐  ┌────▼──────┐  ┌────▼────┐
│ Market  │  │ Research  │  │Portfolio │
│ Pulse   │  │ Analysis  │  │Strategist│
│ Agent   │  │ Agent     │  │ Agent    │
└───┬────┘  └────┬──────┘  └────┬────┘
    │             │              │
    └─────────────┼──────────────┘
                  │
         ┌────────▼──────────┐
         │  LLM Layer        │
         │ (OpenAI GPT-4)    │
         └────────┬──────────┘
                  │
    ┌─────────────┼──────────────┐
    │             │              │
┌───▼────┐  ┌────▼──────┐  ┌────▼────┐
│YFinance │  │ DuckDuckGo│  │ SQLite   │
│  API    │  │   Search  │  │   DB     │
└─────────┘  └───────────┘  └──────────┘
```

### Data Flow

1. **User Query Intake** → Frontend captures user question (Streamlit)
2. **Query Distribution** → Agent Handler routes to appropriate agent(s)
3. **Data Collection** → Agents invoke tools (YFinance, web search)
4. **Analysis & Reasoning** → LLM processes data in agent context
5. **Response Synthesis** → Agents format and structure output
6. **User Delivery** → Results streamed to dashboard with full transparency

### Separation of Concerns

| Layer | Responsibility | Technology |
|-------|---|---|
| **Presentation** | User interaction, visualization | Streamlit, Plotly |
| **Orchestration** | Query routing, agent coordination | Agno Framework |
| **Intelligence** | Domain-specific analysis | OpenAI GPT-4 |
| **Tools** | Data collection and APIs | YFinance, DuckDuckGo |
| **Persistence** | Historical data, agent memory | SQLite |

---

## Agent Architecture

### Core Agents

#### 1. **Market Pulse Agent**
- **Role**: Monitor global markets and identify macro trends
- **Responsibilities**:
  - Track major indices (S&P 500, NASDAQ, SENSEX, NIFTY)
  - Monitor commodity prices (gold, oil, natural gas)
  - Identify emerging market opportunities
  - Alert on significant market movements
- **Tools**: YFinance, Web Search
- **Output**: Market summary, opportunity alerts, trend analysis

#### 2. **Research Analysis Agent**
- **Role**: Perform deep fundamental analysis on securities
- **Responsibilities**:
  - Analyze company financials and metrics
  - Research competitive positioning
  - Assess earnings quality and sustainability
  - Gather industry and peer comparisons
- **Tools**: YFinance (company data), Web Search (news & insights)
- **Output**: Comprehensive research report with key metrics and analysis

#### 3. **Portfolio Strategist Agent**
- **Role**: Synthesize insights into strategic recommendations
- **Responsibilities**:
  - Evaluate risk-adjusted returns
  - Consider portfolio diversification
  - Align recommendations with stated investment thesis
  - Provide entry/exit framework
- **Tools**: Web Search (macro data), Coordination with other agents
- **Output**: Actionable recommendations with confidence levels

#### 4. **Coordinator Agent** (Web Agent / Chat Agent)
- **Role**: Orchestrate multi-agent workflows and user communication
- **Responsibilities**:
  - Route complex queries to specialists
  - Synthesize multi-agent responses
  - Handle general conversation
  - Manage context between queries
- **Tools**: All tools available to specialists
- **Output**: Structured, cohesive final responses

### Agent Collaboration Pattern

```
User Query
    │
    ▼
Coordinator (understands intent)
    │
    ├──────────────────┬──────────────────┬─────────────────┐
    ▼                  ▼                  ▼                 ▼
Market Pulse     Research Analysis  Portfolio          Web Search
Agent            Agent              Strategist Agent    (for context)
    │                  │                  │                 │
    └──────────────────┴──────────────────┴─────────────────┘
                       │
                       ▼
              Synthesize Results
                       │
                       ▼
              Return Structured Output
```

### Agent Communication Protocol

1. **Query Reception**: Coordinator receives user input
2. **Intent Analysis**: Coordinator identifies required expertise
3. **Parallel Execution**: Specialists process in parallel where possible
4. **Result Aggregation**: Coordinator combines outputs
5. **Quality Check**: Verify completeness and coherence
6. **User Delivery**: Format and present to user

---

## Tech Stack

### Backend
- **Python 3.11+**: Core language
- **Agno Framework (v2.2.10+)**: Multi-agent orchestration and coordination
- **FastAPI**: Web API framework for production deployments
- **SQLAlchemy**: Object-relational mapping for database interactions

### Frontend
- **Streamlit (v1.28.0+)**: Interactive dashboard and UI
- **Plotly (v5.17.0+)**: Advanced data visualization and charting

### AI & Language Model
- **OpenAI GPT-4o**: Primary language model for agent reasoning
- **Python-dotenv**: Environment variable management for API keys

### Data & APIs
- **YFinance**: Real-time and historical stock data, company fundamentals
- **DuckDuckGo Search**: Web search for market news and trends
- **Pandas (v2.0.0+)**: Data manipulation and analysis
- **NumPy**: Numerical computing (via dependencies)

### Database & Persistence
- **SQLite**: Lightweight local database for agent memory and chat history
- **Agno SqliteDb**: Database interface for agent context persistence

### Infrastructure & Utilities
- **PyJWT**: Token-based authentication (future)
- **Uvicorn**: ASGI server for FastAPI

---

## How InvestifyAI Works

### Step-by-Step Workflow

#### 1. **Query Intake**
```
User enters: "Should I buy Microsoft? Analyze the current situation."
↓
Streamlit Dashboard captures input
↓
AgentHandler receives query + context
```

#### 2. **Intent Recognition**
```
Coordinator Agent analyzes:
  - Is this a stock analysis request? → YES
  - Multiple agents needed? → YES (Research + Market context)
  - Urgency? → Standard research timeline
```

#### 3. **Task Distribution**
```
Market Pulse Agent Task:
  ├─ Get MSFT current price
  ├─ Check overall tech sector momentum
  └─ Identify recent market catalysts

Research Analysis Agent Task:
  ├─ Fetch MSFT fundamentals (P/E, ROE, debt, etc.)
  ├─ Get recent earnings and guidance
  ├─ Search competitive analysis (vs. Google, Apple, Amazon)
  └─ Gather analyst consensus
```

---

## Use Cases

### 1. **Equity Research**
```
User Query: "Give me a deep dive on Tesla's EV market position."

InvestifyAI Response:
  - Industry analysis (EV adoption trends)
  - Company fundamentals (revenue, margins, capex)
  - Competitive landscape (legacy OEMs, EV-native competitors)
  - Bull/bear case with catalysts
  - Recommendation with entry/exit points
```

### 2. **Portfolio Rebalancing Decisions**
```
User Query: "My portfolio is 60% equities, 40% bonds. Macro environment?"

InvestifyAI Response:
  - Current market regime (rates, inflation, growth)
  - Sector rotation opportunities
  - Bond yield curve assessment
  - Recommended allocation adjustments
  - Specific tactical changes with rationale
```

### 3. **Risk & Volatility Analysis**
```
User Query: "Is the market overbought? What are key risks ahead?"

InvestifyAI Response:
  - Volatility metrics (VIX, put/call ratios)
  - Valuation vs. history
  - Geopolitical/macro risk factors
  - Liquidity conditions
  - Stress-test scenarios
  - Recommended hedges or position sizing
```

### 4. **Sector Rotation & Thematic Investing**
```
User Query: "Where is growth in 2026? Renewable energy opportunities?"

InvestifyAI Response:
  - Macro themes driving growth
  - Sector-level analysis
  - Key companies benefiting
  - Valuations vs. growth rates
  - Recommended plays with risk profiles
  - Timing and catalyst roadmap
```

---

## Installation & Setup

### Prerequisites

- **Python 3.11 or higher** ([Download](https://www.python.org/downloads/))
- **OpenAI API key** (sign up at [platform.openai.com](https://platform.openai.com))
- **Git** for version control
- **Virtual environment** (built-in, or use Conda)

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/investify.ai.git
cd investify.ai
```

### Step 2: Create Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv myenv
.\myenv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv myenv
source myenv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```bash
# .env
OPENAI_API_KEY=sk-your-openai-api-key-here
```

**Do NOT commit `.env` to version control.** Add to `.gitignore`:

```bash
echo ".env" >> .gitignore
```

### Step 5: Initialize Database

```bash
python -c "from agno.db.sqlite import SqliteDb; db = SqliteDb(db_file='agents.db')"
```

### Step 6: Run the Dashboard

```bash
streamlit run dashboard.py
```

The dashboard will open at `http://localhost:8501`

### Verification

- [ ] Dashboard loads without errors
- [ ] API key is recognized
- [ ] Agent Handler shows all agents as ready
- [ ] Test query returns structured response

---

## Configuration

### Environment Variables

| Variable | Required | Description | Example |
|----------|----------|---|---|
| `OPENAI_API_KEY` | Yes | OpenAI API key for GPT-4o model | `sk-...` |
| `STREAMLIT_SERVER_PORT` | No | Port for Streamlit dashboard | `8501` |
| `DB_FILE` | No | Path to SQLite database | `agents.db` |
| `LOG_LEVEL` | No | Logging verbosity (DEBUG, INFO, WARNING) | `INFO` |

### Agent Configuration

Agents can be customized by editing [app_agent.py](app_agent.py):

```python
# Adjust model
finance_agent = Agent(
    name="Finance Agent",
    model=OpenAIChat(id="gpt-4-turbo", api_key=api_key),  # Change model
    ...
)

# Customize instructions
finance_agent = Agent(
    instructions=[
        "Always cite data sources",
        "Provide conservative estimates",
        "Highlight key risks first",
    ],
    ...
)

# Enable/disable tools
finance_agent = Agent(
    tools=[
        YFinanceTools(include_tools=["get_current_stock_price", "get_company_info"]),
        # Add more tools as needed
    ],
    ...
)
```

### Database Persistence

The SQLite database (`agents.db`) stores:
- Agent conversation history
- Query execution logs
- Activity tracking

To reset:
```bash
rm agents.db  # Deletes all history
```

### API Rate Limits

- **OpenAI**: Check [platform.openai.com/account/rate-limits](https://platform.openai.com/account/rate-limits)
- **YFinance**: Generally unlimited for standard use
- **DuckDuckGo**: No official rate limits (respect terms of service)

---

## Limitations & Assumptions

### Data Availability Constraints

- **YFinance**: Limited to publicly traded securities with recent data
- **Web Search**: Dependent on public news coverage and indexing lag
- **Geographic**: Strong coverage for US markets; variable for international
- **Timeliness**: Real-time pricing is end-of-day for most retail-accessible data

### Market Dependency

- **Volatile Markets**: Recommendations may be stale in fast-moving conditions
- **Halted Securities**: No data available for trading halts or delisted companies
- **Corporate Actions**: Splits/dividends may cause data inconsistencies (YFinance delays)
- **After-Hours**: Pricing excludes extended-hours trading

### System Limitations

- **Context Window**: GPT-4 has fixed context length (~128K tokens)—very long analysis requests may be truncated
- **No Real-Time Execution**: System cannot execute trades or access account data
- **No Private Data**: Cannot access insider information, private filings, or confidential data
- **Training Data Cutoff**: Knowledge base has a cutoff date (check OpenAI documentation)

### Important Disclaimer

**⚠️ Not Financial Advice**

InvestifyAI is a research and analysis tool, not a financial advisor:

- Results are **not a personalized recommendation** for your specific situation
- You must consider your **personal risk tolerance, time horizon, and financial goals**
- Past performance does **not guarantee future results**
- Markets carry **inherent risks of loss of principal**
- All investing carries **opportunity cost** and **reinvestment risk**
- **Consult a qualified financial advisor** before making material portfolio changes

**No Liability**: The creators of InvestifyAI are not liable for investment losses, data inaccuracies, or reliance on recommendations.

---

## Future Roadmap

### Phase 2
- [ ] **Multi-Agent Consensus Scoring**: Agents vote on recommendations; higher confidence = stronger signal
- [ ] **Options Analysis Agent**: Greeks, volatility skew, earning announcements
- [ ] **Macro Intelligence Agent**: Fed decisions, employment data, yield curves
- [ ] **Extended History**: Full fundamental history for trend analysis

### Phase 3
- [ ] **Portfolio Backtesting**: Simulate historical recommendations on real portfolios
- [ ] **Risk Scenario Analysis**: Stress tests under various market conditions
- [ ] **Sentiment Analysis Agent**: Social media, earnings call transcripts
- [ ] **Custom Watchlist**: User-defined tracking with alerts

### Phase 4
- [ ] **International Markets**: Expanded coverage for ex-US equities and exchanges
- [ ] **Crypto/Digital Assets**: DeFi, token fundamentals, on-chain metrics
- [ ] **ESG & Sustainability**: Environmental, social, governance factor analysis
- [ ] **API and SDK**: Integration for third-party platforms and apps

### Long-Term Vision (2027+)
- [ ] **Autonomous Rebalancing**: Agent-driven portfolio optimization
- [ ] **Multi-Model Ensemble**: Combine multiple LLM providers for robustness
- [ ] **Real-Time Alerts**: Push notifications on high-conviction opportunities
- [ ] **Regulatory Compliance**: MiFID II, FINRA, and SEC alignment for institutional use

---

## Security & Data Handling

### API Key Security

- **Store locally only**: `.env` file never committed to version control
- **Rotate regularly**: Regenerate OpenAI keys every 90 days
- **Use minimal scope**: Limit key permissions to required APIs only
- **Monitor usage**: Check OpenAI dashboard for unusual activity

### User Data Privacy

- **No data collection**: InvestifyAI does not store user queries or personal information
- **Local processing**: All analysis happens locally; no external logging of queries
- **Ephemeral context**: Agent memory is session-based and cleared on restart
- **Optional persistence**: Users can opt out of SQLite history via configuration

### API Usage Practices

- **OpenAI**: Requests are logged by OpenAI per [API documentation](https://openai.com/policies/privacy-policy)
- **YFinance**: No authentication required; respects rate limits and terms
- **DuckDuckGo**: Search results are cached; respects user agent policies

**Compliance Notes**:
- This tool is for **personal research only** in current form
- **Not approved for institutional use** without modifications (logging, audit trails, compliance)
- **Consult legal/compliance** before deploying to production environments handling real capital

### Secure Deployment (Production)

For institutional or high-security deployments:

```python
# Use API gateway with authentication
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.post("/agents/query")
async def query_agents(
    query: str,
    credentials: HTTPAuthCredentials = Depends(security)
):
    # Verify JWT token
    # Log to audit trail
    # Encrypt response
    pass
```

---

## Contributing Guidelines

We welcome contributions from the community! Whether you're a developer, data scientist, or domain expert, here's how to help:

### Types of Contributions

- **New Agents**: Research, commodity analysis, crypto, ESG, etc.
- **Enhanced Tools**: Additional data sources, APIs, data enrichment
- **Improved UI**: Dashboard enhancements, new visualizations
- **Bug Fixes**: Issues found during testing
- **Documentation**: Better guides, tutorials, examples
- **Performance**: Optimization and efficiency improvements

### Code Standards

1. **Python Style**: Follow [PEP 8](https://pep8.org/)
2. **Type Hints**: All functions should have type annotations
3. **Docstrings**: Use Google-style docstrings for all classes/functions
4. **Testing**: Include unit tests for new features (minimum 80% coverage)
5. **Comments**: Explain complex logic; avoid obvious comments

### License Agreement

By contributing, you agree your code is licensed under the project's license (see below).

---

## License

InvestifyAI is licensed under the **MIT License**.

**You are free to:**
- Use commercially
- Modify the code
- Distribute
- Use privately

**Conditions:**
- Include license notice
- State significant changes

**Limitations:**
- No liability
- No warranty

See [LICENSE](LICENSE) for full text.

---

## Credits & Author

### Built By

**Alok Choudhary** — AI Engineer

### Acknowledgments

- **Agno Framework**: Multi-agent orchestration and collaboration
- **OpenAI**: GPT-4o language model and API
- **YFinance**: Financial data source
- **Streamlit**: Interactive dashboard framework
- **DuckDuckGo**: Search and web intelligence

---

**Last Updated**: February 3, 2026

---

*Built with ❤️ for the financial intelligence community.*
