# Indian market interface functions for TradingAgents
from typing import Annotated
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .config import get_config

# Import Indian market utilities
try:
    from .indian_market_utils import IndianMarketUtils, add_indian_suffix, AlphaVantageIndian
    from .indian_news_utils import IndianNewsUtils, get_indian_stock_news_summary
    from .indian_technical_utils import IndianTechnicalAnalysis
    INDIAN_MODULES_AVAILABLE = True
except ImportError as e:
    print(f"Indian modules not available: {e}")
    INDIAN_MODULES_AVAILABLE = False


def get_indian_stock_data_online(
    symbol: Annotated[str, "Indian stock symbol (e.g., 'RELIANCE', 'TCS')"],
    start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
    end_date: Annotated[str, "End date in yyyy-mm-dd format"],
    exchange: Annotated[str, "NSE or BSE"] = "NSE"
) -> str:
    """Get Indian stock data using Yahoo Finance with Indian market suffixes."""
    
    if not INDIAN_MODULES_AVAILABLE:
        return "Indian market modules not available. Please install required dependencies."
    
    try:
        indian_utils = IndianMarketUtils()
        stock_data = indian_utils.get_indian_stock_data(symbol, start_date, end_date, exchange)
        
        if stock_data.empty:
            return f"No data found for {symbol} on {exchange} exchange between {start_date} and {end_date}"
        
        # Remove timezone info for cleaner output
        if stock_data.index.tz is not None:
            stock_data.index = stock_data.index.tz_localize(None)
        
        # Round numerical values
        numeric_columns = ["Open", "High", "Low", "Close", "Adj Close"]
        for col in numeric_columns:
            if col in stock_data.columns:
                stock_data[col] = stock_data[col].round(2)
        
        csv_string = stock_data.to_csv()
        
        header = f"# Indian stock data for {symbol} ({exchange}) from {start_date} to {end_date}\n"
        header += f"# Total records: {len(stock_data)}\n"
        header += f"# Currency: INR\n"
        header += f"# Data retrieved on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        return header + csv_string
        
    except Exception as e:
        return f"Error fetching Indian stock data for {symbol}: {str(e)}"


def get_indian_company_info_online(
    symbol: Annotated[str, "Indian stock symbol"],
    exchange: Annotated[str, "NSE or BSE"] = "NSE"
) -> str:
    """Get comprehensive information about an Indian company."""
    
    if not INDIAN_MODULES_AVAILABLE:
        return "Indian market modules not available."
    
    try:
        indian_utils = IndianMarketUtils()
        company_info = indian_utils.get_indian_company_info(symbol, exchange)
        
        info_str = f"## Company Information for {symbol} ({exchange})\n\n"
        for key, value in company_info.items():
            if value != "N/A" and value is not None:
                if key in ["Market Cap", "Enterprise Value"] and isinstance(value, (int, float)):
                    # Format large numbers
                    if value >= 1e12:
                        value_formatted = f"₹{value/1e12:.2f} Trillion"
                    elif value >= 1e9:
                        value_formatted = f"₹{value/1e9:.2f} Billion"
                    elif value >= 1e7:
                        value_formatted = f"₹{value/1e7:.2f} Crore"
                    else:
                        value_formatted = f"₹{value:,.2f}"
                    info_str += f"**{key}**: {value_formatted}\n"
                elif key in ["P/E Ratio", "P/B Ratio", "Dividend Yield"] and isinstance(value, (int, float)):
                    info_str += f"**{key}**: {value:.2f}\n"
                else:
                    info_str += f"**{key}**: {value}\n"
        
        return info_str
        
    except Exception as e:
        return f"Error fetching company info for {symbol}: {str(e)}"


def get_indian_technical_analysis_online(
    symbol: Annotated[str, "Indian stock symbol"],
    curr_date: Annotated[str, "Current date in yyyy-mm-dd format"],
    lookback_days: Annotated[int, "Number of days to analyze"] = 30,
    exchange: Annotated[str, "NSE or BSE"] = "NSE"
) -> str:
    """Get comprehensive technical analysis for Indian stocks."""
    
    if not INDIAN_MODULES_AVAILABLE:
        return "Indian technical analysis modules not available."
    
    try:
        start_date = (datetime.strptime(curr_date, "%Y-%m-%d") - 
                     relativedelta(days=lookback_days)).strftime("%Y-%m-%d")
        
        tech_analyzer = IndianTechnicalAnalysis()
        analysis = tech_analyzer.get_indian_technical_indicators(
            symbol, start_date, curr_date, exchange
        )
        
        if "error" in analysis:
            return f"Technical analysis error: {analysis['error']}"
        
        # Format the analysis into a readable report
        report = f"## Technical Analysis for {symbol} ({exchange})\n"
        report += f"Analysis Period: {analysis['analysis_period']}\n\n"
        
        # Trading recommendation
        recommendation = analysis.get('trading_recommendation', {})
        if recommendation:
            report += f"### Trading Recommendation: {recommendation.get('recommendation', 'N/A')}\n"
            report += f"Confidence Score: {recommendation.get('confidence_score', 0):.2f}\n"
            report += f"Risk Level: {recommendation.get('risk_level', 'Medium')}\n\n"
            
            signals = recommendation.get('signals', [])
            if signals:
                report += "**Key Signals:**\n"
                for signal in signals:
                    report += f"- {signal}\n"
                report += "\n"
        
        # Indian market context
        context = analysis.get('indian_market_context', {})
        if context:
            report += "### Indian Market Context\n"
            report += f"Performance vs Nifty: {context.get('relative_to_nifty', 0):.2f}%\n"
            
            sector_info = context.get('sector_context', {})
            if sector_info:
                report += f"Sector: {sector_info.get('sector', 'Other')}\n"
                report += f"Is Sector Leader: {sector_info.get('is_sector_leader', False)}\n"
            
            volatility = context.get('volatility_ranking', {})
            if volatility:
                report += f"Volatility Rank: {volatility.get('volatility_rank', 'Medium')}\n"
                report += f"Annualized Volatility: {volatility.get('annualized_volatility_pct', 0):.2f}%\n"
            
            liquidity = context.get('liquidity_analysis', {})
            if liquidity:
                report += f"Liquidity Rank: {liquidity.get('liquidity_rank', 'Medium')}\n"
                report += f"Average Volume: {liquidity.get('average_volume', 0):,}\n"
        
        return report
        
    except Exception as e:
        return f"Error in technical analysis for {symbol}: {str(e)}"


