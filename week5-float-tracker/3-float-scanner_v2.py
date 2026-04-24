import os
import time
import requests
import sqlite3
from dotenv import load_dotenv 

### WORKFLOW ###
# 1. read tickers from `symbols` table
# 2. track which ones have already been scanned
# 3. pick the next 249 that need scanning
# 4. run those, then stop for the day

# this script: 
# 1. connects to the database
# 2. queries 249 tickers that haven't been scanned (API limit is 250 calls a day)
# 3. loop through all those tickers, calls `get_float()` for each, inserts into `float_snapshots`
# 4. `time.sleep(2)` between calls, and print progress as it goes along

# 2026-04-24 v2: adding error handling for HTTP errors and counter at the end that prints a summary

load_dotenv()

API_KEY = os.getenv("FMP_API_KEY")

con = sqlite3.connect("float_tracker.db")
cur = con.cursor()

start = time.time()   # for timing how long this script takes



cur.execute("""
    SELECT ticker FROM symbols
    WHERE ticker NOT IN (SELECT DISTINCT symbol FROM float_snapshots)
    LIMIT 249
    """) 


tickers = cur.fetchall()
print(f"Tickers to scan: {len(tickers)}")



# get float for each symbol
def get_float(symbol):
    url = f"https://financialmodelingprep.com/stable/shares-float?symbol={symbol}&apikey={API_KEY}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    return data

# creating variables for summary at end (tickers succeeded and tickers failed)
tickers_failed = []
counter_failed = 0
counter_succeeded = 0

for i, ticker in enumerate(tickers):
    symbol = ticker[0]                  # extract string from tuple

    # error handling logic, since `result[0]` fails sometimes and crashes script (2026-04-24)
    try:
        result = get_float(symbol)
    except requests.exceptions.RequestException as e:
        print(f"{i+1}/{len(tickers)} - {symbol} FAILED ({e})")
        tickers_failed.append(symbol)   # add symbol to the `tickers_failed` tuple for end summary
        counter_failed += 1             # increment `counter_failed` by 1
        time.sleep(2)                   # avoid rate limiting
        continue

    if not result:                      # adding error handling, since `result[0]` fails sometimes and crashes script (2026-04-24)
        print(f"{i+1}/{len(tickers)} - {symbol} SKIPPED (no data)")
        tickers_failed.append(symbol)   # add symbol to the `tickers_failed` tuple for end summary
        counter_failed += 1             # increment `counter_failed` by 1
        time.sleep(2)                   # avoid rate limiting
        continue

    record = result[0]

    cur.execute("""
        INSERT INTO float_snapshots
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            record["symbol"],
            record["floatShares"],
            record["freeFloat"],
            record["outstandingShares"],
            record["source"],
            int(time.time()),
            record["date"]
        ))
    
    print(f"{i+1}/{len(tickers)} - {symbol} done")
    counter_succeeded += 1
    time.sleep(2)

    con.commit()



# print summary (time elapsed + tickers succeeded and tickers failed)
elapsed = time.time() - start   # time elapsed since start of script
print(f"\nFloat Scanner completed 249 queries in {elapsed} seconds.\n")
print(f"Tickers added to database: {counter_succeeded}\n")
print(f"Tickers skipped due to failure: {counter_failed}\n")
print("    Tickers failed:")
for ticker in tickers_failed:
    print(f"        {ticker}")