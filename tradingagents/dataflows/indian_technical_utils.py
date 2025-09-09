# Indian technical analysis using stockstats
import pandas as pd
from typing import Annotated, Dict, List
from .stockstats_utils import StockstatsUtils
from .indian_market_utils import IndianMarketUtils, add_indian_suffix
from datetime import datetime, timedelta


class IndianTechnicalAnalysis:
    """Technical analysis specifically for Indian stocks."""
    
    def __init__(self):
        self.stock_utils = StockstatsUtils()
        self.market_utils = IndianMarketUtils()
    
    def get_indian_technical_indicators(
        self,
        symbol: Annotated[str, "Indian stock symbol"],
        start_date: Annotated[str, "Start date YYYY-mm-dd"],
        end_date: Annotated[str, "End date YYYY-mm-dd"],
        exchange: Annotated[str, "NSE or BSE"] = "NSE"
    ) -> Dict:
        """Get comprehensive technical analysis for Indian stocks."""
        
        # Get stock data
        stock_data = self.market_utils.get_indian_stock_data(
            symbol, start_date, end_date, exchange
        )
        
        if stock_data.empty:
            return {"error": f"No data available for {symbol}"}
        
        # Calculate technical indicators using existing stockstats
        indicators = self.stock_utils.get_stockstats_indicators_report(
            stock_data, f"{symbol}.{exchange}"
        )
        
        # Add Indian market specific analysis
        indian_analysis = self._add_indian_market_context(
            symbol, stock_data, exchange
        )
        
        # Combine results
        result = {
            "symbol": symbol,
            "exchange": exchange,
            "analysis_period": f"{start_date} to {end_date}",
            "technical_indicators": indicators,
            "indian_market_context": indian_analysis,
            "trading_recommendation": self._generate_trading_recommendation(
                indicators, indian_analysis
            )
        }
        
        return result
    
    def _add_indian_market_context(
        self, 
        symbol: str, 
        stock_data: pd.DataFrame, 
        exchange: str
    ) -> Dict:
        """Add Indian market specific context to analysis."""
        
        # Get Nifty data for comparison
        end_date = stock_data.index[-1].strftime('%Y-%m-%d')
        start_date = (stock_data.index[-1] - timedelta(days=30)).strftime('%Y-%m-%d')
        
        try:
            nifty_data = self.market_utils.get_nifty_data(start_date, end_date, "nifty50")
            
            # Calculate relative performance vs Nifty
            if not nifty_data.empty:
                stock_return = (stock_data['Close'][-1] / stock_data['Close'][0] - 1) * 100
                nifty_return = (nifty_data['Close'][-1] / nifty_data['Close'][0] - 1) * 100
                relative_performance = stock_return - nifty_return
            else:
                relative_performance = 0
                
        except Exception as e:
            print(f"Error calculating relative performance for {symbol}: {e}")
            relative_performance = 0
        
        # Sector-specific analysis (simplified)
        sector_context = self._get_sector_context(symbol, exchange)
        
        # Market timing context
        market_timing = self._analyze_market_timing(stock_data)
        
        return {
            "relative_to_nifty": relative_performance,
            "sector_context": sector_context,
            "market_timing": market_timing,
            "volatility_ranking": self._calculate_volatility_ranking(stock_data),
            "liquidity_analysis": self._analyze_liquidity(stock_data)
        }
    
    def _get_sector_context(self, symbol: str, exchange: str) -> Dict:
        """Get sector-specific context for the stock."""
        
        # Major Indian sector classifications
        sector_leaders = {
            "IT": ["TCS", "INFY", "WIPRO", "HCLTECH", "TECHM"],
            "Banking": ["HDFC", "ICICIBANK", "KOTAKBANK", "AXISBANK", "SBIN"],
            "Auto": ["MARUTI", "TATAMOTORS", "M&M", "BAJAJ-AUTO", "EICHERMOT"],
            "Pharma": ["SUNPHARMA", "DRREDDY", "CIPLA", "BIOCON", "LUPIN"],
            "FMCG": ["HINDUNILVR", "ITC", "NESTLEIND", "BRITANNIA", "DABUR"],
            "Oil & Gas": ["RELIANCE", "ONGC", "IOC", "BPCL", "GAIL"],
            "Metals": ["TATASTEEL", "HINDALCO", "JSWSTEEL", "NMDC", "COALINDIA"],
            "Telecom": ["BHARTIARTL", "IDEA", "RCOM"]
        }
        
        # Find sector
        stock_sector = "Other"
        for sector, stocks in sector_leaders.items():
            if symbol.upper() in stocks:
                stock_sector = sector
                break
        
        return {
            "sector": stock_sector,
            "sector_leaders": sector_leaders.get(stock_sector, []),
            "is_sector_leader": symbol.upper() in sector_leaders.get(stock_sector, [])
        }
    
    def _analyze_market_timing(self, stock_data: pd.DataFrame) -> Dict:
        """Analyze market timing factors."""
        
        current_price = stock_data['Close'][-1]
        
        # Calculate price levels
        week_high = stock_data['High'][-5:].max() if len(stock_data) >= 5 else current_price
        week_low = stock_data['Low'][-5:].min() if len(stock_data) >= 5 else current_price
        month_high = stock_data['High'][-20:].max() if len(stock_data) >= 20 else current_price
        month_low = stock_data['Low'][-20:].min() if len(stock_data) >= 20 else current_price
        
        # Price position analysis
        week_position = (current_price - week_low) / (week_high - week_low) if week_high != week_low else 0.5
        month_position = (current_price - month_low) / (month_high - month_low) if month_high != month_low else 0.5
        
        return {
            "current_price": current_price,
            "week_high": week_high,
            "week_low": week_low,
            "month_high": month_high,
            "month_low": month_low,
            "week_position_pct": week_position * 100,
            "month_position_pct": month_position * 100,
            "near_week_high": week_position > 0.9,
            "near_week_low": week_position < 0.1,
            "near_month_high": month_position > 0.9,
            "near_month_low": month_position < 0.1
        }
    
    def _calculate_volatility_ranking(self, stock_data: pd.DataFrame) -> Dict:
        """Calculate volatility metrics."""
        
        if len(stock_data) < 20:
            return {"error": "Insufficient data for volatility calculation"}
        
        # Calculate returns
        returns = stock_data['Close'].pct_change().dropna()
        
        # Volatility metrics
        daily_vol = returns.std()
        annualized_vol = daily_vol * (252 ** 0.5) * 100  # Assuming 252 trading days
        
        # Rolling volatility
        rolling_vol = returns.rolling(window=10).std().iloc[-1] if len(returns) >= 10 else daily_vol
        
        return {
            "daily_volatility_pct": daily_vol * 100,
            "annualized_volatility_pct": annualized_vol,
            "10day_rolling_volatility_pct": rolling_vol * 100,
            "volatility_rank": "High" if annualized_vol > 40 else "Medium" if annualized_vol > 20 else "Low"
        }
    
    def _analyze_liquidity(self, stock_data: pd.DataFrame) -> Dict:
        """Analyze stock liquidity."""
        
        if 'Volume' not in stock_data.columns:
            return {"error": "Volume data not available"}
        
        avg_volume = stock_data['Volume'].mean()
        recent_volume = stock_data['Volume'][-5:].mean() if len(stock_data) >= 5 else avg_volume
        
        volume_ratio = recent_volume / avg_volume if avg_volume > 0 else 1
        
        # Liquidity ranking (simplified)
        if avg_volume > 1000000:
            liquidity_rank = "High"
        elif avg_volume > 100000:
            liquidity_rank = "Medium"
        else:
            liquidity_rank = "Low"
        
        return {
            "average_volume": int(avg_volume),
            "recent_volume": int(recent_volume),
            "volume_ratio": volume_ratio,
            "liquidity_rank": liquidity_rank,
            "volume_surge": volume_ratio > 1.5
        }
    
    def _generate_trading_recommendation(
        self, 
        technical_indicators: Dict, 
        indian_context: Dict
    ) -> Dict:
        """Generate trading recommendation based on analysis."""
        
        signals = []
        score = 0
        
        # Technical signals (simplified logic)
        if isinstance(technical_indicators, dict):
            # RSI analysis
            rsi = technical_indicators.get('rsi', 50)
            if rsi < 30:
                signals.append("RSI oversold - potential buy")
                score += 1
            elif rsi > 70:
                signals.append("RSI overbought - potential sell")
                score -= 1
            
            # MACD analysis
            macd_signal = technical_indicators.get('macd_signal', 'neutral')
            if 'bullish' in str(macd_signal).lower():
                signals.append("MACD bullish crossover")
                score += 1
            elif 'bearish' in str(macd_signal).lower():
                signals.append("MACD bearish crossover")
                score -= 1
        
        # Indian market context
        if indian_context.get('relative_to_nifty', 0) > 5:
            signals.append("Outperforming Nifty")
            score += 0.5
        elif indian_context.get('relative_to_nifty', 0) < -5:
            signals.append("Underperforming Nifty")
            score -= 0.5
        
        # Market timing
        market_timing = indian_context.get('market_timing', {})
        if market_timing.get('near_month_low', False):
            signals.append("Near monthly low - potential support")
            score += 0.5
        elif market_timing.get('near_month_high', False):
            signals.append("Near monthly high - potential resistance")
            score -= 0.5
        
        # Generate recommendation
        if score >= 1.5:
            recommendation = "BUY"
        elif score <= -1.5:
            recommendation = "SELL"
        else:
            recommendation = "HOLD"
        
        return {
            "recommendation": recommendation,
            "confidence_score": abs(score),
            "signals": signals,
            "risk_level": indian_context.get('volatility_ranking', {}).get('volatility_rank', 'Medium')
        }
