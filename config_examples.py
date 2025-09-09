"""
Advanced Configuration Example using the new ConfigManager

This demonstrates the most flexible way to configure API keys and settings
using the new unified configuration system.
"""

import os
from tradingagents.config_manager import ConfigManager, get_config_manager
from tradingagents.graph.trading_graph import TradingAgentsGraph

def setup_with_config_manager():
    """Example using the new ConfigManager for flexible configuration."""
    
    # Method 1: Environment variables (recommended)
    os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
    os.environ["TRADINGAGENTS_LLM_PROVIDER"] = "openai"
    os.environ["TRADINGAGENTS_MARKET"] = "us"
    
    # Create config manager
    config_manager = ConfigManager(market_type="us")
    
    # Get configuration
    config = config_manager.get_config()
    
    # Initialize TradingAgents with managed config
    ta = TradingAgentsGraph(debug=True, config=config)
    
    return ta, config_manager

def setup_indian_market():
    """Example for Indian market setup."""
    
    # Set up for Indian market
    os.environ["GOOGLE_API_KEY"] = "your-google-api-key"
    os.environ["TRADINGAGENTS_LLM_PROVIDER"] = "google"
    os.environ["TRADINGAGENTS_MARKET"] = "india"
    
    # Optional: Indian-specific APIs
    os.environ["ALPHA_VANTAGE_API_KEY"] = "your-alpha-vantage-key"
    
    # Create Indian market config
    config_manager = ConfigManager(market_type="india")
    
    # Verify Indian market setup
    if config_manager.is_indian_market():
        print("✅ Indian market configuration active")
        print(f"Primary Exchange: {config_manager.get('primary_exchange')}")
        print(f"Currency: {config_manager.get('currency')}")
        print(f"Market Hours: {config_manager.get('market_open')} - {config_manager.get('market_close')}")
    
    config = config_manager.get_config()
    ta = TradingAgentsGraph(debug=True, config=config)
    
    return ta, config_manager

def check_api_key_status():
    """Check which API keys are configured."""
    
    config_manager = get_config_manager()
    
    print("🔑 API Key Status:")
    print("-" * 30)
    
    services = ["openai", "google", "anthropic", "finnhub", "alpha_vantage"]
    
    for service in services:
        api_key = config_manager.get_api_key(service)
        status = "✅ Configured" if api_key else "❌ Not configured"
        print(f"{service.capitalize():.<15} {status}")
    
    print("\n💡 Set missing API keys using environment variables:")
    print("export OPENAI_API_KEY='your-key'")
    print("export GOOGLE_API_KEY='your-key'")
    print("export ANTHROPIC_API_KEY='your-key'")
    print("export FINNHUB_API_KEY='your-key'")
    print("export ALPHA_VANTAGE_API_KEY='your-key'")

if __name__ == "__main__":
    print("🔧 TradingAgents Configuration Examples")
    print("=" * 50)
    
    # Check current API key status
    check_api_key_status()
    
    print("\n📚 Configuration Examples:")
    print("1. setup_with_config_manager() - US market with OpenAI")
    print("2. setup_indian_market() - Indian market with Google")
    print("\nUncomment the function calls below to test:")
    print("# ta, config = setup_with_config_manager()")
    print("# ta, config = setup_indian_market()")
