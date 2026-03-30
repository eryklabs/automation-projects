from datetime import date

today = date.today()

watchlist = ["AAPL", "NVDA", "MSFT", "AMD", "TSLA", "JPM", "BAC", "INTC"]

semiconductors = ["NVDA", "AMD", "INTC"]
banks = ["JPM", "BAC"]
volatile = ["TSLA"]

for ticker in watchlist: 
    if ticker in semiconductors: 
        print(f"{ticker} - semiconductor, check IV rank")
    elif ticker in banks:
        print(f"{ticker} - financials, check earnings date")
    elif ticker in volatile:
        print(f"TSLA - volatile, check carefully")
    else: 
        print(f"{ticker} - tech, standard scan")


# long way
semi_list = []
for ticker in watchlist:
    if ticker not in semiconductors and ticker not in banks:
        semi_list.append(ticker)

# same thing, one line
semi_list_short = [ticker for ticker in watchlist if ticker not in semiconductors and ticker not in banks]

print(f"\nNew watchlist: {semi_list}")
print(f"Same result, shorter: {semi_list_short}")