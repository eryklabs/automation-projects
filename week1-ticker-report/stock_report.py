import os
import csv
import time
import requests
from datetime import date 
from dotenv import load_dotenv 

load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_KEY")
WATCHLIST = os.getenv("WATCHLIST").split(",")
TODAY = date.today()



def get_quote(ticker):
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={API_KEY}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    if "Global Quote" not in data or not data["Global Quote"]:
        raise ValueError(f"No data returned for {ticker} - possible rate limit")
    
    quote = data["Global Quote"]
    return {
        "ticker":       ticker, 
        "date":         quote["07. latest trading day"],
        "open":         float(quote["02. open"]),
        "high":         float(quote["03. high"]),
        "low":          float(quote["04. low"]),
        "price":        float(quote["05. price"]),
        "volume":       int(quote["06. volume"]),
        "prev_close":   float(quote["08. previous close"]),
        "change":       quote["09. change"],
        "change_pct":   quote["10. change percent"],
    }



def save_report(results):
    filename = f"report_{TODAY}.csv"
    fields = ["ticker","date","open","high","low","price","volume","prev_close","change","change_pct"]

    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"\nReport saved to {filename}")



def print_quote(q):
    print(f"""
    {q['ticker']} - {q['date']}
    Price:      ${q['price']:.2f}
    Open:       ${q['open']:.2f}
    High:       ${q['high']:.2f}
    Low:        ${q['low']:.2f}
    Prev close: ${q['prev_close']:.2f}
    Change:     {q['change']} ({q['change_pct']})
    Volume:     {q['volume']:,}""")


def main():
    print(f"Running stock report for {TODAY}")
    print(f"Tickers: {', '.join(WATCHLIST)}\n")

    results = []

    for ticker in WATCHLIST:
        try:
            quote = get_quote(ticker)
            print_quote(quote)
            results.append(quote)
            time.sleep(12)

        except ValueError as e:
            print(f"{ticker} - {e}")

        except requests.exceptions.HTTPError as e:
            print(f"{ticker} - HTTP error: {e}")

        except requests.exceptions.RequestException as e:
            print(f"{ticker} - request failed: {e}")

    if results:
        save_report(results)
    else:
        print("No data retrieved - nothing to save")



main()