# Float Tracker

Automated tool that snapshots stock float data on a schedule and stores it locally, building a personal historical dataset over time. Built to support LEAPS options research — specifically tracking float changes (dilution, buybacks) as one variable in a broader investment analysis workflow.

## Why

Float data is easy to look up for a single stock on any given day. What's hard to get for free is *historical* float data — how a company's float has changed over weeks and months. Most providers either don't offer it or charge for it.

This tool solves that by snapshotting current float data on a recurring schedule and appending it to a local SQLite database. Run it long enough and you've built your own float history dataset.

## How it works

- Pulls float data from [Financial Modeling Prep](https://financialmodelingprep.com/)'s bulk shares-float endpoint
- Stores each snapshot in SQLite with timestamps, so every run adds a new layer of history
- Runs as a Docker container triggered by cron on a Proxmox Debian VM
- Each run is logged in an `ingestion_runs` table for auditing and debugging

## Data source

FMP's `/stable/shares-float-all` endpoint returns `symbol`, `freeFloat`, `floatShares`, and `outstandingShares`. The free tier currently returns ~86 large/mid-cap tickers. Paid tiers cover broader universes.

FMP does not provide historical float series — only current values. The entire point of this tool is to create that history yourself by snapshotting repeatedly.

## Current status

**In progress.** Building step by step as a learning project (Python, SQLite, Docker, cron, API integration).

- [x] API connection to FMP bulk float endpoint
- [ ] SQLite schema and storage
- [ ] Pagination and full data ingestion
- [ ] Docker container
- [ ] Cron job on Proxmox VM
- [ ] Change detection queries (float deltas between runs)

## Planned

- **Phase 2:** EPS tracking using SEC EDGAR bulk XBRL data (`companyfacts.zip`), bolted onto the same pipeline and symbol table
- **Broader coverage:** Upgrade to paid FMP tier or swap in additional data sources to cover the full US-listed universe (~8,000-10,000 tickers)

## Tech stack

- Python 3.13
- SQLite (via Python's built-in `sqlite3`)
- Docker on Debian (Proxmox VM)
- Cron for scheduling
- FMP API (free tier)

## Project structure

```
float-tracker/
├── src/
│   ├── main.py           # entry point — orchestrates each ingestion run
│   ├── db.py             # SQLite schema and connection
│   └── fmp.py            # FMP API client
├── Dockerfile
├── requirements.txt
├── .env                  # API key (not committed)
├── .gitignore
└── data/                 # SQLite database lives here (not committed)
```

## Setup

1. Get a free API key from [financialmodelingprep.com](https://financialmodelingprep.com/developer/docs/)
2. Copy `.env.example` to `.env` and add your key
3. Build and run with Docker:

```bash
docker build -t float-tracker .
mkdir -p data
docker run --rm --env-file .env -v $(pwd)/data:/data float-tracker
```

4. Set up cron for recurring runs (e.g., every 2 weeks):

```bash
crontab -e
# Add: 0 2 */14 * * docker run --rm --env-file /path/to/.env -v /path/to/data:/data float-tracker >> /path/to/data/cron.log 2>&1
```

## Querying the data

```sql
-- Latest float for a specific stock
SELECT * FROM float_snapshots WHERE symbol = 'AAPL' ORDER BY as_of_date DESC LIMIT 5;

-- Stocks where float changed between the two most recent runs
SELECT
    a.symbol,
    a.float_shares AS prev_float,
    b.float_shares AS curr_float,
    b.float_shares - a.float_shares AS change
FROM float_snapshots a
JOIN float_snapshots b ON a.symbol = b.symbol
WHERE a.run_id = (SELECT MAX(run_id) - 1 FROM ingestion_runs WHERE status = 'success')
  AND b.run_id = (SELECT MAX(run_id) FROM ingestion_runs WHERE status = 'success')
  AND a.float_shares != b.float_shares
ORDER BY ABS(b.float_shares - a.float_shares) DESC;
```
