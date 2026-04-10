# Reddit Comment Aggregator

Personal tool for collecting and analyzing Reddit comments, based on a question posted to one (or multiple) subreddits. 

## Problem

Reddit is a great place to get high-level responses on questions about real-world, real-time problems. 
The problem is, sometimes there are 50-100 replies, and it can take hours to read though each one and research suggested solutions. 

## Solution

Automated pipeline that extracts, ranks, and summarizes highly-focused suggestions.

## What it does

When I post a question to multiple subreddits (5-10), this tool:

1. **Scrapes** all comments from each thread using Reddit's public JSON endpoints (no API key needed)
2. **Saves** the raw data locally as JSON for re-analysis later
3. **Generates** a ranked markdown report — comments sorted by score, subreddits sorted by engagement, with clickable links to each thread 
4. **Analyzes** all comments using a local LLM (Ollama/qwen3) to find consensus, top recommendations, contrarian insights, and action items. Can link to Claude or other AI if desired.

## Usage

### Step 1: Add URLs

Paste your Reddit post URLs into `urls.txt`, one per line:

```
https://www.reddit.com/r/homelab/comments/abc123/my_question/
https://www.reddit.com/r/truenas/comments/def456/my_question/
https://www.reddit.com/r/selfhosted/comments/ghi789/my_question/
```

### Step 2: Scrape

```bash
python scrape.py
```

Fetches all comments, filters deleted/removed, saves to `data/scan_TOPIC_YYYY-MM-DD.json`.

### Step 3: Analyze

```bash
python analyze.py
```

Generates:
- `data/report_TOPIC_YYYY-MM-DD.md` — ranked comment report for manual scanning
- `data/analysis_TOPIC_YYYY-MM-DD.txt` — LLM-generated summary and recommendations

Edit the `TOPIC` variable at the top of each script before running (e.g., `TOPIC = "best-vpn"`, `TOPIC = "best-os-for-nas"`).

## Requirements

- Python 3.9+
- `requests` (for HTTP calls)
- Ollama running locally with `qwen3:14b` (for analysis step only)
- Need to run scrape.py and analyze.py on same day (due to date being part of file naming system). You can also rename files to have matching dates, if need be. 

```bash
pip install -r requirements.txt
```

## How it works

- Uses Reddit's public `.json` endpoint — appends `.json` to any Reddit URL to get structured data
- No API key, no OAuth, no approval process needed
- Randomized delays between requests to avoid rate limiting
- Deleted/removed comments filtered out before analysis
- Comments include vote scores so the LLM can identify both consensus and contrarian viewpoints

## File structure

```
reddit-aggregator/
  scrape.py           # fetches comments from Reddit
  analyze.py          # generates report + LLM analysis
  urls-example.txt    # input: list of Reddit post URLs (example)
  requirements.txt    # Python dependencies
  data/               # output: JSON scans, reports, analyses (gitignored)
```