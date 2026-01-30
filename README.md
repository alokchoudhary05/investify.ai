# InvestifyAI - Intelligent Financial Agent Platform

A production-ready multi-agent AI system for advanced financial analysis, real-time market intelligence, and personalized investment insights.

## 🌟 Product Overview

InvestifyAI leverages cutting-edge AI technology to provide institutional-grade financial intelligence. Our platform combines multiple intelligent agents working in concert to deliver comprehensive market analysis, deep stock research, and strategic investment recommendations.

**Key Capabilities:**
- 📊 Real-time market data analysis
- 🤖 Multi-agent AI collaboration
- 🔬 Deep fundamental research
- 💼 Portfolio strategy optimization
- ⚡ Risk assessment and alerts
- 🌍 Global market coverage

## 🏗️ Architecture

### Core Components

#### 1. **Multi-Agent System**
- **Market Pulse Agent**: Monitors global market trends and identifies opportunities
- **Deep Research Agent**: Performs in-depth analysis on individual securities
- **Portfolio Strategist**: Provides strategic recommendations for wealth building
- **Risk Intelligence Agent**: Analyzes market volatility and risk factors

#### 2. **Data Sources**
- **YFinance Integration**: Real-time stock data, historical prices, company fundamentals
- **Web Search Capability**: Market news, economic indicators, emerging trends
- **Market Indices**: Indian indices (NIFTY, SENSEX), US indices (S&P, NASDAQ, DOW), global markets
- **Commodities Data**: Gold, Oil, and other commodity prices

#### 3. **Technology Stack**

**Backend:**
- Python 3.11+
- Agno (Multi-agent framework)
- FastAPI (Web framework)
- SQLAlchemy (ORM)

**Frontend:**
- Streamlit (Interactive dashboard)
- Plotly (Advanced charting)

**AI/ML:**
- OpenAI GPT-4 (Language model)
- LangChain (LLM orchestration)

**Data Processing:**
- Pandas (Data manipulation)
- NumPy (Numerical computing)
- YFinance (Financial data)
- DuckDuckGo (Web search)

**Infrastructure:**
- SQLite (Local database)
- Python-dotenv (Environment management)

### System Architecture

```
┌─────────────────────────────────────────────┐
│         Streamlit Dashboard (Frontend)      │
│  - API Key Setup Screen                     │
│  - Market Intelligence View                 │
│  - Agent Insights Chat                      │
│  - Stock Intelligence Research              │
└────────────────────┬────────────────────────┘
                     │
┌────────────────────▼────────────────────────┐
│     Agent Handler (Orchestration Layer)     │
│  - Routes user queries to agents            │
│  - Manages response formatting              │
│  - Handles error management                 │
└────────┬──────────────────────────┬─────────┘
         │                          │
    ┌────▼──────────────┐  ┌───────▼──────────┐
    │  Intelligence     │  │   Data Fetchers  │
    │  Agents (Agno)    │  │                  │
    │                   │  ├─ MarketDataFetcher
    ├─ Market Pulse     │  ├─ YFinance API   │
    ├─ Deep Research    │  ├─ Web Search     │
    ├─ Portfolio        │  └─ Stock Database │
    │  Strategist       │                    │
    └─────┬──────────────┘  └──────┬──────────┘
          │                        │
          └────────────┬───────────┘
                       │
            ┌──────────▼───────────┐
            │   OpenAI GPT-4       │
            │   Language Model     │
            └──────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- OpenAI API key (required for production)
- Virtual environment (recommended)

### Installation Steps

#### 1. Clone and Setup Environment
```bash
# Create virtual environment
python -m venv myenv

# Activate virtual environment
# Windows:
myenv\Scripts\activate
# macOS/Linux:
source myenv/bin/activate
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Run the Dashboard
```bash
streamlit run dashboard.py
```

**First Launch:** When you open the dashboard for the first time, you'll be prompted to enter your OpenAI API key through a secure setup screen.

