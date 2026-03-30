from datetime import date

today = date.today()
watchlist = ["AAPL", "NVDA", "MSFT", "AMD", "TSLA"]

for ticker in watchlist:
    print(f"Running scan for {ticker} on {today}")

