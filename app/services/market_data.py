
import yfinance as yf
import pandas as pd
import pandas_ta as ta
from functools import lru_cache

@lru_cache(maxsize=128)
def get_stock_price(symbol: str):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1d")
        if hist.empty:
            return {"error": f"No price data found for {symbol}"}
        price = hist["Close"].iloc[-1]
        prev = hist["Open"].iloc[-1]
        change = price - prev
        pct_change = (change / prev) * 100 if prev else 0
        return {
            "symbol": symbol.upper(),
            "price": round(price, 2),
            "day_change": round(change, 2),
            "percent_change": round(pct_change, 2)
        }
    except Exception as e:
        return {"error": str(e)}

@lru_cache(maxsize=128)
def get_company_overview(symbol: str):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        return {
            "symbol": symbol.upper(),
            "name": info.get("shortName", "N/A"),
            "description": info.get("longBusinessSummary", "No description available."),
            "market_cap": info.get("marketCap", "N/A"),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "dividend_yield": info.get("dividendYield", "N/A"),
            "industry": info.get("industry", "N/A"),
            "sector": info.get("sector", "N/A")
        }
    except Exception as e:
        return {"error": f"Failed to load company info for {symbol}: {str(e)}"}

@lru_cache(maxsize=128)
def get_technical_analysis(symbol: str):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="6mo")
        if hist.empty:
            return {"error": f"No data found for {symbol}"}
        df = hist[["Close"]].copy()
        df["SMA_50"] = ta.sma(df["Close"], length=50)
        df["SMA_200"] = ta.sma(df["Close"], length=200)
        df["RSI"] = ta.rsi(df["Close"], length=14)
        macd = ta.macd(df["Close"])
        bbands = ta.bbands(df["Close"])
        return {
            "sma_50": round(df["SMA_50"].iloc[-1], 2) if not df["SMA_50"].isna().iloc[-1] else "N/A",
            "sma_200": round(df["SMA_200"].iloc[-1], 2) if not df["SMA_200"].isna().iloc[-1] else "N/A",
            "rsi": round(df["RSI"].iloc[-1], 2) if not df["RSI"].isna().iloc[-1] else "N/A",
            "macd": round(macd["MACD_12_26_9"].iloc[-1], 2) if not macd["MACD_12_26_9"].isna().iloc[-1] else "N/A",
            "bollinger_bands": {
                "upper": round(bbands["BBU_20_2.0"].iloc[-1], 2) if not bbands["BBU_20_2.0"].isna().iloc[-1] else "N/A",
                "lower": round(bbands["BBL_20_2.0"].iloc[-1], 2) if not bbands["BBL_20_2.0"].isna().iloc[-1] else "N/A"
            },
            "signal": "buy" if df["RSI"].iloc[-1] < 30 else "sell" if df["RSI"].iloc[-1] > 70 else "hold"
        }
    except Exception as e:
        return {"error": str(e)}


import os
import requests

def get_news(symbol: str):
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        return [{"headline": "NewsAPI key is not set.", "sentiment": "neutral"}]

    try:
        response = requests.get(
            "https://newsapi.org/v2/everything",
            params={{"q": symbol, "sortBy": "publishedAt", "pageSize": 5, "apiKey": api_key}}
        )
        data = response.json()
        articles = data.get("articles", [])
        return [
            {{"headline": a["title"], "sentiment": "neutral"}} for a in articles if "title" in a
        ] or [{"headline": "No news articles found.", "sentiment": "neutral"}]
    except Exception as e:
        return [{"headline": f"News API error: {str(e)}", "sentiment": "neutral"}]
def get_fundamentals(symbol: str):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        return {
            "eps": info.get("trailingEps", "N/A"),
            "revenue": info.get("totalRevenue", "N/A"),
            "profit_margin": info.get("profitMargins", "N/A"),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "peg_ratio": info.get("pegRatio", "N/A"),
            "ev_to_ebitda": info.get("enterpriseToEbitda", "N/A"),
            "analyst_rating": info.get("recommendationKey", "N/A"),
            "target_price": info.get("targetMeanPrice", "N/A")
        }
    except Exception as e:
        return {"error": f"Failed to get fundamentals for {symbol}: {str(e)}"}

def get_watchlist(user_id: str):
    return ["AAPL", "TSLA", "GOOGL"]

def add_to_watchlist(user_id: str, symbol: str):
    return {"message": f"{symbol.upper()} added to watchlist."}

def remove_from_watchlist(user_id: str, symbol: str):
    return {"message": f"{symbol.upper()} removed from watchlist."}

def get_alerts(user_id: str):
    return [{"symbol": "TSLA", "condition": "price > 300", "type": "price"}]

def add_alert(user_id: str, symbol: str, condition: str):
    return {"message": f"Alert set for {symbol.upper()} when {condition}."}

def remove_alert(user_id: str, symbol: str):
    return {"message": f"Alert removed for {symbol.upper()}."}
