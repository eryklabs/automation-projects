# automation-projects

Personal automation and data engineering portfolio. Eight self-directed projects spanning Python scripting, API integration, ETL pipelines, LLM integration, Linux deployment, and homelab tooling. Built between February and April 2026 as a structured self-taught path toward Cybersecurity/Data/Automation Engineer roles.

---

## Highlights

- **Production-deployed ETL pipeline** running daily on a self-hosted Debian VM via cron
- **End-to-end LLM pipelines** combining local models (Ollama/Qwen3) and cloud APIs (Anthropic Claude)
- **Real working tools I use personally**, not tutorial projects
- **Stack:** Python 3.12+, SQLite, REST APIs, cron, Linux (Debian), Docker, Proxmox, Git/GitHub, Whisper, Claude API, Ollama

---

## Projects

### Week 1 — Stock Quote Reporter
**`week1-ticker-report/`**

Python script that pulls live stock quotes from Alpha Vantage, formats the output, and saves a timestamped CSV report. Foundation project covering Python scripting fundamentals.

- Reads watchlist and API key from `.env` (python-dotenv)
- Loops through tickers, calls REST API, parses JSON
- Defensive error handling — rate limits, timeouts, malformed responses
- Writes formatted CSV with `csv.DictWriter`
- 12-second delays to stay under Alpha Vantage free-tier rate limits (25 req/day, 5/min)

**Stack:** Python, requests, python-dotenv, csv

---

### Week 2 — LEAPS Options Screener
**`week2-stock-scraper/`**

Stock screener that ingests a watchlist, calculates technical and fundamental signals, and automatically pulls LEAPS option chains for tickers that pass screening criteria.

- Pulls historical price data via yfinance
- Computes 50-day and 200-day moving averages, volume trends
- Screens against multiple criteria: trend (above 50/200 MA), beta < 2.0, earnings growth > 10%
- For passing tickers, automatically fetches LEAPS expiration chains (365+ days out)
- Calculates intrinsic vs time value breakdown for near-the-money calls
- Filters ETFs from fundamental analysis (different metrics apply)

**Stack:** Python, yfinance, pandas, python-dotenv

---

### Week 3 — YouTube Video Analyzer
**`week3-youtube-analyzer/`**

End-to-end pipeline that downloads YouTube videos, transcribes the audio using OpenAI Whisper with GPU acceleration, and generates structured analysis via the Anthropic Claude API. Built to extract investment insights from long-form financial content.

- Downloads audio with yt-dlp + ffmpeg
- Transcribes with Whisper large-v3 on local GPU (CUDA)
- Hybrid local/cloud architecture — free local transcription + low-cost cloud analysis (~$0.07/video)
- Initial implementation used local Ollama (Qwen3 14B/32B) with chunked analysis; pivoted to Claude API after benchmarking quality
- Single-command pipeline: one URL produces full transcript + structured analysis
- Handles 40-minute videos in under 10 minutes

**Problems solved:** PyTorch CUDA incompatibility with NVIDIA Blackwell (sm_120) — sourced nightly builds with correct compute capability. Python 3.14 / PyTorch compatibility gap — downgraded venv. Ollama streaming JSON response format requiring line-by-line parsing.

**Stack:** Python, OpenAI Whisper, yt-dlp, ffmpeg, PyTorch + CUDA, Ollama, Anthropic Claude API, requests, python-dotenv

---

### Week 4 — Reddit Comment Aggregator
**`week4-reddit-aggregator/`**

Tool for collecting and analyzing Reddit comments from multiple subreddits responding to the same question. Generates ranked markdown reports and LLM-synthesized analyses.

- Scrapes comments from multiple threads using Reddit's public JSON endpoints (no API key, no OAuth)
- Recursive comment extraction including all reply depths
- Filters deleted/removed comments before analysis
- Generates ranked markdown report (sorted by score, subreddits sorted by engagement)
- Sends aggregated comments to local Ollama LLM (Qwen3) for analysis — consensus, top recommendations, contrarian insights, action items
- Randomized request delays to avoid rate limiting

**Stack:** Python, requests, Ollama (Qwen3 14B), JSON parsing, markdown generation

---

### Week 5 — Stock Float Tracker (Production ETL Pipeline)
**`week5-float-tracker/`**

Automated daily stock float tracker deployed on a self-hosted Debian VM. Ingests data from SEC EDGAR (~10,341 US-listed tickers) and Financial Modeling Prep API, stores snapshots in SQLite, runs unattended via cron.

