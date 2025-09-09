#!/usr/bin/env python3
"""
Quick API Key Status Checker

Run this script to check which API keys are configured and get setup guidance.
"""

import os
import sys

def check_api_keys():
    """Check the status of all API keys."""
    
    print("🔑 TradingAgents API Key Status")
    print("=" * 50)
    
    # LLM Provider Keys
    llm_keys = {
        "OpenAI": {
            "env_var": "OPENAI_API_KEY",
            "url": "https://platform.openai.com/api-keys",
            "free_tier": "$5 free credit",
            "models": "GPT-4o, GPT-4o-mini"
        },
        "Google": {
            "env_var": "GOOGLE_API_KEY", 
            "url": "https://makersuite.google.com/app/apikey",
            "free_tier": "Free tier available",
            "models": "Gemini Pro, Gemini Flash"
        },
        "Anthropic": {
            "env_var": "ANTHROPIC_API_KEY",
            "url": "https://console.anthropic.com/",
            "free_tier": "$5 free credit", 
            "models": "Claude 3.5 Sonnet, Claude 3 Haiku"
        }
    }
    
    # Data Source Keys (optional)
    data_keys = {
        "Finnhub": {
            "env_var": "FINNHUB_API_KEY",
            "url": "https://finnhub.io/dashboard", 
            "free_tier": "60 calls/min free",
            "purpose": "Financial data & news"
        },
        "Alpha Vantage": {
            "env_var": "ALPHA_VANTAGE_API_KEY",
            "url": "https://www.alphavantage.co/support/#api-key",
            "free_tier": "25 calls/day free",
            "purpose": "Market data & analysis"
        }
    }
    
    configured_llm = []
    configured_data = []
    
    print("📡 LLM PROVIDERS (Required - choose at least one):")
    print("-" * 50)
    
    for provider, info in llm_keys.items():
        api_key = os.getenv(info["env_var"])
        if api_key:
            status = f"✅ Configured ({len(api_key[-4:])} chars: ...{api_key[-4:]})"
            configured_llm.append(provider)
        else:
            status = "❌ Not configured"
        
        print(f"{provider:.<12} {status}")
        if not api_key:
            print(f"             Get key: {info['url']}")
            print(f"             Free tier: {info['free_tier']}")
            print(f"             Models: {info['models']}")
        print()
    
    print("📊 DATA SOURCES (Optional but recommended):")
    print("-" * 50)
    
    for provider, info in data_keys.items():
        api_key = os.getenv(info["env_var"])
        if api_key:
            status = f"✅ Configured ({len(api_key[-4:])} chars: ...{api_key[-4:]})"
            configured_data.append(provider)
        else:
            status = "❌ Not configured"
        
        print(f"{provider:.<15} {status}")
        if not api_key:
            print(f"                Get key: {info['url']}")
            print(f"                Free tier: {info['free_tier']}")
            print(f"                Purpose: {info['purpose']}")
        print()
    
    # Configuration status
    print("⚙️  CONFIGURATION STATUS:")
    print("-" * 50)
    
    market = os.getenv("TRADINGAGENTS_MARKET", "us")
    provider = os.getenv("TRADINGAGENTS_LLM_PROVIDER", "auto-detect")
    
    print(f"Market.......... {market.upper()}")
    print(f"LLM Provider.... {provider}")
    print(f"Online Tools.... {os.getenv('TRADINGAGENTS_ONLINE_TOOLS', 'true')}")
    print(f"Data Directory.. {os.getenv('TRADINGAGENTS_DATA_DIR', './data')}")
    
    # Summary and next steps
    print("\n🎯 SUMMARY:")
    print("-" * 50)
    
    if configured_llm:
        print(f"✅ LLM Providers: {', '.join(configured_llm)}")
    else:
        print("❌ No LLM providers configured - YOU NEED AT LEAST ONE!")
    
    if configured_data:
        print(f"✅ Data Sources: {', '.join(configured_data)}")
    else:
        print("⚠️  No additional data sources configured (optional)")
    
    print(f"\n🚀 NEXT STEPS:")
    print("-" * 50)
    
    if not configured_llm:
        print("1. ❗ Configure at least one LLM provider:")
        print("   export OPENAI_API_KEY='your-key'")
        print("   export TRADINGAGENTS_LLM_PROVIDER='openai'")
        print("\n2. 🔍 Run validation: python validate_setup.py")
        print("3. 🏃 Run framework: python main.py")
        return False
    else:
        print("1. ✅ LLM provider configured!")
        print("2. 🔍 Run validation: python validate_setup.py") 
        print("3. 🏃 Run framework: python main.py")
        print("4. 💡 Or try CLI: python -m cli.main")
        
        if not configured_data:
            print("\n💡 Optional: Configure data sources for enhanced functionality:")
            print("   export FINNHUB_API_KEY='your-key'")
            print("   export ALPHA_VANTAGE_API_KEY='your-key'")
        
        return True

def show_quick_setup():
    """Show quick setup commands."""
    
    print("\n⚡ QUICK SETUP COMMANDS:")
    print("-" * 50)
    print("# Option 1: OpenAI + US Market")
    print("export OPENAI_API_KEY='sk-your-key'")
    print("export TRADINGAGENTS_LLM_PROVIDER='openai'")
    print("export TRADINGAGENTS_MARKET='us'")
    print()
    print("# Option 2: Google + Indian Market") 
    print("export GOOGLE_API_KEY='your-key'")
    print("export TRADINGAGENTS_LLM_PROVIDER='google'")
    print("export TRADINGAGENTS_MARKET='india'")
    print()
    print("# Then run:")
    print("python main.py")

if __name__ == "__main__":
    ready = check_api_keys()
    
    if not ready:
        show_quick_setup()
        sys.exit(1)
    else:
        print("\n🎉 You're ready to use TradingAgents!")
        sys.exit(0)
