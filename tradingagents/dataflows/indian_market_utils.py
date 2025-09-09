# Indian market data utilities using multiple data sources

import yfinance as yf
import requests
import pandas as pd
from typing import Annotated, Optional, Dict, List
from datetime import datetime, timedelta
import json
from functools import wraps
from .utils import save_output, SavePathType, decorate_all_methods
from .config import get_config


def add_indian_suffix(symbol: str, exchange: str = "NSE") -> str:
    """Add appropriate suffix for Indian stocks based on exchange."""
    config = get_config()
    
    if symbol.endswith(('.NS', '.BO')):
        return symbol
    
    if exchange.upper() == "NSE":
        return f"{symbol}.NS"
    elif exchange.upper() == "BSE":
        return f"{symbol}.BO"
    else:
        return f"{symbol}.NS"  # Default to NSE


def init_indian_ticker(func):
    """Decorator to initialize yf.Ticker with Indian suffix."""
    @wraps(func)
    def wrapper(symbol: str, exchange: str = "NSE", *args, **kwargs):
        indian_symbol = add_indian_suffix(symbol, exchange)
        ticker = yf.Ticker(indian_symbol)
        return func(ticker, symbol, *args, **kwargs)
    return wrapper


@decorate_all_methods(init_indian_ticker)
class IndianMarketUtils:
    
    def get_indian_stock_data(
        symbol: Annotated[str, "Indian stock symbol (e.g., 'RELIANCE', 'TCS')"],
        start_date: Annotated[str, "start date YYYY-mm-dd"],
        end_date: Annotated[str, "end date YYYY-mm-dd"],
        exchange: Annotated[str, "NSE or BSE"] = "NSE",
        save_path: SavePathType = None,
    ) -> pd.DataFrame:
        """Retrieve Indian stock price data."""
        ticker = symbol  # ticker object from decorator
        end_date_adj = pd.to_datetime(end_date) + pd.DateOffset(days=1)
        end_date_adj = end_date_adj.strftime("%Y-%m-%d")
        
        stock_data = ticker.history(start=start_date, end=end_date_adj)
        
        if stock_data.empty:
            print(f"No data found for {symbol} on {exchange}")
            return pd.DataFrame()
            
        return stock_data

    def get_indian_company_info(
        symbol: Annotated[str, "Indian stock symbol"],
        exchange: Annotated[str, "NSE or BSE"] = "NSE",
    ) -> Dict:
        """Get Indian company information."""
        ticker = symbol
        info = ticker.info
        
        # Extract relevant information for Indian companies
        company_info = {
            "Company Name": info.get("shortName", info.get("longName", "N/A")),
            "Industry": info.get("industry", "N/A"),
            "Sector": info.get("sector", "N/A"),
            "Market Cap": info.get("marketCap", "N/A"),
            "Enterprise Value": info.get("enterpriseValue", "N/A"),
            "P/E Ratio": info.get("trailingPE", "N/A"),
            "P/B Ratio": info.get("priceToBook", "N/A"),
            "Dividend Yield": info.get("dividendYield", "N/A"),
            "52 Week High": info.get("fiftyTwoWeekHigh", "N/A"),
            "52 Week Low": info.get("fiftyTwoWeekLow", "N/A"),
            "Currency": info.get("currency", "INR"),
            "Exchange": info.get("exchange", exchange),
            "Country": info.get("country", "India"),
        }
        
        return company_info

    def get_nifty_data(
        start_date: Annotated[str, "start date YYYY-mm-dd"],
        end_date: Annotated[str, "end date YYYY-mm-dd"],
        index: Annotated[str, "nifty50, sensex, banknifty, etc."] = "nifty50"
    ) -> pd.DataFrame:
        """Get Indian market index data."""
        config = get_config()
        index_symbol = config.get("market_indices", {}).get(index, "^NSEI")
        
        ticker = yf.Ticker(index_symbol)
        end_date_adj = pd.to_datetime(end_date) + pd.DateOffset(days=1)
        end_date_adj = end_date_adj.strftime("%Y-%m-%d")
        
        return ticker.history(start=start_date, end=end_date_adj)

    def get_indian_financials(
        symbol: Annotated[str, "Indian stock symbol"],
        exchange: Annotated[str, "NSE or BSE"] = "NSE",
        statement_type: Annotated[str, "income, balance, cashflow"] = "income"
    ) -> pd.DataFrame:
        """Get Indian company financial statements."""
        ticker = symbol
        
        if statement_type.lower() == "income":
            return ticker.financials
        elif statement_type.lower() == "balance":
            return ticker.balance_sheet
        elif statement_type.lower() == "cashflow":
            return ticker.cashflow
        else:
            raise ValueError("statement_type must be 'income', 'balance', or 'cashflow'")

    def get_peer_comparison(
        symbol: Annotated[str, "Indian stock symbol"],
        peers: Annotated[List[str], "List of peer company symbols"],
        exchange: Annotated[str, "NSE or BSE"] = "NSE"
    ) -> pd.DataFrame:
        """Compare key metrics with peer companies."""
        companies = [symbol] + peers
        comparison_data = []
        
        for company in companies:
            try:
                indian_symbol = add_indian_suffix(company, exchange)
                ticker = yf.Ticker(indian_symbol)
                info = ticker.info
                
                comparison_data.append({
                    "Symbol": company,
                    "Company": info.get("shortName", company),
                    "Market Cap": info.get("marketCap", 0),
                    "P/E Ratio": info.get("trailingPE", 0),
                    "P/B Ratio": info.get("priceToBook", 0),
                    "ROE": info.get("returnOnEquity", 0),
                    "Debt/Equity": info.get("debtToEquity", 0),
                    "Dividend Yield": info.get("dividendYield", 0),
                })
            except Exception as e:
                print(f"Error fetching data for {company}: {e}")
                
        return pd.DataFrame(comparison_data)


# NSE specific functions using public APIs
class NSEUtils:
    
    @staticmethod
    def get_nse_stock_info(symbol: str) -> Dict:
        """Get stock info from NSE (using public endpoints)."""
        # Note: NSE has restricted direct API access, this is a placeholder
        # for when you have access to NSE data or third-party providers
        url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching NSE data for {symbol}: {e}")
        
        return {}
    
    @staticmethod
    def get_top_gainers_losers() -> Dict:
        """Get top gainers and losers from NSE."""
        try:
            # This would need to be implemented with proper NSE API access
            # or third-party data provider
            pass
        except Exception as e:
            print(f"Error fetching gainers/losers: {e}")
        
        return {}


# Alpha Vantage integration for Indian stocks
class AlphaVantageIndian:
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"
    
    def get_daily_data(self, symbol: str, exchange: str = "NSE") -> pd.DataFrame:
        """Get daily stock data from Alpha Vantage for Indian stocks."""
        # Alpha Vantage uses different format for Indian stocks
        if exchange == "NSE":
            av_symbol = f"{symbol}.NSE"
        else:
            av_symbol = f"{symbol}.BSE"
            
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': av_symbol,
            'apikey': self.api_key,
            'outputsize': 'compact'
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            if 'Time Series (Daily)' in data:
                df = pd.DataFrame(data['Time Series (Daily)']).T
                df.index = pd.to_datetime(df.index)
                df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
                df = df.astype(float)
                return df.sort_index()
        except Exception as e:
            print(f"Error fetching Alpha Vantage data: {e}")
        
        return pd.DataFrame()
