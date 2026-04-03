import yfinance as yf
from dotenv import load_dotenv
import os
import csv 
from datetime import date

load_dotenv()
WATCHLIST = os.getenv("WATCHLIST").split(",")

def full_analysis(symbol):
    ticker = yf.Ticker(symbol)
    info = ticker.info
    hist = ticker.history(period="1y")

    if len(hist) < 50:
        print(f"\n{symbol} - not enough data, skipping")
        return None
    
    hist["MA50"] = hist["Close"].rolling(window=50).mean()
    hist["MA200"] = hist["Close"].rolling(window=200).mean()

    latest = hist.iloc[-1]
    price = latest["Close"]
    ma50 = latest["MA50"]
    ma200 = latest["MA200"] if len(hist) >= 200 else 0

    vol_20 = hist["Volume"].tail(20).mean()
    vol_5 = hist["Volume"].tail(5).mean()

    above_50 = price > ma50
    above_200 = price > ma200 if ma200 > 0 else False
    beta = info.get("beta", 0)
    earnings_growth = info.get("earningsGrowth", 0)
    forward_pe = info.get("forwardPE", 0)

    passes = above_50 and above_200 and beta < 2.0 and earnings_growth > 0.10

    print(f"\n{'='*40}")
    print(f"{symbol} - {'PASS' if passes else 'SKIP'}")
    print(f"{'='*40}")
    print(f"    Price:      ${price:.2f}")
    print(f"    50MA:       ${ma50:.2f} {'ABOVE' if above_50 else 'BELOW'}")
    if ma200 > 0:
        print(f"    200MA:      ${ma200:.2f} {'ABOVE' if above_200 else 'BELOW'}")
    print(f"    Beta:       {beta}")
    print(f"    Forward PE: {forward_pe}")
    print(f"    EPS Growth: {earnings_growth}")
    print(f"    Vol trend:  {'UP' if vol_5 > vol_20 else 'DOWN'}")

    return {
        "symbol": symbol, 
        "passes": passes, 
        "price": round(price, 2),
        "ma50": round(ma50, 2), 
        "ma200": round(ma200, 2) if ma200 > 0 else "N/A", 
        "beta": beta, 
        "forward_pe": round(forward_pe, 2) if forward_pe else 0,
        "eps_growth": earnings_growth,
        "vol_trend": "UP" if vol_5 > vol_20 else "DOWN"
        }


def save_to_csv(results):
    filename = f"scan_{date.today()}.csv"
    fields = ["symbol", "passes", "price", "ma50", "ma200", "beta", "forward_pe", "eps_growth", "vol_trend"]

    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nSaved to {filename}")


results = []
for symbol in WATCHLIST:
    result = full_analysis(symbol)
    if result:
        results.append(result)

print(f"\n\n{'='*40}")
print("SUMMARY")
print(f"{'='*40}")
passing = [r for r in results if r["passes"]]
print(f"Passing: {', '.join(r['symbol'] for r in passing) if passing else 'None'}")
print(f"Total screened: {len(results)}")

if results:
    save_to_csv(results)