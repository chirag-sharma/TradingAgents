"""
TradingAgents Main Entry Point

This script automatically detects available LLM providers and configures
the framework for both US and Indian markets with intelligent fallbacks.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from tradingagents.graph.trading_graph import TradingAgentsGraph

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
if env_path.exists():
    load_dotenv(env_path)
    print(f"🔧 Loaded configuration from .env file")

def detect_available_llm_provider():
    """
    Automatically detect which LLM provider is available based on API keys.
    Returns the best available provider with appropriate configuration.
    """
    
    providers = {
        "openai": {
            "env_key": "OPENAI_API_KEY",
            "backend_url": "https://api.openai.com/v1",
            "deep_model": "gpt-4o-mini",
            "quick_model": "gpt-4o-mini",
            "priority": 1  # Higher priority
        },
        "google": {
            "env_key": "GOOGLE_API_KEY", 
            "backend_url": "https://generativelanguage.googleapis.com/v1",
            "deep_model": "gemini-2.0-flash",
            "quick_model": "gemini-2.0-flash",
            "priority": 2
        },
        "anthropic": {
            "env_key": "ANTHROPIC_API_KEY",
            "backend_url": "https://api.anthropic.com",
            "deep_model": "claude-3-sonnet-20240229",
            "quick_model": "claude-3-haiku-20240307", 
            "priority": 3
        }
    }
    
    # Check for manually specified provider first
    manual_provider = os.getenv("TRADINGAGENTS_LLM_PROVIDER")
    if manual_provider and manual_provider in providers:
        if os.getenv(providers[manual_provider]["env_key"]):
            print(f"✅ Using manually specified provider: {manual_provider.upper()}")
            return manual_provider, providers[manual_provider]
        else:
            print(f"⚠️  Specified provider {manual_provider} has no API key, auto-detecting...")
    
    # Auto-detect based on available API keys
    available_providers = []
    for provider, config in providers.items():
        if os.getenv(config["env_key"]):
            available_providers.append((provider, config))
            print(f"🔍 Found API key for: {provider.upper()}")
    
    if not available_providers:
        raise ValueError(
            "❌ No LLM provider API keys found!\n"
            "Please set one of these environment variables:\n"
            "- OPENAI_API_KEY\n"
            "- GOOGLE_API_KEY\n" 
            "- ANTHROPIC_API_KEY"
        )
    
    # Sort by priority and select the best one
    available_providers.sort(key=lambda x: x[1]["priority"])
    selected_provider, selected_config = available_providers[0]
    
    print(f"🚀 Auto-selected LLM provider: {selected_provider.upper()}")
    return selected_provider, selected_config

def get_market_config():
    """Get market-specific configuration."""
    market_type = os.getenv("TRADINGAGENTS_MARKET", "india").lower()
    
    if market_type == "india":
        from tradingagents.indian_config import INDIAN_CONFIG
        base_config = INDIAN_CONFIG.copy()
        print(f"🇮🇳 Configured for Indian markets (NSE/BSE)")
    else:
        from tradingagents.default_config import DEFAULT_CONFIG
        base_config = DEFAULT_CONFIG.copy()
        print(f"🇺🇸 Configured for US markets")
    
    return market_type, base_config

# Auto-detect LLM provider and market configuration
try:
    llm_provider, llm_config = detect_available_llm_provider()
    market_type, base_config = get_market_config()
except Exception as e:
    print(f"❌ Configuration Error: {e}")
    print("\n💡 Quick Setup:")
    print("export OPENAI_API_KEY='your-key'")
    print("export TRADINGAGENTS_MARKET='india'  # or 'us'")
    exit(1)

# Create unified configuration
config = base_config.copy()
config.update({
    "llm_provider": llm_provider,
    "backend_url": os.getenv("TRADINGAGENTS_BACKEND_URL", llm_config["backend_url"]),
    "deep_think_llm": os.getenv("TRADINGAGENTS_DEEP_THINK_LLM", llm_config["deep_model"]),
    "quick_think_llm": os.getenv("TRADINGAGENTS_QUICK_THINK_LLM", llm_config["quick_model"]),
    "max_debate_rounds": int(os.getenv("TRADINGAGENTS_MAX_DEBATE_ROUNDS", "1")),
    "online_tools": os.getenv("TRADINGAGENTS_ONLINE_TOOLS", "true").lower() in ('true', '1', 'yes', 'on'),
    "market": market_type
})

def main():
    """Main execution function with intelligent provider detection."""
    
    print("🤖 TradingAgents - Multi-Agent LLM Trading Framework")
    print("=" * 60)
    print(f"🔧 LLM Provider: {config['llm_provider'].upper()}")
    print(f"🌍 Market: {config['market'].upper()}")
    print(f"🌐 Online Tools: {'Enabled' if config['online_tools'] else 'Disabled'}")
    print(f"🤝 Debate Rounds: {config['max_debate_rounds']}")
    
    # Show available data sources
    data_sources = []
    if os.getenv("FINNHUB_API_KEY"):
        data_sources.append("Finnhub")
    if os.getenv("ALPHA_VANTAGE_API_KEY"):
        data_sources.append("Alpha Vantage")
    if os.getenv("REDDIT_CLIENT_ID"):
        data_sources.append("Reddit")
    
    print(f"📊 Data Sources: {', '.join(data_sources) if data_sources else 'Basic (Yahoo Finance)'}")
    print("=" * 60)
    
    # Initialize TradingAgents
    try:
        print("🚀 Initializing TradingAgents framework...")
        ta = TradingAgentsGraph(debug=True, config=config)
        print("✅ Framework initialized successfully!")
        
    except Exception as e:
        print(f"❌ Initialization Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your API keys with: python check_api_keys.py")
        print("2. Run validation: python validate_setup.py")
        print("3. Try a different LLM provider")
        return
    
    # Select example ticker based on market
    if config['market'] == "india":
        example_tickers = ["TCS", "RELIANCE", "INFY", "HDFCBANK", "ICICIBANK"]
        print(f"🇮🇳 Indian Market - Example stocks: {', '.join(example_tickers)}")
        ticker = "TCS"  # Tata Consultancy Services
    else:
        example_tickers = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"] 
        print(f"🇺🇸 US Market - Example stocks: {', '.join(example_tickers)}")
        ticker = "AAPL"  # Apple Inc.
    
    print(f"📈 Analyzing: {ticker}")
    print("-" * 40)
    
    # Run analysis
    try:
        print("🔍 Starting multi-agent analysis...")
        print("⏳ This may take 30-60 seconds...")
        
        _, decision = ta.propagate(ticker, "2024-09-09")
        
        print("\n" + "🎯 TRADING DECISION SUMMARY" + "🎯")
        print("=" * 60)
        print(decision)
        print("=" * 60)
        
        print(f"\n✅ Analysis complete for {ticker}!")
        print(f"💡 Try analyzing other {config['market'].upper()} stocks by modifying the ticker in main.py")
        
        # Optional: Enable reflection and memory
        # print("🧠 Learning from this analysis...")
        # ta.reflect_and_remember(1000)  # parameter is the position returns
        
    except Exception as e:
        print(f"❌ Analysis Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check internet connection")
        print("2. Verify API key limits")
        print("3. Try with offline tools: export TRADINGAGENTS_ONLINE_TOOLS=false")

if __name__ == "__main__":
    main()
