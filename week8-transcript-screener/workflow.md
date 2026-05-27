# Workflow: Running a Screen on One Ticker

> **Purpose**: this is the literal step-by-step. Read this first when you come back to the project. Should be runnable as a checklist with no prior context.
>
> **Time budget**: ~15–20 minutes per ticker once you've done it 3–4 times. First run is slower (~45 min).

---

## Prerequisites (one-time setup)

- [ ] Repo cloned locally
- [ ] All three prompts present in `prompts/`
- [ ] Access to Claude (web, desktop, or mobile chat — API not required for manual MVP)
- [ ] Source for transcripts: Motley Fool Transcripts (free), Seeking Alpha (paywall), AlphaStreet (free), or company IR page

---

## Step 0 — Pick a ticker

A ticker is worth screening if **all three** are true:

1. The company just reported quarterly earnings (within the last 2 weeks ideally; up to 6 weeks is OK).
2. You have a reason to look at it — appeared on an IBD scan, a watchlist, a peer ran well, sector heat, etc. Don't randomly pick from the universe; the prompts work on candidates, not on the entire market.
3. You don't already have a strong opinion. The point is to screen with a framework, not to confirm a bias. If you're already convinced you want to buy it, the screen is wasted; you'd rationalize through it.

**For your first 3–5 runs**: don't screen new ideas. Run the prompts on tickers you already know well (current portfolio, names you passed on previously) so you have an independent prior to sanity-check the output against. This is the **calibration phase**, not the screening phase.

---

## Step 1 — Pull transcripts (5 min)

Goal: get the last 4 quarterly earnings call transcripts.

