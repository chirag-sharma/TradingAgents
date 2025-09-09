# Indian Trading Agents Example
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.indian_config import INDIAN_CONFIG

def analyze_indian_stock(symbol, company_name, date, exchange="NSE"):
    """
    Analyze an Indian stock using the TradingAgents framework.
    
    Args:
        symbol (str): Indian stock symbol (e.g., 'RELIANCE', 'TCS')
        company_name (str): Full company name (e.g., 'Reliance Industries')
        date (str): Analysis date in YYYY-MM-DD format
        exchange (str): NSE or BSE
    
    Returns:
        Trading decision and analysis
    """
    
    # Create custom config for Indian market
    config = INDIAN_CONFIG.copy()
    
    # Configure your API keys here
    config["llm_provider"] = "openai"  # or "google", "anthropic"
    config["backend_url"] = "https://api.openai.com/v1"  # Your API URL
    config["deep_think_llm"] = "gpt-4o-mini"  # Use cost-effective model for testing
    config["quick_think_llm"] = "gpt-4o-mini"
    
    # Set Indian market specific settings
    config["market"] = "india"
    config["primary_exchange"] = exchange
    config["online_tools"] = True
    
    # Add your API keys if you have them
    # config["indian_apis"]["alpha_vantage"]["api_key"] = "YOUR_ALPHA_VANTAGE_KEY"
    
    print(f"🇮🇳 Analyzing {company_name} ({symbol}) on {exchange} for date: {date}")
    print("=" * 60)
    
    # Initialize with Indian config
    try:
        ta = TradingAgentsGraph(
            debug=True, 
            config=config,
            selected_analysts=["market", "news", "fundamentals"]  # Start with core analysts
        )
        
        # Run analysis
        print(f"🔍 Starting analysis for {symbol}...")
        final_state, decision = ta.propagate(symbol, date)
        
        print("\n" + "=" * 60)
        print("📊 ANALYSIS RESULTS")
        print("=" * 60)
        
        # Print key insights
        if 'market_report' in final_state and final_state['market_report']:
            print("\n🏪 MARKET ANALYSIS:")
            print(final_state['market_report'][:500] + "...")
        
        if 'news_report' in final_state and final_state['news_report']:
            print("\n📰 NEWS ANALYSIS:")
            print(final_state['news_report'][:500] + "...")
        
        if 'fundamentals_report' in final_state and final_state['fundamentals_report']:
            print("\n💰 FUNDAMENTALS ANALYSIS:")
            print(final_state['fundamentals_report'][:500] + "...")
        
        if 'final_trade_decision' in final_state:
            print("\n🎯 FINAL TRADING DECISION:")
            print(final_state['final_trade_decision'])
        
        print(f"\n✅ Decision: {decision}")
        
        return final_state, decision
        
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        print("\n💡 Troubleshooting tips:")
        print("1. Ensure you have internet connection for online data")
        print("2. Check if the stock symbol is correct")
        print("3. Verify the date is not too recent (market data delay)")
        print("4. Install missing dependencies if any")
        
        return None, None


def main():
    """Run examples with major Indian stocks."""
    
    # Example Indian stocks to analyze
    indian_stocks = [
        ("RELIANCE", "Reliance Industries Limited"),
        ("TCS", "Tata Consultancy Services"),
        ("INFY", "Infosys Limited"),
        ("HDFCBANK", "HDFC Bank Limited"),
        ("ICICIBANK", "ICICI Bank Limited"),
    ]
    
    # Use a date with available data (not too recent)
    analysis_date = "2024-03-15"  # Adjust as needed
    
    print("🚀 Indian TradingAgents Analysis Framework")
    print("=" * 60)
    print("This example demonstrates how to analyze Indian stocks")
    print("using the adapted TradingAgents framework.\n")
    
    # Run analysis for first stock as example
    symbol, company = indian_stocks[0]  # Reliance
    
    try:
        final_state, decision = analyze_indian_stock(
            symbol=symbol,
            company_name=company,
            date=analysis_date,
            exchange="NSE"
        )
        
        if decision:
            print(f"\n🎉 Successfully analyzed {company}!")
        
    except KeyboardInterrupt:
        print("\n⚠️  Analysis interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("📚 Next Steps:")
    print("1. Install required dependencies: pip install -e .")
    print("2. Get API keys for enhanced data (Alpha Vantage, etc.)")
    print("3. Customize the indian_config.py for your specific needs")
    print("4. Try analyzing different Indian stocks")
    print("5. Modify the selected_analysts for different perspectives")


if __name__ == "__main__":
    main()
