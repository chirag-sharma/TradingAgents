"""
Example: Direct API Key Configuration in Code

This shows how to configure API keys programmatically if you prefer
not to use environment variables.
"""

import os
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.indian_config import INDIAN_CONFIG

def setup_with_api_keys():
    """Example of setting up TradingAgents with API keys in code."""
    
    # Method 1: Set environment variables in code
    os.environ["OPENAI_API_KEY"] = "your-openai-api-key-here"
    # OR
    # os.environ["GOOGLE_API_KEY"] = "your-google-api-key-here"
    # OR
    # os.environ["ANTHROPIC_API_KEY"] = "your-anthropic-api-key-here"
    
    # Choose your configuration
    market_type = "us"  # or "india"
    
    if market_type == "india":
        config = INDIAN_CONFIG.copy()
    else:
        config = DEFAULT_CONFIG.copy()
    
    # Configure LLM provider
    config.update({
        "llm_provider": "openai",  # or "google", "anthropic"
        "deep_think_llm": "gpt-4o-mini",
        "quick_think_llm": "gpt-4o-mini",
        "backend_url": "https://api.openai.com/v1",
        "online_tools": True,
        "max_debate_rounds": 1
    })
    
    # Initialize TradingAgents
    ta = TradingAgentsGraph(debug=True, config=config)
    
    return ta

def example_usage():
    """Example usage with different configurations."""
    
    # For US markets with OpenAI
    print("Setting up for US markets with OpenAI...")
    os.environ["OPENAI_API_KEY"] = "your-openai-key"
    os.environ["TRADINGAGENTS_MARKET"] = "us"
    os.environ["TRADINGAGENTS_LLM_PROVIDER"] = "openai"
    
    # For Indian markets with Google
    print("Setting up for Indian markets with Google...")
    os.environ["GOOGLE_API_KEY"] = "your-google-key"
    os.environ["TRADINGAGENTS_MARKET"] = "india"
    os.environ["TRADINGAGENTS_LLM_PROVIDER"] = "google"
    
    # Additional data source APIs (optional)
    os.environ["FINNHUB_API_KEY"] = "your-finnhub-key"
    os.environ["ALPHA_VANTAGE_API_KEY"] = "your-alpha-vantage-key"

if __name__ == "__main__":
    # Uncomment and modify with your actual API keys
    # ta = setup_with_api_keys()
    # result = ta.propagate("AAPL", "2024-01-15")
    # print(result)
    
    print("Please add your API keys to the functions above and uncomment the code to run.")
    print("\n🔑 API Key Locations:")
    print("- OpenAI: https://platform.openai.com/api-keys")
    print("- Google: https://makersuite.google.com/app/apikey")  
    print("- Anthropic: https://console.anthropic.com/")
    print("- Finnhub: https://finnhub.io/dashboard")
    print("- Alpha Vantage: https://www.alphavantage.co/support/#api-key")
