"""Market data fetching utility for financial dashboard."""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import streamlit as st
from logger import get_logger

logger = get_logger()


class MarketDataFetcher:
    """Fetch and cache market data for dashboard display."""
    
    # Indian indices
    INDIAN_INDICES = {
        "NIFTY 50": "^NSEI",
        "Sensex": "^BSESN",
        "Bank Nifty": "^NSEBANK",
    }
    
    # Global indices
    GLOBAL_INDICES = {
        "S&P 500": "^GSPC",
        "Nasdaq": "^IXIC",
        "Dow Jones": "^DJI",
    }
    
    # Commodities
    COMMODITIES = {
        "Gold": "GC=F",
        "Silver": "SI=F",
        "Crude Oil": "CL=F",
    }
    
    @staticmethod
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def get_index_data(ticker: str) -> Optional[Dict]:
        """Fetch current index data."""
        try:
            data = yf.Ticker(ticker)
            hist = data.history(period="1d")
            
            if hist.empty:
                return None
            
            current_price = hist['Close'].iloc[-1]
            
            # Get previous close for change calculation
            hist_prev = data.history(period="5d")
            if len(hist_prev) > 1:
                prev_price = hist_prev['Close'].iloc[-2]
            else:
                prev_price = current_price
            
            change = current_price - prev_price
            change_pct = (change / prev_price * 100) if prev_price > 0 else 0
            
            return {
                "price": round(current_price, 2),
                "change": round(change, 2),
                "change_pct": round(change_pct, 2),
                "timestamp": datetime.now()
            }
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            return None
    
    @staticmethod
    @st.cache_data(ttl=300)
    def get_all_indices() -> Dict[str, Dict]:
        """Fetch all indices data."""
        indices_data = {}
        
        # Fetch Indian indices
        for name, ticker in MarketDataFetcher.INDIAN_INDICES.items():
            data = MarketDataFetcher.get_index_data(ticker)
            if data:
                indices_data[name] = data
        
        return indices_data
    
    @staticmethod
    @st.cache_data(ttl=300)
    def get_all_global_indices() -> Dict[str, Dict]:
        """Fetch all global indices data."""
        indices_data = {}
        
        # Fetch global indices
        for name, ticker in MarketDataFetcher.GLOBAL_INDICES.items():
            data = MarketDataFetcher.get_index_data(ticker)
            if data:
                indices_data[name] = data
        
        return indices_data
    
    @staticmethod
    @st.cache_data(ttl=300)
    def get_all_commodities() -> Dict[str, Dict]:
        """Fetch all commodities data."""
        commodities_data = {}
        
        # Fetch commodities
        for name, ticker in MarketDataFetcher.COMMODITIES.items():
            data = MarketDataFetcher.get_index_data(ticker)
            if data:
                commodities_data[name] = data
        
        return commodities_data
    
    @staticmethod
    @st.cache_data(ttl=600)
    def get_stock_data(symbol: str, period: str = "1y") -> Optional[pd.DataFrame]:
        """Fetch historical stock data - handles both US and Indian stocks."""
        try:
            # First, check if it's already a US stock (has .NS, .BO, or other suffixes)
            if "." in symbol:
                # Already has a suffix, use as-is
                data = yf.download(symbol, period=period, progress=False)
                if not data.empty:
                    logger.debug(f"Fetched stock data for {symbol}")
                    return data
                return None
            
            # Try as US stock first (most common)
            try:
                data = yf.download(symbol, period=period, progress=False)
                if not data.empty and len(data) > 2:  # Ensure we got real data
                    logger.debug(f"Fetched US stock data for {symbol}")
                    return data
            except Exception as us_error:
                logger.debug(f"Failed to fetch US stock {symbol}: {us_error}")
            
            # If US failed, try Indian stock with .NS suffix
            try:
                data = yf.download(symbol + ".NS", period=period, progress=False)
                if not data.empty and len(data) > 2:
                    logger.debug(f"Fetched Indian stock data for {symbol}.NS")
                    return data
            except Exception as ns_error:
                logger.debug(f"Failed to fetch Indian stock {symbol}.NS: {ns_error}")
            
            # If .NS failed, try .BO (BSE)
            try:
                data = yf.download(symbol + ".BO", period=period, progress=False)
                if not data.empty and len(data) > 2:
                    logger.debug(f"Fetched Indian stock data for {symbol}.BO")
                    return data
            except Exception as bo_error:
                logger.debug(f"Failed to fetch Indian stock {symbol}.BO: {bo_error}")
            
            logger.warning(f"No valid data found for {symbol}")
            return None
            
        except Exception as e:
            logger.error(f"Error fetching stock data for {symbol}: {e}")
            return None
    
    @staticmethod
    def get_stock_info(symbol: str) -> Optional[Dict]:
        """Get basic stock information for US and Indian stocks."""
        try:
            adjusted_symbol = symbol
            ticker_obj = None
            
            # Try original symbol first
            try:
                ticker_obj = yf.Ticker(symbol)
                info = ticker_obj.info
                if info and len(info) > 5:  # Got valid data
                    adjusted_symbol = symbol
            except:
                pass
            
            # If original failed, try with .NS suffix (Indian NSE)
            if not ticker_obj or not info or len(info) < 5:
                try:
                    ticker_obj = yf.Ticker(symbol + ".NS")
                    info = ticker_obj.info
                    if info and len(info) > 5:
                        adjusted_symbol = symbol + ".NS"
                except:
                    pass
            
            # If .NS failed, try with .BO suffix (Indian BSE)
            if not ticker_obj or not info or len(info) < 5:
                try:
                    ticker_obj = yf.Ticker(symbol + ".BO")
                    info = ticker_obj.info
                    if info and len(info) > 5:
                        adjusted_symbol = symbol + ".BO"
                except:
                    pass
            
            # If still no data, return with N/A values
            if not info or len(info) < 5:
                logger.warning(f"No stock information found for {symbol}")
                return None
            
            result = {
                "name": info.get("longName", symbol),
                "sector": info.get("sector", "N/A"),
                "industry": info.get("industry", "N/A"),
                "market_cap": info.get("marketCap", "N/A"),
                "pe_ratio": info.get("trailingPE", "N/A"),
                "dividend_yield": info.get("dividendYield", "N/A"),
                "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
                "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
                "current_price": info.get("currentPrice", "N/A"),
                "description": info.get("longBusinessSummary", "No description available"),
                "website": info.get("website", "N/A"),
                "country": info.get("country", "N/A"),
                "adjusted_symbol": adjusted_symbol,  # Return which symbol worked
            }
            
            logger.debug(f"Fetched stock info for {symbol} (using {adjusted_symbol})")
            return result
        except Exception as e:
            logger.error(f"Error fetching stock info for {symbol}: {e}")
            return None
    
    @staticmethod
    @st.cache_data(ttl=3600)
    def search_stock_suggestions(query: str) -> List[Tuple[str, str]]:
        """Search for stock suggestions based on company name or ticker."""
        try:
            # Common Indian stocks
            indian_stocks = {
                "TCS": "Tata Consultancy Services",
                "INFY": "Infosys Limited",
                "WIPRO": "Wipro Limited",
                "RELIANCE": "Reliance Industries",
                "HDFC": "HDFC Bank",
                "ICICIBANK": "ICICI Bank",
                "SBIN": "State Bank of India",
                "BAJAJ-AUTO": "Bajaj Auto",
                "MARUTI": "Maruti Suzuki",
                "APOLLOHOSP": "Apollo Hospitals",
                "DMART": "DMart",
                "LT": "Larsen & Toubro",
                "ITC": "ITC Limited",
                "COALINDIA": "Coal India",
                "ONGC": "Oil and Natural Gas Corporation",
            }
            
            # Common US stocks
            us_stocks = {
                "AAPL": "Apple Inc.",
                "MSFT": "Microsoft Corporation",
                "GOOGL": "Alphabet Inc.",
                "AMZN": "Amazon.com Inc.",
                "TSLA": "Tesla Inc.",
                "META": "Meta Platforms",
                "NVDA": "NVIDIA Corporation",
                "JPM": "JPMorgan Chase",
                "JNJ": "Johnson & Johnson",
                "V": "Visa Inc.",
                "PG": "Procter & Gamble",
                "MA": "Mastercard",
                "INTC": "Intel Corporation",
                "NFLX": "Netflix Inc.",
                "BA": "Boeing Co.",
            }
            
            all_stocks = {**indian_stocks, **us_stocks}
            
            if not query:
                return []
            
            query_lower = query.lower()
            suggestions = []
            
            for ticker, name in all_stocks.items():
                if (query_lower in ticker.lower() or 
                    query_lower in name.lower()):
                    suggestions.append((ticker, name))
            
            logger.debug(f"Found {len(suggestions)} suggestions for '{query}'")
            return suggestions[:10]  # Return top 10 suggestions
        
        except Exception as e:
            logger.error(f"Error searching stock suggestions: {e}")
            return []
