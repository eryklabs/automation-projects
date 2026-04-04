import yfinance as yf
from dotenv import load_dotenv
from datetime import date, datetime
import os
import csv

load_dotenv()
WATCHLIST = os.getenv("WATCHLIST").split(",")

# Full Pipeline: Screen every ticker --> identify which pass --> automatically pull LEAPS chains for the winners 
#                --> show ITM strikes with intrinsic/time value breakdown

def screen_ticker(symbol):
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

    print(f"\n{'='*50}")
    print(f"{symbol} --- {'PASS' if passes else 'SKIP'}")
    print(f"{'='*50}")
    print(f"   Price:       ${price:.2f}")
    print(f"   50MA:        ${ma50:.2f}   {'ABOVE' if above_50 else 'BELOW'}")
    if ma200 > 0:
        print(f"   200MA:       ${ma200:.2f}   {'ABOVE' if above_50 else 'BELOW'}")
    print(f"   Beta:        {beta}")
    print(f"   Forward PE:  {forward_pe}")
    print(f"   EPS Growth:  {earnings_growth}")
    print(f"   Vol Trend:   {'UP' if vol_5 > vol_20 else 'DOWN'}")

    return {
        "symbol": symbol, 
        "passes": passes,
        "price": round(price, 2),
        "ticker_obj": ticker
    }

def find_leaps_expiration(ticker):
    expirations = ticker.options
    today = date.today()

    leaps = []
    for exp in expirations:
        exp_date = datetime.strptime(exp, "%Y-%m-%d").date()
        days_out = (exp_date - today).days
        # filters to only 365+ days out, since we only want to look at LEAPS
        if days_out >= 365:                                 
            leaps.append(exp)
    
    return leaps 

def analyze_leaps(ticker, symbol, price, exp_date):
    chain = ticker.option_chain(exp_date)
    calls = chain.calls

    near_money = calls[(calls["strike"] >= price * 0.7) & (calls["strike"] <= price * 1.0)]   

    print(f"\n  LEAPS calls expiring {exp_date}:")
    print(f"    {'Strike':<10} {'Bid':<10} {'Ask':<10} {'Last':<10} {'IV':<10} {'OI':<10} {'Intrinsic':<12} {'Time Val':<12} {'Time %'}")
    print(f"    {'-'*82}")

    for _, row in near_money.iterrows():
        intrinsic = max(price - row["strike"], 0)
        time_value = row["ask"] - intrinsic
        time_pct = (time_value / row["ask"] * 100) if row["ask"] > 0 else 0

        print(f"    ${row['strike']:<9} ${row['bid']:<9} ${row['ask']:<9} ${row['lastPrice']:<10} {row['impliedVolatility']:.2%}    {int(row['openInterest']):<10} ${intrinsic:<11.2f} ${time_value:<11.2f} {time_pct:.0f}%")



# --- MAIN ---
print(f"LEAPS SCREENER - {date.today()}")
print(f"Watchlist: {', '.join(WATCHLIST)}\n")

results = []
for symbol in WATCHLIST:
    result = screen_ticker(symbol)
    if result:
        results.append(result)

passing = [r for r in results if r["passes"]]

print(f"\n\n{'='*50}")
print("SCREENING COMPLETE")
print(f"{'='*50}")
print(f"Screened: {len(results)}")
print(f"Passing: {', '.join(r['symbol'] for r in passing) if passing else 'None'}")

if passing:
    print(f"\n\nPulling LEAPS data for passing tickers...")

    for r in passing:
        exps = find_leaps_expiration(r["ticker_obj"])
        if exps:
            print(f"\n{'='*50}")
            print(f"{r['symbol']} - LEAPS expirations available: {len(exps)}")
            print(f"{'='*50}")

            # analyze the two furthest-out expirations
            for exp in exps:
                analyze_leaps(r["ticker_obj"], r["symbol"], r["price"], exp)
        else: 
            print(f"\n{r['symbol']} - no LEAPS expirations found")
else:
    print("\nNo tickers passed screening - no LEAPS to analyze")

