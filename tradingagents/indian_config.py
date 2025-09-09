import os

# Indian Market Configuration for TradingAgents
INDIAN_CONFIG = {
    "project_dir": os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
    "results_dir": os.getenv("TRADINGAGENTS_RESULTS_DIR", "./results"),
    "data_dir": "/Users/chirag/VsCodeProjects/TradingAgents/indian_data",
    "data_cache_dir": os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
        "dataflows/data_cache",
    ),
    
    # Market-specific settings
    "market": "india",
    "primary_exchange": "NSE",  # NSE or BSE
    "secondary_exchange": "BSE",
    "currency": "INR",
    "market_timezone": "Asia/Kolkata",
    
    # Trading hours (IST)
    "market_open": "09:15",
    "market_close": "15:30",
    
    # LLM settings
    "llm_provider": "openai",
    "deep_think_llm": "gpt-4o-mini",
    "quick_think_llm": "gpt-4o-mini",
    "backend_url": "https://api.openai.com/v1",
    
    # Debate and discussion settings
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
    "max_recur_limit": 100,
    
    # Tool settings
    "online_tools": True,
    
    # Indian-specific API configurations
    "indian_apis": {
        "alpha_vantage": {
            "api_key": "",  # User will provide
            "base_url": "https://www.alphavantage.co/query"
        },
        "nse_tools": {
            "enabled": True,
            "base_url": "https://www.nseindia.com/api"
        },
        "economic_times": {
            "enabled": True,
            "rss_feeds": [
                "https://economictimes.indiatimes.com/markets/stocks/rssfeeds/2146842.cms",
                "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms"
            ]
        },
        "moneycontrol": {
            "enabled": True,
            "base_url": "https://www.moneycontrol.com"
        },
        "yahoofinance_india": {
            "suffix": ".NS",  # NSE suffix for Yahoo Finance
            "bse_suffix": ".BO"  # BSE suffix for Yahoo Finance
        }
    },
    
    # Indian market indices for context
    "market_indices": {
        "nifty50": "^NSEI",
        "sensex": "^BSESN",
        "banknifty": "^NSEBANK",
        "nifty_it": "^CNXIT",
        "nifty_pharma": "^CNXPHARMA"
    },
    
    # Common Indian stock suffixes
    "stock_suffixes": {
        "nse": ".NS",
        "bse": ".BO"
    }
}
