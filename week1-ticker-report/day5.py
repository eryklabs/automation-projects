import os
import requests
import ssl
import certifi
import time
import json
from dotenv import load_dotenv

load_dotenv()


api_key = os.getenv("ALPHA_VANTAGE_KEY")
watchlist_raw = os.getenv("WATCHLIST")
watchlist = watchlist_raw.split(",")

print(f"Loaded {len(watchlist)} tickers from .env")
print(f"API key loaded: {'yes' if api_key else 'NO - CHECK YOUR .env FILE'}")

for ticker in watchlist:
    try:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={api_key}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        # print(json.dumps(data, indent=2))     # using this for visualizing what the API was giving us)
        # break # only print the first ticker so we're not flooded <-- (was using this for visualizing what the API was giving us)
        quote = data["Global Quote"]
        
        price = quote["05. price"]
        change = quote["10. change percent"]
        volume = quote["06. volume"]
        
        #print(f"{ticker}: ${float(price):.2f} | change: {change} | volume: {int(volume):,}")  # (old version)
        print(f"""
              {ticker}
                Price:          ${float(price):.2f}
                Open:           ${float(quote['02. open']):.2f}
                High:           ${float(quote['03. high']):.2f}
                Low:            ${float(quote['04. low']):.2f}
                Prev close:     ${float(quote['08. previous close']):.2f}
                Change:         {change}
                Volume:         {int(volume):,}
                Trading day:    {quote['07. latest trading day']}
            """)
        time.sleep(12)  # wait 12 seconds between requests

    except requests.exceptions.Timeout:
        print(f"{ticker} - timed out, skipping")

    except requests.exceptions.HTTPError as e:
        print(f"{ticker} - HTTP error: {e}")

    except KeyError:
        print(f"{ticker} - unexpected response: {data}")

    except requests.exceptions.RequestException as e:
        print(f"{ticker} - something went wrong: {e}")

