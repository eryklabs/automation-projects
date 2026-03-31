# week1-ticker-report

A Python automation script that pulls live stock quotes from the Alpha Vantage API
and saves a formatted report to CSV. Built as the Week 1 project of a 90-day
automation engineering roadmap.

---

## What it does

- Reads a watchlist and API key from a `.env` file
- Loops through each ticker and calls the Alpha Vantage GLOBAL_QUOTE endpoint
- Prints a formatted quote to the terminal (price, open, high, low, volume, change)
- Saves all results to a timestamped CSV file
- Handles errors gracefully — rate limits, timeouts, and bad responses don't crash the script

## Usage

1. Clone the repo and navigate to this folder
2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file (never commit this):
   ```
   ALPHA_VANTAGE_KEY=your_key_here
   WATCHLIST=AAPL,NVDA,MSFT,AMD,TSLA
   ```
5. Run the script:
   ```
   python stock_report.py
   ```

## Output

Terminal output per ticker:
```
AAPL — 2026-03-30
  Price:      $246.63
  Open:       $250.07
  High:       $250.87
  Low:        $245.51
  Prev close: $248.80
  Change:     -2.1700 (-0.8722%)
  Volume:     38,097,741
```

Also saves `report_YYYY-MM-DD.csv` to the project folder.

## Rate limits

Alpha Vantage free tier: 25 requests/day, 5 requests/minute.
The script waits 12 seconds between requests to stay under the per-minute limit.

## Stack

- Python 3.12
- requests
- python-dotenv

## What I learned building this

- Calling a REST API with the `requests` library
- Parsing JSON responses and navigating nested dictionaries
- Storing secrets safely with `.env` files and `python-dotenv`
- Writing CSV output with `csv.DictWriter`
- Handling errors with `try/except` so the script doesn't crash on bad data
- Structuring code into functions — each function does one thing