1. Go to https://www.fool.com/earnings-call-transcripts/ (or alternative source)
2. Search ticker → find the 4 most recent quarterly calls
3. For each transcript:
   - Copy the full text (prepared remarks + Q&A — don't truncate)
   - Save raw to `transcripts/_raw/[TICKER]/[FYxxQy]_[YYYY-MM-DD].txt`

**Skip if:**
- Fewer than 2 quarters of transcripts available (recent IPO, recently public after spin) — you can't run trend analysis without history. Mark `INSUFFICIENT_HISTORY` and move on.
- The transcript is paywalled and you don't have access — try Motley Fool or AlphaStreet as fallback.
- The call is a "preliminary" or "special" call rather than a regular quarterly — these have different structure; be cautious.

---

## Step 2 — Concatenate transcripts (3 min)

Goal: produce a single text file with all 4 quarters in chronological order, ready to paste into Claude.

1. Create `transcripts/_processed/[TICKER]/4Q_concatenated_[YYYY-MM-DD].txt`
2. Order quarters **oldest first**, **newest last**
3. Between each transcript, insert a delimiter line:
   ```
   ===== QUARTER: TICKER FYxxQy YYYY-MM-DD =====
   ```
   Example for NVDA:
   ```
   ===== QUARTER: NVDA FY24Q1 2023-05-24 =====
   [transcript text]
   
   ===== QUARTER: NVDA FY24Q2 2023-08-23 =====
   [transcript text]
   
   ... etc
   ```

**Optional preprocessing** (skip for first runs, do later if signal is noisy):
- Strip "Operator" boilerplate at the start ("Good morning, ladies and gentlemen, and welcome to...")
- Strip safe-harbor / forward-looking-statement legal paragraph
- Add `[PREPARED REMARKS]` and `[Q&A]` section tags if not already present
- Tag each speaker turn (`[EXEC: Jensen Huang, CEO]`, `[ANALYST: Vivek Arya, BofA]`)

If your transcript source is messy (lots of stage directions, ads, formatting noise), spend the 5 minutes cleaning it up. Garbage in = garbage out.

---

## Step 3 — Run Stage 1: extraction (5 min)

Goal: produce a structured factual extraction with verbatim quotes.

1. Open Claude. **New chat.**
2. Open `prompts/stage1_extraction_v2.md` and copy the entire prompt block.
3. Paste the prompt into Claude.
4. Below the prompt, paste the concatenated transcript file from Step 2.
5. Send.
6. Wait for full output.
7. Copy the entire response.
8. Save to `outputs/[TICKER]/[YYYY-MM-DD]/stage1_extraction.md`.

**Important:** use a fresh chat for Stage 1. Don't share context with prior runs — context bleed is a real problem.

---

## Step 4 — VALIDATE Stage 1 output (3 min) ← non-negotiable

Goal: confirm Stage 1 didn't hallucinate or get numbers wrong.

This step is the single most important quality control in the whole workflow. Skip it and Stages 2A/2B are garbage.

1. Open the company's most recent quarterly earnings press release (their IR page, or via SEC EDGAR).
2. From Stage 1's H2 (quantitative scorecard), pick **5 random numbers** for the most recent quarter:
   - Revenue
   - GAAP EPS (diluted)
   - Operating margin %
   - At least one segment-level number
   - At least one guidance number
3. Verify each against the press release. Numbers should match exactly.
4. From Stage 1's H4 (guidance), pick the verbatim guidance quote and verify it word-for-word against the press release or the IR investor deck.

**If anything is wrong:**
- Single discrepancy on a small number → flag it, rerun Stage 1, re-validate. The prompt may have miscaptured one detail.
- Multiple discrepancies, or a major-number error (revenue, EPS) → STOP. Do not proceed to Stage 2. Likely root causes:
  - Transcript was truncated or corrupted. Re-pull from a different source.
  - Speaker tagging is wrong; numbers were attributed to the wrong quarter.
  - The prompt's verbatim-quote rule didn't hold. May indicate model drift; try a different model.
- Ongoing pattern of errors across multiple tickers → the prompt has a real problem. Update `prompts/CHANGELOG.md` and fix.

**If everything is correct**, proceed to Stage 5.

---

## Step 5 — Run Stage 2A: CAN SLIM analysis (3 min)

1. Open Claude. **New chat.** (Fresh context — do not reuse the Stage 1 chat.)
2. Open `prompts/stage2a_canslim_v1.md` and copy the prompt block.
3. Paste the prompt into Claude.
4. Below the prompt, paste your validated Stage 1 output from Step 4.
5. Send.
6. Save the response to `outputs/[TICKER]/[YYYY-MM-DD]/stage2a_canslim.md`.

---

## Step 6 — Run Stage 2B: Superstocks analysis (3 min)

1. Open Claude. **New chat.** (Fresh context — do not reuse Stage 1 or Stage 2A chats.)
2. Open `prompts/stage2b_superstocks_v3.md` and copy the prompt block.
3. Paste the prompt into Claude.
4. Below the prompt, paste your validated Stage 1 output from Step 4.
5. Send.
6. Save the response to `outputs/[TICKER]/[YYYY-MM-DD]/stage2b_superstocks.md`.

---

## Step 7 — Read both Stage 2 outputs (5 min)

For each output, read **only the TL;DR scorecard at the top first.** Form an initial reaction in 30 seconds.

Look at:
- **Verdict**: BUY CANDIDATE / WATCH / PASS
- **Top 3 bullish signals** with quotes
- **Top 3 risks** with quotes
- **Confidence score** (0–10)

Then compare the two lenses:

| Pattern | Interpretation |
|---|---|
| Both lenses BUY CANDIDATE | High-conviction signal — proceed to external follow-up |
| CAN SLIM BUY, Superstocks PASS | Likely a large-cap leader; chart-driven CAN SLIM trade if technicals confirm |
| CAN SLIM PASS, Superstocks BUY CANDIDATE | Likely a stealth-phase microcap; verify float, insider buying, theme |
| Both WATCH | Not actionable now; revisit next quarter |
| Both PASS | Drop the ticker |
| Stage 2B "DIVERGING" behavioral verdict | Numbers say buy but behavior says caution — downgrade to WATCH |

Write your own one-paragraph verdict in `outputs/[TICKER]/[YYYY-MM-DD]/notes.md`. Include:
- Your independent read (do you agree or disagree with the prompts?)
- What the calibration outcome is for tickers you already had a prior on (the prompts agreed / disagreed with you)
- One specific external follow-up question this ticker raises

---

## Step 8 — External follow-up (only if BUY CANDIDATE on either lens)

The prompts cannot assess these. You must verify before any action.

**Chart (essential):**
- [ ] Pull weekly chart from Stockcharts / TradingView
- [ ] Check 30-week moving average position
- [ ] Identify base structure: how long, how tight?
- [ ] RS rating (IBD) ≥ 80?
- [ ] Distance from 52-week high
- [ ] Volume on most recent breakout

**Microstructure:**
- [ ] Float (target <10M for Stine; <25M for O'Neil)
- [ ] Market cap
- [ ] Average daily volume
- [ ] Listed options yes/no (Stine prefers no)
- [ ] Short interest % of OS

**Insider activity:**
- [ ] SEC EDGAR Form 4 filings, last 90 days
- [ ] Open-market purchases only (filing code "P")
- [ ] Multiple distinct insiders?
- [ ] Dollar size relative to executive salary

**Discovery state:**
- [ ] Number of sell-side analysts (fewer is better per Stine)
- [ ] IBD 100 / IBD industry rank
- [ ] Recent press coverage (CNBC / WSJ / Bloomberg)
- [ ] Days since IPO (avoid <12 months per Stine)

**Capital structure:**
- [ ] Recent secondary offering, ATM, convertible? (Stine: wait 6 months)
- [ ] Strategic-alternatives announcement? (Stine: hard sell signal)
- [ ] Long-term debt level

**Market direction (CAN SLIM "M"):**
- [ ] S&P 500 / NASDAQ trend (uptrend confirmed?)
- [ ] Distribution-day count (recent)
- [ ] Follow-through-day status

A BUY CANDIDATE verdict that fails any of the chart criteria is not a buy — it's a watch. Stine ch. 6 is unambiguous: **chart pattern is checked first, fundamentals second.**

---

## Step 9 — Update tracking

After every screen, regardless of verdict:

1. Add a line to `outputs/[TICKER]/[YYYY-MM-DD]/notes.md` with:
   - Final verdict (your verdict, not just the prompts')
   - Action taken (added to watchlist, opened position, dropped, etc.)
   - Date stamp
2. If you took action: add the entry date and verdict to a portfolio log so you can track forward returns later. Six months from now, you want to be able to ask "of the names I screened as BUY CANDIDATE, how many actually outperformed?"

---

## Common failure modes

**Stage 1 invents a number not in the transcript.** Most common cause: transcript got truncated mid-paragraph and the model filled in. Fix: re-pull transcript, verify completeness, rerun.

**Stage 2 verdict feels obviously wrong.** Most common cause: Stage 1 missed important context (e.g., a key Q&A exchange) or got a number wrong that propagated. Re-validate Stage 1 H2 numbers and H9 Q&A summary.

**Both stages run fine but verdict doesn't match your independent read on a calibration ticker.** This is the calibration phase doing its job. Two possibilities: (a) the prompts have a real flaw — log it in `decisions_log.md` and consider tightening the prompts; (b) your independent read was actually wrong and the prompts caught something — also valuable.

**Outputs are inconsistent run-to-run on the same input.** Set Claude temperature lower if running via API. In the chat interface, simply rerun and use the more conservative verdict.

**The screen takes too long and you start cutting corners.** Don't screen 50 tickers in one sitting. The discipline that catches errors decays with fatigue. Cap at 5–8 tickers per session.

---

## Calibration milestone (gate to live screening)

**Do not start live-screening new ideas until:**

1. You've run the prompts on at least 5 tickers you have strong priors on (current holdings, recent passes), and the prompts agree with your read on ≥4 of them.
2. You've run the prompts on the backtest set (5 winners + 3 failures, see `backtest/`) and verdicts match expected outcomes on ≥6 of 8.
3. Stage 1 number accuracy is ≥99% on a 25-sample audit across multiple tickers.

If you can't hit those gates, the prompts need iteration. The fastest path to better prompts is more calibration runs, not more research.

---

## When to upgrade the workflow

The manual workflow above is appropriate for ~50 tickers per quarter. If you're consistently exceeding that, OR if you find the manual repetition error-prone, upgrade in this order:

1. **Python preprocessor** (P1 + P2 from the migration spec): cleans transcripts, computes deterministic counts. Saves ~3 min per ticker, eliminates LLM count hallucination.
2. **Anthropic API + scripted pipeline**: removes the copy-paste step. Saves ~5 min per ticker, enables batch processing.
3. **Storage in a database** instead of flat files: only when the file system is unmanageable (>200 outputs).
4. **Web UI / dashboard**: only if other people will use this. Otherwise YAGNI.

Don't upgrade until the manual flow is working reliably. Engineering cost > screening cost until ~50 tickers per quarter.
