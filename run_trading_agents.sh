#!/bin/bash

# TradingAgents - Easy Startup Script
# This script sets up the environment and runs the framework

echo "🚀 Starting TradingAgents Framework..."

# Set up the Python path
export PYTHONPATH="/Users/chirag/VsCodeProjects/TradingAgents"

# Change to project directory
cd "/Users/chirag/VsCodeProjects/TradingAgents"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please configure your API keys in .env file first."
    echo "💡 Edit the .env file and add your API keys, then try again."
    exit 1
fi

# Activate virtual environment and run
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

echo "📋 Choose how to run TradingAgents:"
echo "1) CLI Interface (Interactive)"
echo "2) Direct Analysis (Quick)"
echo ""
read -p "Enter choice (1 or 2): " choice

case $choice in
    1)
        echo "🎯 Starting CLI Interface..."
        python cli/main.py
        ;;
    2)
        echo "🎯 Starting Direct Analysis..."
        python main.py
        ;;
    *)
        echo "❌ Invalid choice. Please enter 1 or 2."
        exit 1
        ;;
esac

echo "✅ TradingAgents session completed!"
