#!/usr/bin/env python3
"""
TradingAgents Validation Script

This script validates the refactoring fixes and ensures the framework
is properly configured and functional.
"""

import sys
import os
import importlib.util
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are available."""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        ("pandas", "pandas"), ("yfinance", "yfinance"), ("stockstats", "stockstats"), 
        ("langchain_openai", "langchain_openai"), ("langchain_anthropic", "langchain_anthropic"),
        ("langchain_google_genai", "langchain_google_genai"), ("langgraph", "langgraph"),
        ("requests", "requests"), ("beautifulsoup4", "bs4"), ("feedparser", "feedparser"),
        ("chromadb", "chromadb")
    ]
    
    missing_packages = []
    
    for package_name, import_name in required_packages:
        try:
            spec = importlib.util.find_spec(import_name)
            if spec is None:
                missing_packages.append(package_name)
            else:
                print(f"  ✅ {package_name}")
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -e . to install missing dependencies")
        return False
    
    print("✅ All dependencies available")
    return True


def check_configuration():
    """Check configuration management."""
    print("\n🔧 Checking configuration...")
    
    try:
        # Test import of new config manager
        from tradingagents.config_manager import ConfigManager, get_config_manager
        print("  ✅ New configuration manager available")
        
        # Test US config
        us_config = ConfigManager("us")
        us_settings = us_config.get_config()
        print(f"  ✅ US market config loaded ({len(us_settings)} settings)")
        
        # Test Indian config  
        indian_config = ConfigManager("india")
        indian_settings = indian_config.get_config()
        print(f"  ✅ Indian market config loaded ({len(indian_settings)} settings)")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Configuration error: {e}")
        return False


def check_imports():
    """Check critical import issues are fixed."""
    print("\n📦 Checking imports...")
    
    try:
        # Test dataflows imports
        from tradingagents.dataflows import StockstatsUtils, YFinanceUtils
        print("  ✅ Core dataflows imports working")
        
        # Test Indian modules
        from tradingagents.dataflows.indian_technical_utils import IndianTechnicalAnalysis
        from tradingagents.dataflows.indian_market_utils import IndianMarketUtils
        print("  ✅ Indian market modules importing correctly")
        
        # Test main framework
        from tradingagents.graph.trading_graph import TradingAgentsGraph
        print("  ✅ Main trading graph importing correctly")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Import error: {e}")
        return False


def check_file_structure():
    """Check that critical files exist."""
    print("\n📁 Checking file structure...")
    
    critical_files = [
        "tradingagents/config_manager.py",
        "tradingagents/error_handling.py", 
        "tradingagents/default_config.py",
        "tradingagents/indian_config.py",
        "tradingagents/dataflows/stockstats_utils.py",
        "tradingagents/dataflows/indian_technical_utils.py",
        "main.py",
        "pyproject.toml"
    ]
    
    missing_files = []
    
    for file_path in critical_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"  ✅ {file_path}")
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All critical files present")
    return True


def check_api_keys():
    """Check if API keys are configured."""
    print("\n🔑 Checking API key configuration...")
    
    api_keys = {
        "OpenAI": "OPENAI_API_KEY",
        "Google": "GOOGLE_API_KEY", 
        "Anthropic": "ANTHROPIC_API_KEY",
        "Finnhub": "FINNHUB_API_KEY",
        "Alpha Vantage": "ALPHA_VANTAGE_API_KEY"
    }
    
    configured_keys = []
    
    for service, env_var in api_keys.items():
        if os.getenv(env_var):
            configured_keys.append(service)
            print(f"  ✅ {service} API key configured")
        else:
            print(f"  ⚠️  {service} API key not configured ({env_var})")
    
    if configured_keys:
        print(f"✅ {len(configured_keys)} API key(s) configured")
        return True
    else:
        print("❌ No API keys configured - framework will have limited functionality")
        return False


def main():
    """Run all validation checks."""
    print("🔍 TradingAgents Validation Report")
    print("=" * 50)
    
    checks = [
        ("File Structure", check_file_structure),
        ("Dependencies", check_dependencies), 
        ("Configuration", check_configuration),
        ("Imports", check_imports),
        ("API Keys", check_api_keys)
    ]
    
    results = {}
    
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"\n❌ {check_name} check failed: {e}")
            results[check_name] = False
    
    print("\n" + "=" * 50)
    print("📊 VALIDATION SUMMARY")
    print("=" * 50)
    
    passed = sum(results.values())
    total = len(results)
    
    for check_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{check_name:.<20} {status}")
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 All validation checks passed! Framework is ready to use.")
        print("\nNext steps:")
        print("1. Set your API keys (see README.md)")
        print("2. Run: python main.py")
        print("3. Or try the CLI: python -m cli.main")
        return 0
    else:
        print(f"\n⚠️  {total - passed} validation check(s) failed.")
        print("Please address the issues above before using the framework.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
