import yfinance as yf

ticker = yf.Ticker("AAPL")
info = ticker.info

for key in sorted(info.keys()):
    print(f"{key}: {info[key]}")