def get_indian_financial_news_online(
    symbol: Annotated[str, "Indian stock symbol"],
    company_name: Annotated[str, "Company name"],
    curr_date: Annotated[str, "Current date in yyyy-mm-dd format"],
    lookback_days: Annotated[int, "Number of days to look back"] = 7
) -> str:
    """Get Indian financial news for a specific company."""
    
    if not INDIAN_MODULES_AVAILABLE:
        return "Indian news modules not available."
    
    try:
        return get_indian_stock_news_summary(symbol, company_name, lookback_days)
        
    except Exception as e:
        return f"Error fetching Indian news for {symbol}: {str(e)}"


def get_indian_market_indices_online(
    curr_date: Annotated[str, "Current date in yyyy-mm-dd format"],
    lookback_days: Annotated[int, "Number of days to look back"] = 5
) -> str:
    """Get Indian market indices data (Nifty, Sensex, etc.)."""
    
    if not INDIAN_MODULES_AVAILABLE:
        return "Indian market modules not available."
    
    try:
        start_date = (datetime.strptime(curr_date, "%Y-%m-%d") - 
                     relativedelta(days=lookback_days)).strftime("%Y-%m-%d")
        
        indian_utils = IndianMarketUtils()
        
        indices_data = {}
        indices = ["nifty50", "sensex", "banknifty"]
        
        for index in indices:
            try:
                data = indian_utils.get_nifty_data(start_date, curr_date, index)
                if not data.empty:
                    latest = data.iloc[-1]
                    first = data.iloc[0]
                    change = ((latest['Close'] - first['Close']) / first['Close']) * 100
                    
                    indices_data[index] = {
                        "current_level": latest['Close'],
                        "change_pct": change,
                        "high": data['High'].max(),
                        "low": data['Low'].min(),
                        "volume": latest.get('Volume', 0)
                    }
            except Exception as e:
                print(f"Error processing index {index}: {e}")
                continue
        
        # Format report
        report = f"## Indian Market Indices Overview\n"
        report += f"Period: {start_date} to {curr_date}\n\n"
        
        for index, data in indices_data.items():
            index_name = index.upper().replace("50", " 50")
            report += f"### {index_name}\n"
            report += f"Current Level: {data['current_level']:.2f}\n"
            report += f"Change: {data['change_pct']:+.2f}%\n"
            report += f"High: {data['high']:.2f}\n"
            report += f"Low: {data['low']:.2f}\n\n"
        
        return report
        
    except Exception as e:
        return f"Error fetching Indian market indices: {str(e)}"


def get_indian_peer_comparison_online(
    symbol: Annotated[str, "Indian stock symbol"],
    peers: Annotated[str, "Comma-separated list of peer symbols"],
    exchange: Annotated[str, "NSE or BSE"] = "NSE"
) -> str:
    """Compare Indian stock with its peers."""
    
    if not INDIAN_MODULES_AVAILABLE:
        return "Indian market modules not available."
    
    try:
        peer_list = [p.strip() for p in peers.split(",") if p.strip()]
        
        indian_utils = IndianMarketUtils()
        comparison_df = indian_utils.get_peer_comparison(symbol, peer_list, exchange)
        
        if comparison_df.empty:
            return f"No data available for peer comparison of {symbol}"
        
        # Format as readable table
        report = f"## Peer Comparison for {symbol}\n\n"
        
        for _, row in comparison_df.iterrows():
            report += f"### {row['Symbol']} - {row['Company']}\n"
            report += f"Market Cap: ₹{row['Market Cap']:,.0f}\n"
            report += f"P/E Ratio: {row['P/E Ratio']:.2f}\n"
            report += f"P/B Ratio: {row['P/B Ratio']:.2f}\n"
            report += f"ROE: {row['ROE']:.2%}\n"
            report += f"Debt/Equity: {row['Debt/Equity']:.2f}\n"
            report += f"Dividend Yield: {row['Dividend Yield']:.2%}\n\n"
        
        return report
        
    except Exception as e:
        return f"Error in peer comparison for {symbol}: {str(e)}"
