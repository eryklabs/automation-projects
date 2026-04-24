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

load_dotenv()

API_KEY = os.getenv("FMP_API_KEY")

con = sqlite3.connect("float_tracker.db")
cur = con.cursor()



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


for i, ticker in enumerate(tickers):
    symbol = ticker[0]      # extract string from tuple

    result = get_float(symbol)

    if not result:          # adding error handling, since `result[0]` fails sometimes and crashes script (2026-04-24)
        print(f"{i+1}/{len(tickers)} - {symbol} SKIPPED (no data)")
        time.sleep(2)
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
    time.sleep(2)

    con.commit()




