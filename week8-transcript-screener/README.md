# transcript-screener

> A two-stage LLM prompt system for screening publicly traded stocks via earnings call transcripts, using William O'Neil's CAN SLIM and Jesse Stine's Superstocks methodologies.

**Last updated:** 2026-05-03  
**Status:** Manual-MVP phase. Prompts built. Backtest not yet run. No live screens yet.  
**Owner:** [you]

---

## What this is

A reusable prompt system that takes 3–5 quarters of an earnings call transcripts for a single publicly traded stock, runs them through Claude in two stages, and produces a structured screening verdict (BUY CANDIDATE / WATCH / PASS) through two independent methodological lenses.

The two lenses are run separately and intentionally:
- **Stage 2A — CAN SLIM** (William O'Neil, *How to Make Money in Stocks*, 4th ed., 2009): growth + leadership + breakout-from-base bias, large-cap-friendly.
- **Stage 2B — Superstocks** (Jesse Stine, *Insider Buy Superstocks*, 2013): contrarian, microcap-skewed, weekly-chart-driven, low-float, low-PE, theme-driven.

Where the two lenses agree → high-conviction signal. Where they disagree → informative edge case.

This is a **buy-screening** tool, not a sell-signal tool. Sell signals are a future project.

---

## What this is NOT

- Not a chart analyzer. Both methodologies require chart confirmation; this only handles the fundamental/transcript side.
- Not a portfolio-management system. No position sizing, no stops, no entry timing.
- Not a substitute for the external follow-up checklist (float, Form 4, RS rating, market direction). The prompts explicitly flag what must be verified outside the transcript.
- Not a buy recommendation engine. The output is a screening bucket, not a trade signal.

---

## Current state of the world

| Component | Status |
|---|---|
| Stage 1 extraction prompt (v2) | ✅ Written, not yet validated against backtest |
| Stage 2A CAN SLIM prompt (v1) | ✅ Written, not yet validated against backtest |
| Stage 2B Superstocks prompt (v3) | ✅ Written, primary-source-aligned, not yet validated |
| Methodology research | ✅ Complete (`docs/methodology_research.md`) |
| Stine book primary-source notes | ✅ Complete (`docs/stine_book_notes.md`) |
| Backtest set assembled | ❌ Not done |
| Backtest run on prompts | ❌ Not done |
| Live screening | ❌ Not started — gated on backtest |
| Python preprocessor | ❌ Not started — manual MVP first |
| API/scripted pipeline | ❌ Not started — gated on workflow validation |

---

## Quick start

To run a screen on one ticker, see `docs/workflow.md`. End-to-end takes ~15–20 minutes per ticker once you've done it 3–4 times.

Required inputs:
- Last 4 quarterly earnings call transcripts for the target ticker (Motley Fool, Seeking Alpha, or company IR site)
- Access to Claude (web/desktop chat is fine — API not required for manual MVP)
- The three prompts in `prompts/`

---

## Repo layout

```
transcript-screener/
├── README.md                          ← you are here
├── prompts/                           ← copy-paste prompts; the core IP
│   ├── stage1_extraction_v2.md
│   ├── stage2a_canslim_v1.md
│   ├── stage2b_superstocks_v3.md
│   └── CHANGELOG.md
├── docs/
│   ├── workflow.md                    ← step-by-step run procedure
│   ├── methodology_research.md        ← original deep-research artifact
│   ├── stine_book_notes.md            ← primary-source findings
│   ├── canslim_reference.md           ← O'Neil bars summarized
│   └── decisions_log.md               ← append-only log of design choices
├── transcripts/
│   ├── _raw/[TICKER]/                 ← unmodified pasted transcripts
│   └── _processed/[TICKER]/           ← concatenated, ready to feed Stage 1
├── outputs/
│   └── [TICKER]/[YYYY-MM-DD]/
│       ├── stage1_extraction.md
│       ├── stage2a_canslim.md
│       ├── stage2b_superstocks.md
│       └── notes.md                   ← your independent verdict
├── backtest/
│   ├── known_winners.md               ← target tickers + dates
│   ├── known_failures.md              ← target tickers + dates
│   └── results/                       ← stage outputs vs. expected verdicts
└── preprocessor/                      ← future Python work; empty for now
```

---

## What to do when you come back to this project after a break

1. Read this README's "Current state" table — what's done vs. not done?
2. Open `docs/decisions_log.md` — what was the most recent decision and why?
3. Open `docs/workflow.md` — re-orient on the run procedure.
4. Open `prompts/CHANGELOG.md` — has anything been updated since you last ran a screen?
5. Pick the smallest next action from the "Current state" table that isn't done. Do that.

If you can't get oriented in <10 minutes from these four files, the documentation has decayed — fix the docs before doing project work.

---

## Known limitations

Documented in full in `docs/methodology_research.md`. Short version:
- Both methodologies are growth/momentum frameworks tuned to past market regimes. Don't assume the bars (≥25% EPS, <10M float, ≤PE 10) are immutable.
- LLM number hallucination is the #1 risk. Stage 1's verbatim-quote requirement is the primary mitigation. Spot-check 3–5 numbers per run.
- LLM cross-quarter counts (hedging density, theme frequency, prepared-remarks length) are approximations, not measurements. Migrate to deterministic preprocessor when reliability matters.
- Stine's framework is microcap-skewed and biased toward concentration. The verdict is a screen, not a position-sizing recommendation.
- 60–70% of CAN SLIM signal and 50–60% of Superstocks signal is transcript-extractable. The rest (chart, MAs, RS, float, Form 4, market direction) must be verified externally.

---

## License / sharing

Private repo. The prompts reference but do not reproduce copyrighted Stine/O'Neil text. Do not push public until that's been reviewed.

---

## Contact / future-self note

If anything in here doesn't make sense to you when you come back: the most likely explanation is that you tweaked something and didn't update this file. Fix the README before fixing the code.