**To obtain an OpenAI API key:**
1. Visit [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create a new API key
3. Enter it in the dashboard setup screen
4. Enjoy full access to all InvestifyAI features

## 📖 Usage Guide

### Dashboard Views

#### 📈 Market Intelligence
- View real-time market indices (Indian, US, Global)
- Monitor commodity prices
- See active intelligence agents
- Track market movements

#### 🤖 Agent Insights
- Chat interface with intelligent agents
- Ask questions about stocks, markets, or investments
- Get AI-powered analysis and recommendations
- View conversation history

#### 📋 Stock Intelligence
- Search stocks by ticker or company name
- View detailed company information
- Analyze price charts and trends
- Review key financial metrics
- Access fundamentals data

### Dashboard Features

**Navigation:**
- Easy-to-use sidebar for switching between views
- Automatic refresh options (5, 10, 15 minutes or manual)
- Show/hide agent details and advanced metrics

**Settings:**
- Customize your analysis preferences
- View about information
- Access help and documentation

## 🛠️ Configuration

### API Key Setup
The application uses a secure setup screen for API key input:
1. Launch the dashboard
2. You'll be redirected to the setup screen
3. Enter your OpenAI API key
4. Click "Verify & Continue"
5. Full dashboard access granted

**Security:** API keys are held only in memory during the session and never persisted to disk.

### Backend Server (Optional)
For programmatic API access, run the FastAPI server:
```bash
python app_agent.py
```

The server provides RESTful endpoints and auto-documentation at `/docs`.

## 📊 Key Features

### Intelligence Agents

**1. Market Pulse Agent**
- Analyzes global market trends
- Identifies emerging opportunities
- Monitors sector rotation
- Tracks economic indicators

**2. Deep Research Agent**
- Company fundamental analysis
- Competitive positioning
- Financial health assessment
- Valuation analysis

**3. Portfolio Strategist**
- Asset allocation recommendations
- Diversification suggestions
- Risk-adjusted returns analysis
- Strategy optimization

**4. Risk Intelligence Agent**
- Volatility analysis
- Drawdown assessment
- Portfolio risk metrics
- Market stress testing

### Market Data Coverage

- **Indian Markets**: NIFTY 50, SENSEX, sectoral indices
- **US Markets**: S&P 500, NASDAQ, DOW JONES
- **Global Markets**: FTSE 100, DAX, Nikkei 225
- **Commodities**: Gold, Crude Oil, Natural Gas
- **Individual Stocks**: Support for 50,000+ securities

## 🔐 Security

- **API Key Protection**: Keys held in memory only, never persisted to disk
- **Session-Based**: Secure session management
- **HTTPS Ready**: Compatible with secure deployments
- **Data Privacy**: No data sharing beyond OpenAI
- **Access Control**: User-based session isolation

## 📦 Project Structure

```
InvestifyAI/
├── dashboard.py              # Streamlit frontend application
├── app_agent.py             # FastAPI backend server
├── agent_handler.py         # Multi-agent orchestration
├── market_data.py           # Data fetching and processing
├── logger.py                # Logging configuration
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (not in repo)
├── .gitignore               # Git ignore rules
├── README.md                # This file
└── logs/                    # Application logs
```

## 🔧 Development

### Logging
Application logs are automatically saved to `logs/` directory. Check logs for debugging and monitoring.

### Testing
To verify your setup:
```bash
python test_setup.py
```

## 🌍 Deployment

### Production Checklist
- [ ] Use strong API keys
- [ ] Configure HTTPS for secure connections
- [ ] Set up monitoring and alerts
- [ ] Implement rate limiting for API endpoints
- [ ] Enable CORS for cross-origin requests

### Deployment Options
- **Local**: Run on personal machine or office server
- **Cloud**: Deploy to AWS, Google Cloud, or Azure
- **Docker**: Containerized deployment ready

## 📊 Monitoring

The application logs important events for monitoring:
- Agent queries and responses
- Data fetch operations
- System errors and exceptions
- Performance metrics

Check `logs/` directory for detailed logs.

## 📝 Dependencies

### Core Framework
- **agno** (2.4.2): Multi-agent framework
- **openai**: GPT-4 integration
- **fastapi** (0.128.0): Web framework
- **uvicorn**: ASGI server
- **streamlit**: Dashboard framework

### Data Processing
- **pandas**: Data manipulation
- **numpy**: Numerical computing
- **yfinance**: Financial data
- **duckduckgo-search** (8.1.1): Web search

### Utilities
- **python-dotenv**: Environment variables
- **sqlalchemy**: ORM
- **plotly** (5.22.0): Charting library
- **beautifulsoup4** (4.14.3): HTML parsing

For complete dependency list, see `requirements.txt`.

## 🎯 Roadmap

**Upcoming Features:**
- Portfolio tracking and management
- Automated trading signals
- Mobile app (iOS/Android)
- Advanced ML models
- Real-time alerts and notifications
- Backtesting framework

## 🙏 Built With

- OpenAI for GPT-4 language model
- YFinance for financial data
- Streamlit for interactive interfaces
- Agno framework for multi-agent orchestration

---

**InvestifyAI** - Your Intelligent Financial Agent Platform
*Make smarter investment decisions powered by AI*
