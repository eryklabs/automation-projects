import yfinance as yf

ticker = yf.Ticker("AMD")

# see all available expiration dates
expirations = ticker.options
print("Available expirations:")
for exp in expirations:
    print(f" {exp}")

# pick a LEAPS expiration
exp_date = "2028-01-21"

chain = ticker.option_chain(exp_date)
calls = chain.calls

print(f"\nCALLS for AMD expiring {exp_date}")
print(f"Total strikes: {len(calls)}\n")

# show the colums available
print(f"Columns: {list(calls.columns)}\n")

# show strikes near the current price
price = ticker.info.get("currentPrice", 0)
print(f"Current price: ${price:.2f}\n")

# filter to strikes within 20% of current price
near_money = calls[(calls["strike"] >= price * 0.8) & (calls["strike"] <= price * 1.2)]

for _, row in near_money.iterrows():
    print(f"    Strike: ${row['strike']:<10} Bid: ${row['bid']:<10} Ask: ${row['ask']:<10} Last Price: ${row['lastPrice']:<10} IV: {row['impliedVolatility']:<10,.2%} OI: {row['openInterest']}")

print(f"\n--- LEAPS value check ---")
for _, row in near_money.iterrows():
    intrinsic = max(price - row["strike"], 0)
    time_value = row["ask"] - intrinsic
    print(f"   ${row['strike']:<8} intrinsic: ${intrinsic:<10.2f} time value: ${time_value:<10.2f} ({time_value/row['ask']*100:.0f}% of premium)")