<p align="center">
  <img src="assets/TauricResearch.png" style="width: 60%; height: auto;">
</p>

<div align="center" style="line-height: 1;">
  <a href="https://arxiv.org/abs/2412.20138" target="_blank"><img alt="arXiv" src="https://img.shields.io/badge/arXiv-2412.20138-B31B1B?logo=arxiv"/></a>
  <a href="https://discord.com/invite/hk9PGKShPK" target="_blank"><img alt="Discord" src="https://img.shields.io/badge/Discord-TradingResearch-7289da?logo=discord&logoColor=white&color=7289da"/></a>
  <a href="./assets/wechat.png" target="_blank"><img alt="WeChat" src="https://img.shields.io/badge/WeChat-TauricResearch-brightgreen?logo=wechat&logoColor=white"/></a>
  <a href="https://x.com/TauricResearch" target="_blank"><img alt="X Follow" src="https://img.shields.io/badge/X-TauricResearch-white?logo=x&logoColor=white"/></a>
  <br>
  <a href="https://github.com/TauricResearch/" target="_blank"><img alt="Community" src="https://img.shields.io/badge/Join_GitHub_Community-TauricResearch-14C290?logo=discourse"/></a>
</div>

<div align="center">
  <!-- Keep these links. Translations will automatically update with the README. -->
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=de">Deutsch</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=es">Español</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=fr">français</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=ja">日本語</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=ko">한국어</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=pt">Português</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=ru">Русский</a> | 
  <a href="https://www.readme-i18n.com/TauricResearch/TradingAgents?lang=zh">中文</a>
</div>

---

# TradingAgents: Multi-Agents LLM Financial Trading Framework 

> 🎉 **TradingAgents** officially released! We have received numerous inquiries about the work, and we would like to express our thanks for the enthusiasm in our community.

**TradingAgents** is a comprehensive multi-agent framework for financial trading that leverages Large Language Models (LLMs) to provide intelligent market analysis and trading decisions. The framework supports both **US** and **Indian** equity markets with sophisticated agent-based collaboration.

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Valid API keys for your chosen LLM provider (OpenAI, Google, Anthropic)
- Optional: Additional API keys for enhanced data sources

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/TauricResearch/TradingAgents.git
   cd TradingAgents
   ```

2. **Install dependencies:**
   ```bash
   pip install -e .
   ```

3. **🔑 Configure API Keys (Required):**

   **Option A: Environment Variables (Recommended)**
   ```bash
   # Choose ONE LLM provider:
   
   # OpenAI (GPT-4, etc.)
   export OPENAI_API_KEY="sk-your-openai-api-key-here"
   export TRADINGAGENTS_LLM_PROVIDER="openai"
   
   # OR Google Gemini
   export GOOGLE_API_KEY="your-google-api-key-here" 
   export TRADINGAGENTS_LLM_PROVIDER="google"
   
   # OR Anthropic Claude
   export ANTHROPIC_API_KEY="sk-ant-your-anthropic-api-key-here"
   export TRADINGAGENTS_LLM_PROVIDER="anthropic"
   
   # Market selection
   export TRADINGAGENTS_MARKET="us"  # or "india"
   ```

   **Option B: Use Setup Script**
   ```bash
   # Copy and customize the environment setup
   cp setup_env.sh my_setup.sh
   # Edit my_setup.sh with your API keys
   source my_setup.sh
   ```

   **Option C: .env File**
   ```bash
   # Copy the example and fill in your keys
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **🔍 Validate Setup:**
   ```bash
   python validate_setup.py
   ```

### Basic Usage

**For US Markets:**
```bash
export TRADINGAGENTS_MARKET="us"
python main.py
```

**For Indian Markets:**
```bash
export TRADINGAGENTS_MARKET="india"
python main.py
```

**Using the CLI:**
```bash
python -m cli.main
```

## 🔑 **Where to Get API Keys**

