#!/bin/bash
# TradingAgents Environment Setup Script
# Save this as 'setup_env.sh' and run with: source setup_env.sh

echo "🔧 Setting up TradingAgents Environment Variables..."

# Choose your LLM provider and set the corresponding API key
echo "Choose your LLM provider:"
echo "1. OpenAI (GPT-4, etc.)"
echo "2. Google (Gemini)"
echo "3. Anthropic (Claude)"

# OpenAI Configuration
# export OPENAI_API_KEY="sk-your-openai-api-key-here"
# export TRADINGAGENTS_LLM_PROVIDER="openai"
# export TRADINGAGENTS_DEEP_THINK_LLM="gpt-4o-mini"
# export TRADINGAGENTS_QUICK_THINK_LLM="gpt-4o-mini"
# export TRADINGAGENTS_BACKEND_URL="https://api.openai.com/v1"

# Google Configuration
# export GOOGLE_API_KEY="your-google-api-key-here"
# export TRADINGAGENTS_LLM_PROVIDER="google"
# export TRADINGAGENTS_DEEP_THINK_LLM="gemini-2.0-flash"
# export TRADINGAGENTS_QUICK_THINK_LLM="gemini-2.0-flash"
# export TRADINGAGENTS_BACKEND_URL="https://generativelanguage.googleapis.com/v1"

# Anthropic Configuration
# export ANTHROPIC_API_KEY="sk-ant-your-anthropic-api-key-here"
# export TRADINGAGENTS_LLM_PROVIDER="anthropic"
# export TRADINGAGENTS_DEEP_THINK_LLM="claude-3-sonnet-20240229"
# export TRADINGAGENTS_QUICK_THINK_LLM="claude-3-haiku-20240307"
# export TRADINGAGENTS_BACKEND_URL="https://api.anthropic.com"

# Market Selection
export TRADINGAGENTS_MARKET="us"  # Change to "india" for Indian markets

# Optional: Data source API keys for enhanced functionality
# export FINNHUB_API_KEY="your-finnhub-api-key"
# export ALPHA_VANTAGE_API_KEY="your-alpha-vantage-api-key"

# Framework Configuration
export TRADINGAGENTS_ONLINE_TOOLS="true"
export TRADINGAGENTS_MAX_DEBATE_ROUNDS="1"
export TRADINGAGENTS_DATA_DIR="./data"

echo "✅ Environment setup complete!"
echo "💡 Uncomment and fill in your API keys above, then run: source setup_env.sh"
echo "🚀 Then run: python main.py"
