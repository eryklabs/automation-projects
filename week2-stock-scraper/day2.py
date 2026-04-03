import yfinance as yf

ticker = yf.Ticker("AAPL")
hist = ticker.history(period="1y")

print(hist.head())
print(f"\nColumns:  {list(hist.columns)}")
print(f"Total rows: {len(hist)}")

# calculate moving averages from the actual historical data
hist["MA50"] = hist["Close"].rolling(window=50).mean()
hist["MA200"] = hist["Close"].rolling(window=200).mean()

# get the most recent day
latest = hist.iloc[-1]

print(f"\nLatest day: {hist.index[-1].date()}")
print(f"    Close:      ${latest['Close']:.2f}")
print(f"    MA50:       ${latest['MA50']:.2f}")
print(f"    Volume:     {int(latest['Volume']):,}")

# show the last 5 days of price vs MA50
print(f"\nLast 5 days - price vs 50MA:")
for i in range(-5, 0):
    day = hist.iloc[i]
    date = hist.index[i].date()
    above = "ABOVE" if day["Close"] > day ["MA50"] else "BELOW"
    print(f"    {date}  ${day['Close']:.2f}  vs  ${day['MA50']:.2f} - {above}")

# check MA200
latest = hist.iloc[-1]
print(f"\n  MA200:  ${latest['MA200']:.2f}")
print(f"    Above 200MA: {'YES' if latest['Close'] > latest['MA200'] else 'NO'}")

# average volume over last 20 days vs last 5
vol_20 = hist["Volume"].tail(20).mean()
vol_5 = hist["Volume"].tail(5).mean()
print(f"\n  Avg volume (20d): {int(vol_20):,}")
print(f"    Avg volume (5d):  {int(vol_5):,}")
print(f"    Volume trend:     {'INCREASING' if vol_5 > vol_20 else 'DECREASING'}")