| Provider | Free Tier | Get API Key | Notes |
|----------|-----------|-------------|-------|
| **OpenAI** | $5 credit | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) | Best for GPT-4o models |
| **Google** | Free tier available | [makersuite.google.com](https://makersuite.google.com/app/apikey) | Best for Gemini models |
| **Anthropic** | $5 credit | [console.anthropic.com](https://console.anthropic.com/) | Best for Claude models |
| **Finnhub** | Free tier: 60 calls/min | [finnhub.io](https://finnhub.io/dashboard) | Financial data (optional) |
| **Alpha Vantage** | Free tier: 25 calls/day | [alphavantage.co](https://www.alphavantage.co/support/#api-key) | Market data (optional) |

**Using the CLI:**
```bash
python -m cli.main
```

## ⚙️ Configuration

TradingAgents uses a unified configuration system that supports multiple markets and deployment scenarios.

### Environment Variables

| Variable | Description | Default | Options |
|----------|-------------|---------|---------|
| `TRADINGAGENTS_MARKET` | Target market | `us` | `us`, `india` |
| `TRADINGAGENTS_LLM_PROVIDER` | LLM provider | `openai` | `openai`, `google`, `anthropic`, `ollama` |
| `TRADINGAGENTS_ONLINE_TOOLS` | Enable online data | `true` | `true`, `false` |
| `TRADINGAGENTS_MAX_DEBATE_ROUNDS` | Agent debate rounds | `1` | Any positive integer |
| `TRADINGAGENTS_DATA_DIR` | Data storage directory | `./data` | Any valid path |

### Market-Specific Configuration

**US Market Features:**
- Yahoo Finance integration
- Finnhub data sources  
- Reddit sentiment analysis
- SEC filings analysis

**Indian Market Features:**
- NSE/BSE stock data
- Indian financial news (Economic Times, MoneyControl)
- Indian market indices (Nifty 50, Sensex, Bank Nifty)
- Sector-specific analysis

## 🏗️ Architecture

The framework employs a sophisticated multi-agent architecture:

### Core Agents

1. **Market Analysts** - Technical and fundamental analysis
2. **News Analysts** - News sentiment and impact analysis  
3. **Social Media Analysts** - Social sentiment tracking
4. **Fundamental Analysts** - Company financials and valuation
5. **Bull/Bear Researchers** - Debate-based decision making
6. **Risk Managers** - Portfolio risk assessment
7. **Traders** - Final execution decisions

### Workflow

```
Input (Ticker + Date) → Analysts → Researchers → Risk Assessment → Trading Decision
```

## 🛠️ Recent Improvements

### Fixed Issues ✅
- ✅ **Class naming conflicts** - Standardized `StockstatsUtils` across all modules
- ✅ **Configuration management** - Unified config system with environment support
- ✅ **Import issues** - Removed duplicate imports and wildcard imports
- ✅ **Error handling** - Proper exception handling with logging
- ✅ **Hardcoded paths** - Environment-based path configuration

### Enhanced Features ✅
- ✅ **Market-agnostic main.py** - Automatic US/Indian market detection
- ✅ **Robust error handling** - Comprehensive retry and fallback mechanisms
- ✅ **Type safety** - Improved type hints and validation
- ✅ **Logging system** - Centralized logging with configurable levels
>
> So we decided to fully open-source the framework. Looking forward to building impactful projects with you!

<div align="center">
<a href="https://www.star-history.com/#TauricResearch/TradingAgents&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=TauricResearch/TradingAgents&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=TauricResearch/TradingAgents&type=Date" />
   <img alt="TradingAgents Star History" src="https://api.star-history.com/svg?repos=TauricResearch/TradingAgents&type=Date" style="width: 80%; height: auto;" />
 </picture>
</a>
</div>

<div align="center">

🚀 [TradingAgents](#tradingagents-framework) | ⚡ [Installation & CLI](#installation-and-cli) | 🎬 [Demo](https://www.youtube.com/watch?v=90gr5lwjIho) | 📦 [Package Usage](#tradingagents-package) | 🤝 [Contributing](#contributing) | 📄 [Citation](#citation)

</div>

## TradingAgents Framework

TradingAgents is a multi-agent trading framework that mirrors the dynamics of real-world trading firms. By deploying specialized LLM-powered agents: from fundamental analysts, sentiment experts, and technical analysts, to trader, risk management team, the platform collaboratively evaluates market conditions and informs trading decisions. Moreover, these agents engage in dynamic discussions to pinpoint the optimal strategy.

<p align="center">
  <img src="assets/schema.png" style="width: 100%; height: auto;">
</p>

> TradingAgents framework is designed for research purposes. Trading performance may vary based on many factors, including the chosen backbone language models, model temperature, trading periods, the quality of data, and other non-deterministic factors. [It is not intended as financial, investment, or trading advice.](https://tauric.ai/disclaimer/)

Our framework decomposes complex trading tasks into specialized roles. This ensures the system achieves a robust, scalable approach to market analysis and decision-making.

### Analyst Team
- Fundamentals Analyst: Evaluates company financials and performance metrics, identifying intrinsic values and potential red flags.
- Sentiment Analyst: Analyzes social media and public sentiment using sentiment scoring algorithms to gauge short-term market mood.
- News Analyst: Monitors global news and macroeconomic indicators, interpreting the impact of events on market conditions.
- Technical Analyst: Utilizes technical indicators (like MACD and RSI) to detect trading patterns and forecast price movements.

<p align="center">
  <img src="assets/analyst.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

### Researcher Team
- Comprises both bullish and bearish researchers who critically assess the insights provided by the Analyst Team. Through structured debates, they balance potential gains against inherent risks.

<p align="center">
  <img src="assets/researcher.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

### Trader Agent
- Composes reports from the analysts and researchers to make informed trading decisions. It determines the timing and magnitude of trades based on comprehensive market insights.

<p align="center">
  <img src="assets/trader.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

### Risk Management and Portfolio Manager
- Continuously evaluates portfolio risk by assessing market volatility, liquidity, and other risk factors. The risk management team evaluates and adjusts trading strategies, providing assessment reports to the Portfolio Manager for final decision.
- The Portfolio Manager approves/rejects the transaction proposal. If approved, the order will be sent to the simulated exchange and executed.

<p align="center">
  <img src="assets/risk.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

## Installation and CLI

### Installation

Clone TradingAgents:
```bash
git clone https://github.com/TauricResearch/TradingAgents.git
cd TradingAgents
```

Create a virtual environment in any of your favorite environment managers:
```bash
conda create -n tradingagents python=3.13
conda activate tradingagents
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### Required APIs

You will also need the FinnHub API for financial data. All of our code is implemented with the free tier.
```bash
export FINNHUB_API_KEY=$YOUR_FINNHUB_API_KEY
```

You will need the OpenAI API for all the agents.
```bash
export OPENAI_API_KEY=$YOUR_OPENAI_API_KEY
```

### CLI Usage

You can also try out the CLI directly by running:
```bash
python -m cli.main
```
You will see a screen where you can select your desired tickers, date, LLMs, research depth, etc.

<p align="center">
  <img src="assets/cli/cli_init.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

An interface will appear showing results as they load, letting you track the agent's progress as it runs.

<p align="center">
  <img src="assets/cli/cli_news.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

<p align="center">
  <img src="assets/cli/cli_transaction.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

## TradingAgents Package

### Implementation Details

We built TradingAgents with LangGraph to ensure flexibility and modularity. We utilize `o1-preview` and `gpt-4o` as our deep thinking and fast thinking LLMs for our experiments. However, for testing purposes, we recommend you use `o4-mini` and `gpt-4.1-mini` to save on costs as our framework makes **lots of** API calls.

### Python Usage

To use TradingAgents inside your code, you can import the `tradingagents` module and initialize a `TradingAgentsGraph()` object. The `.propagate()` function will return a decision. You can run `main.py`, here's also a quick example:

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())

# forward propagate
_, decision = ta.propagate("NVDA", "2024-05-10")
print(decision)
```

You can also adjust the default configuration to set your own choice of LLMs, debate rounds, etc.

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Create a custom config
config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "gpt-4.1-nano"  # Use a different model
config["quick_think_llm"] = "gpt-4.1-nano"  # Use a different model
config["max_debate_rounds"] = 1  # Increase debate rounds
config["online_tools"] = True # Use online tools or cached data

# Initialize with custom config
ta = TradingAgentsGraph(debug=True, config=config)

# forward propagate
_, decision = ta.propagate("NVDA", "2024-05-10")
print(decision)
```

> For `online_tools`, we recommend enabling them for experimentation, as they provide access to real-time data. The agents' offline tools rely on cached data from our **Tauric TradingDB**, a curated dataset we use for backtesting. We're currently in the process of refining this dataset, and we plan to release it soon alongside our upcoming projects. Stay tuned!

You can view the full list of configurations in `tradingagents/default_config.py`.

## Contributing

We welcome contributions from the community! Whether it's fixing a bug, improving documentation, or suggesting a new feature, your input helps make this project better. If you are interested in this line of research, please consider joining our open-source financial AI research community [Tauric Research](https://tauric.ai/).

## Citation

Please reference our work if you find *TradingAgents* provides you with some help :)

```
@misc{xiao2025tradingagentsmultiagentsllmfinancial,
      title={TradingAgents: Multi-Agents LLM Financial Trading Framework}, 
      author={Yijia Xiao and Edward Sun and Di Luo and Wei Wang},
      year={2025},
      eprint={2412.20138},
      archivePrefix={arXiv},
      primaryClass={q-fin.TR},
      url={https://arxiv.org/abs/2412.20138}, 
}
```
