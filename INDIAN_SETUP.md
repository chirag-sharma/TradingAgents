# Indian Market Trading Agents Setup Guide

This guide explains how to set up TradingAgents for analyzing Indian equities (NSE/BSE stocks).

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install all requirements including Indian market support
pip install -e .

# Or install from pyproject.toml
pip install .
```

### 2. Run the Example

```bash
python indian_example.py
```

## 📋 Features for Indian Markets

### ✅ Supported Features

1. **Indian Stock Data**: 
   - NSE and BSE stocks via Yahoo Finance
   - Automatic suffix handling (.NS, .BO)
   - INR currency support

2. **Technical Analysis**:
   - All standard indicators (RSI, MACD, Bollinger Bands)
   - Indian market context (vs Nifty performance)
   - Sector-specific analysis
   - Volatility and liquidity rankings

3. **Indian Financial News**:
   - Economic Times RSS feeds
   - Moneycontrol news
   - Business Standard
   - Live Mint
   - Company-specific news filtering

4. **Market Indices**:
   - Nifty 50, Sensex, Bank Nifty
   - Sector indices support
   - Market sentiment analysis

5. **Peer Comparison**:
   - Industry peer analysis
   - Financial ratios comparison
   - Sector leadership identification

### 🔧 Configuration

Edit `tradingagents/indian_config.py` to customize:

```python
INDIAN_CONFIG = {
    # Market settings
    "market": "india",
    "primary_exchange": "NSE",  # or "BSE"
    "currency": "INR",
    
    # Your API keys
    "indian_apis": {
        "alpha_vantage": {
            "api_key": "YOUR_API_KEY_HERE"
        }
    }
}
```

## 📊 Usage Examples

### Basic Stock Analysis

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.indian_config import INDIAN_CONFIG

# Configure for Indian market
config = INDIAN_CONFIG.copy()
config["llm_provider"] = "openai"
config["market"] = "india"

# Initialize
ta = TradingAgentsGraph(debug=True, config=config)

# Analyze Indian stock
final_state, decision = ta.propagate("RELIANCE", "2024-03-15")
print(f"Decision: {decision}")
```

### Major Indian Stocks Examples

```python
# NSE listed stocks
nse_stocks = [
    "RELIANCE",     # Reliance Industries
    "TCS",          # Tata Consultancy Services  
    "INFY",         # Infosys
    "HDFCBANK",     # HDFC Bank
    "ICICIBANK",    # ICICI Bank
    "HINDUNILVR",   # Hindustan Unilever
    "ITC",          # ITC Limited
    "KOTAKBANK",    # Kotak Mahindra Bank
    "LT",           # Larsen & Toubro
    "ASIANPAINT",   # Asian Paints
]

# BSE listed stocks (use .BO suffix or specify exchange="BSE")
bse_stocks = [
    "500325",       # Reliance (BSE code)
    "532540",       # TCS (BSE code)
]
```

## 🔌 Data Sources

### Supported Data Providers

1. **Yahoo Finance** (Primary)
   - Real-time stock prices
   - Historical data
   - Financial statements
   - Company information

2. **Indian News Sources**
   - Economic Times
   - Moneycontrol
   - Business Standard
   - Live Mint

3. **Optional Enhanced Data**
   - Alpha Vantage (with API key)
   - NSE/BSE APIs (when available)

### Data Coverage

- **Stock Data**: 2000+ NSE stocks, 5000+ BSE stocks
- **Indices**: Nifty 50, Sensex, Bank Nifty, Sector indices
- **News**: Real-time financial news from major Indian sources
- **Fundamentals**: P/E, P/B, market cap, financial ratios

## ⚙️ Agent Configuration

### Recommended Analyst Selection

For Indian stocks, consider these combinations:

```python
# Conservative analysis
selected_analysts = ["market", "fundamentals"]

# Comprehensive analysis  
selected_analysts = ["market", "social", "news", "fundamentals"]

# News-focused analysis
selected_analysts = ["news", "social", "fundamentals"]
```

### LLM Configuration

```python
# Cost-effective for testing
config["deep_think_llm"] = "gpt-4o-mini"
config["quick_think_llm"] = "gpt-4o-mini"

# Production quality
config["deep_think_llm"] = "gpt-4o"
config["quick_think_llm"] = "gpt-4o"
```

## 📈 Indian Market Specifics

### Trading Hours
- **Market Open**: 09:15 IST
- **Market Close**: 15:30 IST
- **Pre-market**: 09:00-09:15 IST
- **After-market**: 15:40-16:00 IST

### Major Sectors
- Information Technology
- Banking & Financial Services
- Oil & Gas
- Automobiles
- Pharmaceuticals
- FMCG (Fast Moving Consumer Goods)
- Metals & Mining
- Telecommunications

### Market Indices Context
- **Nifty 50**: Top 50 companies by market cap
- **Sensex**: 30 largest companies on BSE
- **Bank Nifty**: Banking sector index
- **Nifty IT**: IT sector index

## 🔧 Troubleshooting

### Common Issues

1. **"Indian market modules not available"**
   ```bash
   pip install -e .
   ```

2. **No data for stock symbol**
   - Verify symbol is correct (e.g., "RELIANCE" not "RIL")
   - Check if stock is listed on specified exchange
   - Try different date (avoid weekends/holidays)

3. **News sources not working**
   - Check internet connection
   - Some RSS feeds may be temporarily unavailable
   - Try different news sources

4. **Slow performance**
   - Reduce `lookback_days` parameter
   - Use fewer analysts in `selected_analysts`
   - Use lighter LLM models for testing

### API Keys Setup

1. **Alpha Vantage** (Optional, for enhanced data)
   ```python
   config["indian_apis"]["alpha_vantage"]["api_key"] = "YOUR_KEY"
   ```

2. **OpenAI API** (Required for LLM)
   ```bash
   export OPENAI_API_KEY="your_openai_key"
   ```

## 🎯 Next Steps

1. **Install dependencies**: `pip install -e .`
2. **Run example**: `python indian_example.py`
3. **Customize config**: Edit `indian_config.py`
4. **Try different stocks**: Modify the example script
5. **Integrate with your workflow**: Use the API in your applications

## 🤝 Contributing

To improve Indian market support:

1. Add more Indian data sources
2. Enhance news sentiment analysis for Hindi/regional languages
3. Add NSE/BSE specific indicators
4. Improve sector classification
5. Add support for F&O (Futures & Options) data

## ⚠️ Disclaimer

This framework is for research and educational purposes. Trading decisions should not be based solely on AI analysis. Always:

- Conduct your own research
- Consider market risks
- Consult financial advisors
- Comply with Indian securities regulations (SEBI guidelines)

## 📞 Support

For Indian market specific issues:
1. Check this README
2. Review the example scripts
3. Test with major stocks like RELIANCE, TCS
4. Ensure all dependencies are installed
