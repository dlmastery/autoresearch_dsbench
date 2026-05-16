---
name: three-stream-feature-engineering
description: Three-stream feature engineering — combine daily, pre-market (causal-anchor), and high-frequency hourly streams with a strict-causal anchor cutoff. SPY example uses daily yfinance + Asian/EU pre-market + Barchart hourly streams anchored at us_open (09:30 ET). Triggers on "three-stream", "Asian pre-market", "Barchart hourly", "causal anchor", "asia_close", "us_open", "us_close", "anchor cutoff".
metadata:
  category: engineering
  source: autoresearchindexspy
  related: [data-integrity-rules, train-val-test-invariants, stacked-ensemble-design]
---

# Three-Stream Feature Engineering (causal-anchor multi-source)

## When to use

- The single-stream model has plateaued.
- The asset has natural multi-region or multi-frequency observations available before the prediction anchor.
- You want to encode genuinely causal information that the market hasn't fully priced in yet.

## The rule

> ### Three-stream feature engineering (MANDATORY pre-flight discipline)
> Every SPY training run combines these three causally-anchored streams. See `autoresearchspy/FEATURES_AND_DATA.md` §10–11 for the full spec.
>
> 1. **Daily yfinance stream** — `data/download.py` + `data/features.py`. ~205 columns: SPY OHLCV technicals, sector ETFs, vol regime (VIX/VXN/MOVE), yields/credit, macro/FX, panel-learning targets.
> 2. **Asian + European pre-market stream** — `data/asian_premarket.py`. ~70 columns: N225, HSI, KS11, TWII, STI, AXJO, 000001.SS, BSESN (close before 09:30 ET, fully causal) + FTSE/DAX/CAC/STOXX50E/IBEX/SSMI lagged 1d. Includes blended `asian_sentiment_score` and `asian_divergence`.
> 3. **Barchart hourly stream** — `data/barchart_hourly.py`. ~400 columns: 34 tickers (SPY, breadth ETFs, Asia/Europe ETF surrogates, megacap ADRs, US megacaps, vol/yields/macro, ES/NQ/YM/RTY futures) × 12 hourly features (RSI/MACD/RV/Amihud/first-hour/last-hour/overnight-gap). Aligned to daily index via causal anchor (`asia_close` | `us_open` | `us_close`).
>
> **Anchor contract:** the chosen anchor (default `us_open` = 09:30 ET) sets the strict-causal cutoff. Every feature in row[T] must be observable at or before the anchor on date T. Train at `us_open`; ablate at `asia_close` for maximum lead; `us_close` is explanatory-only and forbidden for forward-prediction training. **Barchart credentials:** `.env` file (gitignored) — copy `.env.example` and fill in `BARCHART_USERNAME` / `BARCHART_PASSWORD`.

### Why this pattern matters

> **Asian close is the SPY edge.** N225/HSI/KS11/AXJO close 5–9h before NYSE 09:30; their close-to-close moves carry causal information for SPY day-T direction (Hamao-Masulis-Ng 1990, Lin-Engle-Ito 1994, Lou-Polk-Skouras 2019). Blended `asian_sentiment_score` aggregates them.

The SPY project demonstrated **+0.330 composite** gain from adding the Asian/EU pre-market block alone — the single largest gain in the project arc.

### Generalisation pattern

Any prediction task with a clear time-anchor and multi-source causal data can adopt this pattern:

1. **Pick the anchor.** What's the latest moment before the prediction at which features can be observed?
2. **Enumerate streams.** What data sources are observable strictly before the anchor? List them with their native frequency.
3. **Align to the prediction index.** Resample / forward-fill each stream up to the anchor; never let a row see data observed AFTER its anchor.
4. **Wire causality guards.** Every feature column has a `_anchor_cutoff_validated: true` flag verified by a unit test that walks the pipeline timestamps.
5. **Anchor ablation.** Train at the latest causal anchor (e.g. `us_open`), ablate at an earlier anchor (`asia_close`) to measure how much edge you give up; never train at a post-prediction anchor (`us_close` for next-day prediction).

## Anti-patterns

- **Mixing anchors in a single row.** Some columns at `us_open` and others at `us_close` — guaranteed leakage.
- **Forward-fill that crosses anchor boundaries.** A pre-market column forward-filled from the previous prediction day into today's anchor includes data observed within the gap.
- **Training at `us_close` for next-day prediction.** The close is observable AFTER the prediction window — pure leakage masquerading as edge.
- **No anchor-validation unit test.** Without it, future feature additions silently violate causality.
- **Skipping the credentials gitignore.** Barchart credentials leaked to public repo = account suspended + security incident.

## Implementation checklist

1. `data/<daily_source>.py`, `data/<premarket_source>.py`, `data/<hourly_source>.py` each cache to their own dir (`.data_cache/`, `.data_cache_premarket/`, `.data_cache_hourly/`).
2. Each module exposes `align_to_index(target_index, anchor) -> DataFrame` that rejects post-anchor observations.
3. Top-level `features.py` calls each module, concatenates the columns, validates the `_anchor_cutoff_validated` flag.
4. Credentials in `.env`; `.env.example` is the template; `.env` is gitignored.
5. Unit test: walk every column's timestamps vs the row's anchor; abort the build if any violation.

## References

- Source: `autoresearchindexspy/autoresearchspy/CLAUDE.md` section "Three-stream feature engineering (MANDATORY pre-flight discipline)"
- Hamao, Masulis, Ng 1990 'Correlations in Price Changes and Volatility across International Stock Markets' RFS.
- Lin, Engle, Ito 1994 'Do Bulls and Bears Move Across Borders? International Transmission of Stock Returns and Volatility' RFS.
- Lou, Polk, Skouras 2019 'A Tug of War: Overnight versus Intraday Expected Returns' JFE — overnight/intraday return decomposition.
- Related: `data-integrity-rules`, `train-val-test-invariants`, `stacked-ensemble-design`.
