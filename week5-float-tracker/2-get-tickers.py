import requests
import json
import time
import sqlite3

# Get a list of all stock tickers directly from the SEC
# 2026-04-23 - thurs


con = sqlite3.connect("float_tracker.db")
cur = con.cursor()



response = requests.get(
    "https://www.sec.gov/files/company_tickers.json",
    headers={"User-Agent": "BobBobski bobbobski22532@gmail.com"}
)

data = response.json()
print(f"Total tickers: {len(data)}")

# Print first 5 (for testing)
#for key in list(data.keys())[:5]:
#    print(data[key])

# save to JSON file to analyze data
with open("tickers.json", "w") as f:
    json.dump(data, f, indent=2)



# saving tickers to SQLite database so float tracker script can read from it
# cik = Central Index Key (a unique identifier assigned by the U.S. Securities and Exchange Commission (SEC) to companies, funds, insiders, and entities that file with the SEC)
cur.execute("""
            CREATE TABLE IF NOT EXISTS symbols(
                ticker TEXT, 
                title TEXT, 
                cik INTEGER,  
                retrieved_at INTEGER)
            """)

con.commit()


# insert all SEC data (10,000+ tickers) into our `symbols` database
for key in data:
    record = data[key]

    cur.execute("""
        INSERT INTO symbols
        VALUES (?, ?, ?, ?)
        """, (
            record["ticker"],
            record["title"],
            record["cik_str"],
            int(time.time())
        ))

con.commit()

cur.execute("SELECT COUNT(*) FROM symbols")
print(cur.fetchone())
