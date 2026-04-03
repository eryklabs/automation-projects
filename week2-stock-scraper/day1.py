import yfinance as yf
from dotenv import load_dotenv
import os

load_dotenv()
WATCHLIST = os.getenv("WATCHLIST").split(",")

fields = [
    "symbol",
    "currentPrice",
    "fiftyTwoWeekHigh",
    "fiftyTwoWeekLow",
    "fiftyDayAverage",
    "twoHundredDayAverage",
    "marketCap",
    "trailingPE",
    "forwardPE",
    "priceToBook",
    "earningsGrowth",
    "revenueGrowth",
    "returnOnEquity",
    "debtToEquity",
    "beta",
]

def analyze(symbol):
    ticker = yf.Ticker(symbol)
    info = ticker.info

    price = info.get("currentPrice", 0)
    ma50 = info.get("fiftyDayAverage", 0)
    ma200 = info.get("twoHundredDayAverage", 0)
    week52high = info.get("fiftyTwoWeekHigh", 0)
    week52low = info.get("fiftyTwoWeekLow", 0)
    beta = info.get("beta", 0)
    forward_pe = info.get("forwardPE", 0)
    earnings_growth = info.get("earningsGrowth", 0)
    marketcap = info.get("marketCap", 0)
    pricetobook = info.get("priceToBook", 0)
    revenuegrowth = info.get("revenueGrowth", 0)
    returnonequity = info.get("returnOnEquity", 0)
    debttoequity = info.get("debtToEquity", 0)

    above_50 = price > ma50
    above_200 = price > ma200
    week_range_pct = ((price - week52low) / (week52high - week52low)) * 100 if (week52high - week52low) > 0 else 0
    passes = above_50 and above_200 and beta < 2.0 and earnings_growth > 0.10

    print(f"\n{symbol}")
    print(f"    Price:              ${price:.2f}")
    print(f"    Above 50MA:         {'YES' if above_50 else 'NO'}")
    print(f"    Above 200MA:        {'YES' if above_200 else 'NO'}")
    print(f"    52wk pos:           {week_range_pct:.1f}%")
    print(f"    Beta:               {beta}")
    print(f"    Forward PE:         {forward_pe:.2f}")
    print(f"    EPS growth:         {earnings_growth}")
    print(f"    LEAPS signal:       {'PASS' if passes else 'SKIP'}")
    print(f"    Market Cap:         ${marketcap:,}")
    print(f"    Price to Book:      {pricetobook:.2f}")
    print(f"    Revenue Growth:     {revenuegrowth}")
    print(f"    Return on Equity:   {returnonequity:.2f}")
    print(f"    Debt to Equity:     {debttoequity:.2f}")

for symbol in WATCHLIST:
    analyze(symbol)
