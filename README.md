# automation-projects

Personal automation learning repo — financial data, homelab tooling, and scripting practice.
Built through a 90-day roadmap toward automation engineering.

---

## Structure

```
automation-projects/
  week1-ticker-report/       # Python fundamentals — file I/O, loops, functions
  week2-stock-scraper/       # APIs, requests library, pulling real stock data
  week3-homelab-scripts/     # Bash + SSH automation for TrueNAS / Proxmox
  week4-git-structure/       # Git workflows, project structure, secrets handling
  ...
```

Each folder is a standalone mini-project with its own README explaining what it does and what I learned.

---

## Stack

- Python 3.12
- Libraries: requests, pandas, BeautifulSoup, python-dotenv (added as needed per week)
- Bash / shell scripting
- Runs on: Windows (dev), TrueNAS + Proxmox (homelab deployment)

---

## Security

All API keys and credentials are stored in `.env` files.
`.env` is in `.gitignore` — never committed.
Scripts use placeholder values in examples.

---

## Goals

- Build real tools for financial data analysis (LEAPS / stock screening)
- Automate homelab maintenance (TrueNAS, Proxmox)
- Develop a portfolio of working automation scripts

---

*Started March 2026*