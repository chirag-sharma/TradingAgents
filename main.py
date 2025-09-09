"""
TradingAgents Main Entry Point

This script demonstrates how to use the TradingAgents framework for both
US and Indian markets with proper configuration management.
"""

import os
from tradingagents.graph.trading_graph import TradingAgentsGraph

# Check if we should use Indian market configuration
market_type = os.getenv("TRADINGAGENTS_MARKET", "us").lower()

if market_type == "india":
    from tradingagents.indian_config import INDIAN_CONFIG
    base_config = INDIAN_CONFIG.copy()
else:
    from tradingagents.default_config import DEFAULT_CONFIG
    base_config = DEFAULT_CONFIG.copy()

# Create a custom config with environment-specific overrides
config = base_config.copy()
config["llm_provider"] = os.getenv("TRADINGAGENTS_LLM_PROVIDER", "google")
config["backend_url"] = os.getenv("TRADINGAGENTS_BACKEND_URL", "https://generativelanguage.googleapis.com/v1")
config["deep_think_llm"] = os.getenv("TRADINGAGENTS_DEEP_THINK_LLM", "gemini-2.0-flash")
config["quick_think_llm"] = os.getenv("TRADINGAGENTS_QUICK_THINK_LLM", "gemini-2.0-flash")
config["max_debate_rounds"] = int(os.getenv("TRADINGAGENTS_MAX_DEBATE_ROUNDS", "1"))
config["online_tools"] = os.getenv("TRADINGAGENTS_ONLINE_TOOLS", "true").lower() in ('true', '1', 'yes', 'on')

def main():
    """Main execution function."""
    
    print(f"Initializing TradingAgents for {market_type.upper()} market...")
    print(f"Using LLM Provider: {config['llm_provider']}")
    print(f"Online Tools: {'Enabled' if config['online_tools'] else 'Disabled'}")
    
    # Initialize with custom config
    ta = TradingAgentsGraph(debug=True, config=config)
    
    # Example ticker based on market
    if market_type == "india":
        ticker = "TCS"  # TCS for Indian market
        print(f"Analyzing Indian stock: {ticker}")
    else:
        ticker = "NVDA"  # NVIDIA for US market
        print(f"Analyzing US stock: {ticker}")
    
    # Forward propagate
    try:
        _, decision = ta.propagate(ticker, "2024-05-10")
        print("\n" + "="*50)
        print("TRADING DECISION:")
        print("="*50)
        print(decision)
        print("="*50)
        
        # Uncomment to enable reflection and memory
        # ta.reflect_and_remember(1000)  # parameter is the position returns
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        print("Please check your API keys and configuration.")

if __name__ == "__main__":
    main()
