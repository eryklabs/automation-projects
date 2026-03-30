from datetime import date

today = date.today()

watchlist = ["AAPL", "NVDA", "MSFT", "AMD", "TSLA", "JPM", "BAC"]

def format_ticker_report(ticker, date):
    return f"{ticker}, {date}, pending"

for ticker in watchlist:
    print(format_ticker_report(ticker, today))


filename = f"report_{today}.txt"

with open(filename, "w") as f:
    for ticker in watchlist:
        line = format_ticker_report(ticker, today)
        f.write(line + "\n")
        

print(f"\nReport saved to {filename}")