import os
import requests
import sqlite3
import time
from dotenv import load_dotenv 

load_dotenv()

API_KEY = os.getenv("FMP_API_KEY")

con = sqlite3.connect("float_tracker.db")
cur = con.cursor()

# Creating `float_snapshots` table, a SQLite database of float data that we are tracking
# `retrieved at` = when we retrieved this data
# `date` = when FMP last updated their tickers data
cur.execute("""
            CREATE TABLE IF NOT EXISTS float_snapshots(
                symbol TEXT, 
                float_shares INTEGER, 
                free_float REAL, 
                outstanding_shares INTEGER, 
                source TEXT, 
                retrieved_at INTEGER, 
                date TEXT)
            """)



cur.execute("""
            INSERT INTO float_snapshots
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                "MSFT", 
                7400000000, 
                99.1, 
                7470000000, 
                "manual_test", 
                int(time.time()), 
                "2026-04-18"
            ))

con.commit()



cur.execute("SELECT * FROM float_snapshots WHERE symbol = ?", ("MSFT",))
rows = cur.fetchall()

print(rows)


# get float for each symbol
def get_float(symbol):
    url = f"https://financialmodelingprep.com/stable/shares-float?symbol={symbol}&apikey={API_KEY}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    return data


result = get_float("AAPL")
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

con.commit()

cur.execute("SELECT * FROM float_snapshots WHERE symbol = ?", ("AAPL",))
print(cur.fetchall())