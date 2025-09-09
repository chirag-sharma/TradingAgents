# Indian financial news sources and sentiment analysis

import requests
import feedparser
from typing import Annotated, List, Dict
from datetime import datetime, timedelta
import pandas as pd
from bs4 import BeautifulSoup
import json
from .config import get_config


class IndianNewsUtils:
    """Utilities for fetching Indian financial news."""
    
    def __init__(self):
        self.config = get_config()
        self.news_sources = {
            "economic_times": {
                "rss_feeds": [
                    "https://economictimes.indiatimes.com/markets/stocks/rssfeeds/2146842.cms",
                    "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
                    "https://economictimes.indiatimes.com/industry/rssfeeds/13352306.cms"
                ]
            },
            "moneycontrol": {
                "rss_feeds": [
                    "https://www.moneycontrol.com/rss/business.xml",
                    "https://www.moneycontrol.com/rss/marketstats.xml"
                ]
            },
            "business_standard": {
                "rss_feeds": [
                    "https://www.business-standard.com/rss/markets-106.rss",
                    "https://www.business-standard.com/rss/companies-101.rss"
                ]
            },
            "livemint": {
                "rss_feeds": [
                    "https://www.livemint.com/rss/markets",
                    "https://www.livemint.com/rss/companies"
                ]
            }
        }
    
    def get_indian_financial_news(
        self,
        days_back: Annotated[int, "Number of days to look back"] = 7,
        sources: Annotated[List[str], "News sources to include"] = None
    ) -> List[Dict]:
        """Fetch recent Indian financial news from multiple sources."""
        
        if sources is None:
            sources = list(self.news_sources.keys())
        
        all_news = []
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        for source in sources:
            if source in self.news_sources:
                for rss_url in self.news_sources[source]["rss_feeds"]:
                    try:
                        feed = feedparser.parse(rss_url)
                        
                        for entry in feed.entries:
                            # Parse publication date
                            pub_date = None
                            if hasattr(entry, 'published_parsed'):
                                pub_date = datetime(*entry.published_parsed[:6])
                            elif hasattr(entry, 'updated_parsed'):
                                pub_date = datetime(*entry.updated_parsed[:6])
                            
                            # Filter by date
                            if pub_date and pub_date >= cutoff_date:
                                news_item = {
                                    "title": entry.get("title", ""),
                                    "summary": entry.get("summary", ""),
                                    "link": entry.get("link", ""),
                                    "published": pub_date.strftime("%Y-%m-%d %H:%M:%S") if pub_date else "",
                                    "source": source,
                                    "content": self._extract_article_content(entry.get("link", ""))
                                }
                                all_news.append(news_item)
                                
                    except Exception as e:
                        print(f"Error fetching news from {source}: {e}")
        
        # Sort by publication date (newest first)
        all_news.sort(key=lambda x: x["published"], reverse=True)
        return all_news
    
    def get_company_specific_news(
        self,
        company_name: Annotated[str, "Company name to search for"],
        symbol: Annotated[str, "Stock symbol"],
        days_back: Annotated[int, "Number of days to look back"] = 7
    ) -> List[Dict]:
        """Get news specific to a company."""
        
        all_news = self.get_indian_financial_news(days_back)
        company_news = []
        
        # Search terms
        search_terms = [
            company_name.lower(),
            symbol.lower(),
            f"{symbol}.ns",
            f"{symbol}.bo"
        ]
        
        for news_item in all_news:
            title_lower = news_item["title"].lower()
            summary_lower = news_item["summary"].lower()
            
            # Check if any search term appears in title or summary
            if any(term in title_lower or term in summary_lower for term in search_terms):
                company_news.append(news_item)
        
        return company_news
    
    def get_market_sentiment_news(
        self,
        days_back: Annotated[int, "Number of days to look back"] = 3
    ) -> Dict:
        """Get overall market sentiment from news headlines."""
        
        news_items = self.get_indian_financial_news(days_back)
        
        # Keywords for sentiment analysis
        positive_keywords = [
            "gains", "surge", "rally", "bullish", "growth", "profit", "dividend",
            "expansion", "acquisition", "partnership", "breakthrough", "record"
        ]
        
        negative_keywords = [
            "falls", "drops", "crash", "bearish", "loss", "decline", "recession",
            "layoffs", "bankruptcy", "investigation", "fraud", "warning"
        ]
        
        sentiment_scores = []
        categorized_news = {"positive": [], "negative": [], "neutral": []}
        
        for news in news_items:
            text = f"{news['title']} {news['summary']}".lower()
            
            positive_count = sum(1 for word in positive_keywords if word in text)
            negative_count = sum(1 for word in negative_keywords if word in text)
            
            if positive_count > negative_count:
                sentiment = "positive"
                score = 1
            elif negative_count > positive_count:
                sentiment = "negative"
                score = -1
            else:
                sentiment = "neutral"
                score = 0
            
            sentiment_scores.append(score)
            categorized_news[sentiment].append(news)
        
        overall_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
        
        return {
            "overall_sentiment_score": overall_sentiment,
            "total_articles": len(news_items),
            "categorized_news": categorized_news,
            "sentiment_distribution": {
                "positive": len(categorized_news["positive"]),
                "negative": len(categorized_news["negative"]),
                "neutral": len(categorized_news["neutral"])
            }
        }
    
    def _extract_article_content(self, url: str) -> str:
        """Extract article content from URL (basic implementation)."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to find main content (this is basic and may need refinement)
            content_tags = soup.find_all(['p', 'div'], class_=lambda x: x and 'content' in x.lower())
            if content_tags:
                content = ' '.join([tag.get_text().strip() for tag in content_tags[:3]])
                return content[:500]  # Limit content length
            
        except Exception as e:
            print(f"Error extracting content from {url}: {e}")
        
        return ""


# Social media sentiment for Indian stocks
class IndianSocialSentiment:
    """Social media sentiment analysis for Indian stocks."""
    
    def __init__(self):
        self.platforms = ["twitter", "reddit", "telegram"]
    
    def get_twitter_sentiment(
        self,
        symbol: Annotated[str, "Stock symbol"],
        company_name: Annotated[str, "Company name"],
        days_back: Annotated[int, "Days to look back"] = 3
    ) -> Dict:
        """Get Twitter sentiment for Indian stocks."""
        # This would require Twitter API access
        # Placeholder implementation
        return {
            "platform": "twitter",
            "sentiment_score": 0.0,
            "mention_count": 0,
            "positive_mentions": 0,
            "negative_mentions": 0,
            "neutral_mentions": 0,
            "trending_hashtags": [],
            "sample_tweets": []
        }
    
    def get_reddit_indian_stocks_sentiment(
        self,
        symbol: Annotated[str, "Stock symbol"],
        subreddits: Annotated[List[str], "Subreddits to search"] = None
    ) -> Dict:
        """Get Reddit sentiment from Indian stock communities."""
        
        if subreddits is None:
            subreddits = [
                "IndiaInvestments",
                "IndianStockMarket", 
                "indiainvestments",
                "DalalStreetTalks",
                "SecurityAnalysis"
            ]
        
        # This would require Reddit API integration
        # Placeholder implementation
        return {
            "platform": "reddit",
            "sentiment_score": 0.0,
            "post_count": 0,
            "comment_count": 0,
            "upvote_ratio": 0.0,
            "subreddit_breakdown": {},
            "sample_posts": []
        }
    
    def get_telegram_sentiment(
        self,
        symbol: Annotated[str, "Stock symbol"],
        channels: Annotated[List[str], "Telegram channels"] = None
    ) -> Dict:
        """Get sentiment from Indian stock Telegram channels."""
        
        # Popular Indian stock Telegram channels (requires API access)
        default_channels = [
            "StockMarketIndia",
            "IndianStocks",
            "NSE_BSE_Updates"
        ]
        
        if channels is None:
            channels = default_channels
        
        # Placeholder implementation
        return {
            "platform": "telegram",
            "sentiment_score": 0.0,
            "message_count": 0,
            "channel_breakdown": {},
            "sample_messages": []
        }


def get_indian_stock_news_summary(
    symbol: Annotated[str, "Stock symbol"],
    company_name: Annotated[str, "Company name"],
    days_back: Annotated[int, "Days to look back"] = 7
) -> str:
    """Get a comprehensive news summary for an Indian stock."""
    
    news_utils = IndianNewsUtils()
    
    # Get company-specific news
    company_news = news_utils.get_company_specific_news(company_name, symbol, days_back)
    
    # Get market sentiment
    market_sentiment = news_utils.get_market_sentiment_news(days_back)
    
    # Create summary
    summary = f"News Analysis for {company_name} ({symbol})\n"
    summary += f"Period: Last {days_back} days\n\n"
    
    summary += f"Market Sentiment Overview:\n"
    summary += f"- Overall sentiment score: {market_sentiment['overall_sentiment_score']:.2f}\n"
    summary += f"- Total articles analyzed: {market_sentiment['total_articles']}\n"
    summary += f"- Positive: {market_sentiment['sentiment_distribution']['positive']}\n"
    summary += f"- Negative: {market_sentiment['sentiment_distribution']['negative']}\n"
    summary += f"- Neutral: {market_sentiment['sentiment_distribution']['neutral']}\n\n"
    
    if company_news:
        summary += f"Company-Specific News ({len(company_news)} articles):\n"
        for i, news in enumerate(company_news[:5], 1):  # Top 5 news items
            summary += f"{i}. {news['title']}\n"
            summary += f"   Source: {news['source']} | Date: {news['published']}\n"
            if news['summary']:
                summary += f"   Summary: {news['summary'][:200]}...\n"
            summary += "\n"
    else:
        summary += "No company-specific news found in the specified period.\n"
    
    return summary
