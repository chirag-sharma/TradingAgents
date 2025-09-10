# 🔑 TradingAgents API Key Configuration Guide

## 📍 **Where to Provide API Keys**

### **Option 1: Environment Variables (Recommended) 🌟**

Set environment variables in your terminal:

```bash
# Choose ONE LLM provider:

# OpenAI (Best for GPT-4 models)
export OPENAI_API_KEY="sk-your-openai-api-key-here"
export TRADINGAGENTS_LLM_PROVIDER="openai"

# OR Google (Best for Gemini models, has free tier)
export GOOGLE_API_KEY="your-google-api-key-here"
export TRADINGAGENTS_LLM_PROVIDER="google"

# OR Anthropic (Best for Claude models)  
export ANTHROPIC_API_KEY="sk-ant-your-anthropic-api-key-here"
export TRADINGAGENTS_LLM_PROVIDER="anthropic"

# Market selection
export TRADINGAGENTS_MARKET="india"  # or "us"
```

### **Option 2: Setup Script 📜**

Use the provided setup script:

```bash
# Copy the setup template
cp setup_env.sh my_setup.sh

# Edit my_setup.sh and add your API keys
nano my_setup.sh  # or use any editor

# Load the environment
source my_setup.sh
```

### **Option 3: .env File 📄**

Create a `.env` file for automatic loading:

```bash
# Copy the example
cp .env.example .env

# Edit .env with your API keys
nano .env

# The framework will automatically load these
```

### **Option 4: Direct in Code 💻**

Set API keys programmatically:

```python
import os
from tradingagents.graph.trading_graph import TradingAgentsGraph

# Set API key in code
os.environ["OPENAI_API_KEY"] = "sk-your-key-here"
os.environ["TRADINGAGENTS_LLM_PROVIDER"] = "openai"
os.environ["TRADINGAGENTS_MARKET"] = "us"

# Initialize TradingAgents
ta = TradingAgentsGraph(debug=True)
```

## 🔗 **Where to Get API Keys**

| Provider | Cost | URL | Notes |
|----------|------|-----|-------|
| **OpenAI** | $5 free credit | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) | GPT-4o, GPT-4o-mini |
| **Google** | Free tier available | [makersuite.google.com](https://makersuite.google.com/app/apikey) | Gemini Pro, Gemini Flash |
| **Anthropic** | $5 free credit | [console.anthropic.com](https://console.anthropic.com/) | Claude 3.5 Sonnet, Claude 3 Haiku |
| **Finnhub** | 60 calls/min free | [finnhub.io/dashboard](https://finnhub.io/dashboard) | Financial data (optional) |
| **Alpha Vantage** | 25 calls/day free | [alphavantage.co](https://www.alphavantage.co/support/#api-key) | Market data (optional) |

## ✅ **Verification Tools**

Check your setup:

```bash
# Quick API key status check
python check_api_keys.py

# Full validation (dependencies, imports, config)
python validate_setup.py
```

## 🚀 **Quick Start Examples**

### **Indian Market with OpenAI (Default)**
```bash
export OPENAI_API_KEY="sk-your-key"
export TRADINGAGENTS_LLM_PROVIDER="openai"
export TRADINGAGENTS_MARKET="india"
python main.py
```

### **US Market with Google**
```bash
export GOOGLE_API_KEY="your-key"
export TRADINGAGENTS_LLM_PROVIDER="google" 
export TRADINGAGENTS_MARKET="us"
python main.py
```

### **CLI Interface**
```bash
# Set your API keys first, then:
python -m cli.main
```

## 🛠️ **Troubleshooting**

### **API Key Not Working?**
- ✅ Check the format (OpenAI keys start with `sk-`, Anthropic with `sk-ant-`)
- ✅ Verify the key is active in your provider dashboard
- ✅ Check billing/quota limits
- ✅ Run `python check_api_keys.py` to verify configuration

### **Import Errors?**
- ✅ Run `pip install -e .` to install dependencies
- ✅ Run `python validate_setup.py` for full diagnosis

### **Market-Specific Issues?**
- ✅ For Indian markets, set `TRADINGAGENTS_MARKET="india"`
- ✅ Indian analysis works best with Google Gemini (free tier available)
- ✅ US markets work well with all providers

## 📁 **Configuration Files Reference**

```
TradingAgents/
├── .env.example          # Template for .env file
├── setup_env.sh          # Shell script template  
├── check_api_keys.py     # API key status checker
├── validate_setup.py     # Full system validation
├── config_examples.py    # Advanced configuration examples
└── example_api_setup.py  # Programmatic setup examples
```

## 💡 **Best Practices**

1. **Start with Google Gemini** - has the most generous free tier
2. **Use environment variables** - more secure than hardcoding
3. **Run validation first** - `python validate_setup.py`
4. **Check API limits** - monitor your usage in provider dashboards
5. **Optional APIs enhance functionality** - but aren't required to start

---

**Need help?** Run `python check_api_keys.py` for personalized setup guidance!