- Two-source ETL: SEC EDGAR for master ticker list, FMP for per-symbol float data
- Designed a 42-day cycle to scan the full universe within FMP's 250 calls/day free-tier limit
- Status-flagged schema (`scan_status` column) to skip permanently empty tickers (foreign ADRs, delisted, ETFs) and preserve daily API quota
- Transaction-safe commits inside the loop so partial progress survives crashes
- Defensive error handling for HTTP errors, empty responses, network failures
- Deployed via cron on Debian VM (VM-100) on Proxmox

**Database schema:**
- `symbols` — master list with ticker, title, CIK, retrieval timestamp, scan status
- `float_snapshots` — symbol, float shares, free float %, outstanding shares, source, date

**Deployment problems solved:** SSH config hostname collision between Gitea and VM caused SCP to authenticate against wrong service. GitHub PAT authentication for first-time push from VM. SQLite transaction durability during long-running ingestion.

**Stack:** Python, SQLite, requests, python-dotenv, cron, Debian, Proxmox, SSH/SCP

---

### Week 6 — Voice Notes to Tasks
**`week6-voice-notes-to-tasks/`**

Pipeline that transcribes voice notes with Whisper and converts spoken thoughts into structured task lists.

- Local Whisper transcription with GPU acceleration
- Extracts action items from unstructured speech
- (See folder for current implementation details)

**Stack:** Python, OpenAI Whisper, PyTorch + CUDA

---

### Week 7 — Reddit Research Dashboard
**`week7-research-dashboard/`**

Web dashboard built on top of the Reddit aggregator (Week 4) for organizing and reviewing research threads.

- Streamlit-based UI
- Reads aggregated comment data and LLM analyses
- (See folder for current implementation details)

**Stack:** Python, Streamlit, pandas, SQLite

---

### Week 8 — Transcript Screener
**`week8-transcript-screener/`**

Tool for screening transcripts (likely earnings calls or YouTube transcripts) for specific signals.

- (See folder for current implementation details)

**Stack:** Python, LLM integration

---

## Skills Demonstrated

**Languages & Core Tools**
Python 3.12+, SQL (SQLite), Bash, Git

**Data Engineering**
ETL pipeline design, schema design with status flags, idempotent ingestion, rate-limit-aware batching, transaction-safe commits, multi-source data integration

**APIs & Integration**
REST API integration (Alpha Vantage, FMP, SEC EDGAR, Reddit, Anthropic Claude), JSON parsing, error handling, authentication, rate limiting, pagination strategy

**LLMs & AI**
Local LLM serving (Ollama with Qwen3 14B/32B), cloud LLM APIs (Anthropic Claude), prompt engineering for structured extraction, chunked text processing, hybrid local/cloud architecture, OpenAI Whisper with GPU acceleration

**Linux & Deployment**
Debian admin, cron scheduling, SSH/SCP, venv management, Proxmox virtualization, deployment from local to remote VM

**Defensive Coding**
try/except patterns, transaction durability, retry logic, response validation, graceful degradation under API failures

**Development Workflow**
Git/GitHub, Personal Access Tokens, SSH key authentication, `.env` secrets management, `requirements.txt`, README documentation

---

## Stack Summary

| Category       | Tools                                                                |
| -------------- | -------------------------------------------------------------------- |
| Language       | Python 3.12+                                                         |
| Data Storage   | SQLite                                                               |
| APIs           | Alpha Vantage, FMP, SEC EDGAR, Reddit, Anthropic Claude              |
| Libraries      | requests, yfinance, pandas, python-dotenv, beautifulsoup4, Streamlit |
| LLMs           | Ollama (Qwen3 14B/32B), Anthropic Claude Sonnet                      |
| Audio/Video    | OpenAI Whisper (large-v3), yt-dlp, ffmpeg, PyTorch + CUDA            |
| Infrastructure | Linux (Debian), Proxmox VM, cron, Docker                             |
| Dev Tools      | Git, GitHub, SSH/SCP, VS Code                                        |

---

## Repository Structure

```
automation-projects/
├── week1-ticker-report/         # Alpha Vantage stock quote reporter
├── week2-stock-scraper/         # LEAPS options screener
├── week3-youtube-analyzer/      # YouTube → Whisper → Claude analysis pipeline
├── week4-reddit-aggregator/     # Multi-subreddit comment aggregator + LLM analysis
├── week5-float-tracker/         # Production ETL pipeline (deployed to Debian VM)
├── week6-voice-notes-to-tasks/  # Voice transcription + task extraction
├── week7-research-dashboard/    # Streamlit dashboard for Reddit research
├── week8-transcript-screener/   # Transcript screening tool
├── .gitignore
├── requirements.txt
└── README.md
```

Each project folder contains its own README, source code, and (where applicable) sample output.

---

## Contact

GitHub: [@eryklabs](https://github.com/eryklabs)
