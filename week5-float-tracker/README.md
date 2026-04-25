# Float Tracker

Automated tool that snapshots stock float data on a daily schedule and stores it in a local SQLite database, building a personal historical dataset over time. Built to support investing research - specifically tracking float changes (dilution, buybacks) as one variable in a broader investment analysis workflow.

## Why

Float data is easy to look up for a single stock on any given day. What's hard to get for free is *historical* float data - how a company's float has changed over weeks and months. Most providers either don't offer it or charge for it.

This tool solves that by snapshotting current float data for every US-listed ticker on a recurring schedule. Run it long enough and you've built your own float history dataset.

## How it works

The system uses two free data sources:

- **SEC EDGAR** for the master ticker list (`company_tickers.json`) - a complete list of every SEC-registered company with ticker, name, and CIK. Free, no API key required, ~10,341 tickers.
- **Financial Modeling Prep (FMP)** for actual float data, via the per-symbol `/stable/shares-float` endpoint. Free tier allows 250 API calls per day.

Because FMP limits free users to 250 calls/day, the scanner cycles through the full ticker list 249 tickers at a time, taking ~42 days for a complete sweep. Each run picks the next batch of unscanned tickers and inserts a snapshot into SQLite. Tickers that return no data (foreign ADRs, ETFs, delisted stocks) are flagged in the database so they don't get retried and waste API calls.

A cron job on a Proxmox Debian VM runs the scanner daily at 7am.

## Data source

FMP's `/stable/shares-float?symbol=AAPL` endpoint returns `symbol`, `date`, `freeFloat`, `floatShares`, `outstandingShares`, and `source` (a link to the SEC filing the data was pulled from).

FMP does not provide historical float series - only current values. The entire point of this tool is to create that history yourself by snapshotting repeatedly.

## Tech stack

- Python 3.13
- SQLite (via Python's built-in `sqlite3`)
- `requests` and `python-dotenv`
- Cron on Debian (Proxmox VM)
- FMP API (free tier) + SEC EDGAR

## Project structure

```
week5-float-tracker/
├── 1-call-api.py           # initial API exploration script
├── 2-get-tickers.py        # pulls SEC ticker list, populates `symbols` table
├── 3-float-scanner_v4.py   # main scanner - runs daily via cron
├── float_tracker.db        # SQLite database (gitignored)
├── .env                    # API key (gitignored)
└── README.md
```

## Database schema

**`symbols`** - master list of all SEC-registered tickers
- `ticker` TEXT
- `title` TEXT (company name)
- `cik` INTEGER (SEC Central Index Key)
- `retrieved_at` INTEGER (unix timestamp)
- `scan_status` TEXT (defaults to `'pending'`, set to `'no_data'` if FMP returns no float data)

**`float_snapshots`** - append-only table of float data over time
- `symbol` TEXT
- `float_shares` INTEGER
- `free_float` REAL (percentage)
- `outstanding_shares` INTEGER
- `source` TEXT (URL to SEC filing)
- `retrieved_at` INTEGER (unix timestamp)
- `date` TEXT (FMP's reported date for the data)

## Setup

1. Get a free API key from [financialmodelingprep.com](https://financialmodelingprep.com/developer/docs/)
2. Clone the repo and create a virtual environment:

```bash
git clone https://github.com/eryklabs/automation-projects.git
cd automation-projects/week5-float-tracker
python3 -m venv .venv
source .venv/bin/activate
pip install requests python-dotenv
```

3. Create `.env`:

```
FMP_API_KEY=your_key_here
```

4. Populate the `symbols` table from SEC EDGAR (one-time):

```bash
python3 2-get-tickers.py
```

5. Run the scanner manually to confirm everything works:

```bash
python3 3-float-scanner_v4.py
```

6. Set up a cron job to run daily:

```bash
crontab -e
```

Add:

```
0 7 * * * cd /path/to/week5-float-tracker && /path/to/week5-float-tracker/.venv/bin/python3 3-float-scanner_v4.py >> /path/to/week5-float-tracker/cron.log 2>&1
```

## Querying the data

```sql
-- How many tickers have been scanned
SELECT COUNT(DISTINCT symbol) FROM float_snapshots;

-- Tickers with the lowest free float (most insider/institutional ownership)
SELECT symbol, free_float, float_shares, outstanding_shares
FROM float_snapshots
WHERE float_shares > 0
ORDER BY free_float ASC
LIMIT 20;

-- Tickers still pending a scan
SELECT COUNT(*) FROM symbols
WHERE ticker NOT IN (SELECT DISTINCT symbol FROM float_snapshots)
  AND scan_status != 'no_data';

-- Once enough data has accumulated: float changes over time for a ticker
SELECT symbol, retrieved_at, float_shares
FROM float_snapshots
WHERE symbol = 'AAPL'
ORDER BY retrieved_at DESC;
```

## Status

- [x] SEC ticker list ingestion
- [x] Per-symbol FMP float scanning
- [x] SQLite schema with two tables
- [x] Error handling (HTTP errors, empty responses)
- [x] `no_data` flag to skip dead tickers on future runs
- [x] Run summary with success/failure counts and rate
- [x] Cron job deployed on Proxmox VM
- [ ] Logging module instead of print + cron.log
- [ ] Re-scan logic for second pass after first sweep completes
- [ ] Periodic retry of `no_data` tickers (in case FMP gets data later)
- [ ] Database backups to TrueNAS
- [ ] Failure notifications (Discord/email webhook)
- [ ] Phase 2: EPS tracking via SEC EDGAR XBRL data
