# 🔑 Quick Setup Guide for .env File

## Step 1: Edit the .env file
Open the `.env` file in this directory and replace the placeholder values:

```bash
# Replace this line:
OPENAI_API_KEY=your-openai-api-key-here

# With your actual API key:
OPENAI_API_KEY=sk-proj-your-actual-openai-key-here
```

## Step 2: Get API Keys (if you don't have them)

### OpenAI (Recommended)
1. Go to: https://platform.openai.com/api-keys
2. Create account or log in
3. Click "Create new secret key"
4. Copy the key starting with `sk-proj-` or `sk-`

### Finnhub (Optional - for better market data)
1. Go to: https://finnhub.io/dashboard
2. Sign up for free account
3. Copy your API key

### Alpha Vantage (Optional - for additional market data)
1. Go to: https://www.alphavantage.co/support/#api-key
2. Get free API key
3. Copy the key

## Step 3: Save and Run
1. Save the `.env` file
2. Run: `./run_trading_agents.sh`
3. Choose option 1 for CLI or option 2 for direct analysis

## ✅ You're Ready!
The framework will automatically load your API keys and start with Indian market configuration.

---
**Tip**: Keep your API keys secure and never share them publicly!
