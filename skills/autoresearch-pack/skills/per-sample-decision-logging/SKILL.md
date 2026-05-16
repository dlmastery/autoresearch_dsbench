---
name: per-sample-decision-logging
description: Per-sample (trade-level) decision logging — one row per test-day with prediction, direction, return, confidence, aleatoric/epistemic, correct, pnl_bps + per-fold summary stats. Triggers on "trade logs", "per-sample logging", "exp<N>_trades.csv", "trade summary", "win/loss spreadsheet", "confidence-stratified".
metadata:
  category: verification
  source: autoresearch
  related: [traditional-ml-metrics, heteroscedastic-loss, explainability-audit-14-section]
---

# Per-Sample (Trade-Level) Decision Logging

## When to use

- Every experiment — produce the per-sample CSV alongside aggregate metrics.
- Diagnosing which dates/regimes the model fails on.
- Calibrating confidence thresholds for deployment.

## The rule

> ### Trade-Level Win/Loss Logging (MANDATORY for every experiment)
> For EVERY experiment, produce a per-trade win/loss spreadsheet on test data. This is critical for understanding WHERE the model makes and loses money — not just aggregate metrics.
>
> **Output file:** `autoresearch_results/trade_logs/exp<N>_trades.csv`
>
> **Columns (one row per trade/day in test data):**
> | Column | Description |
> |--------|-------------|
> | date | Trade date |
> | fold | Which test fold window (1-7) |
> | regime | Regime label (e.g., "Post-crash recovery") |
> | prediction | Raw model prediction (mean) |
> | pred_direction | +1 (long) or -1 (short) |
> | actual_return | Actual daily return |
> | actual_direction | +1 (up) or -1 (down) |
> | strategy_return | sign(pred) * actual_return |
> | cumulative_return | Running cumulative return within fold |
> | confidence | Model confidence (1 - epistemic) |
> | aleatoric | Aleatoric uncertainty |
> | epistemic | Epistemic uncertainty |
> | correct | 1 if pred_direction == actual_direction, else 0 |
> | pnl_bps | P&L in basis points |
>
> **Per-fold summary at bottom of CSV (or separate `exp<N>_trade_summary.json`):**
> - Total trades, wins, losses per fold
> - Average win size (bps), average loss size (bps)
> - Largest single win, largest single loss
> - Win/loss ratio (avg_win / abs(avg_loss))
> - Streak analysis: max consecutive wins, max consecutive losses
> - Confidence-stratified accuracy: accuracy when confidence > 0.9 vs < 0.9
>
> **This data enables:**
> - Identifying specific dates/regimes where the model fails
> - Confidence calibration analysis (does high confidence = high accuracy?)
> - Position sizing research (Kelly criterion, volatility scaling)
> - Filtering rules (skip trades below confidence threshold)

### Generalisation for non-trading tasks

For generic DSBench / classification tasks, the same idea applies:

- One row per test sample with `sample_id`, `fold`, `prediction`, `predicted_class`, `true_class`, `correct`, `confidence`, `softmax_entropy` (proxy for aleatoric), `mc_dropout_var` (proxy for epistemic), `loss`.
- Per-fold summary: counts, top-k accuracy, calibration, confidence-stratified accuracy.

## Anti-patterns

- **Only aggregate metrics, no per-sample.** Aggregate hides regime-specific failure and confidence miscalibration.
- **Per-sample CSV without confidence/uncertainty columns.** Loses the most valuable filtering signal.
- **Streak analysis missing.** Max-consecutive-losses informs drawdown risk and kill-switch design.
- **Confidence-stratified accuracy lumped into one bucket.** Bucket by decile (or at least high/low).
- **No `regime` label.** Without it, you can't tell which regime is killing the model.

## Implementation checklist

1. Runner emits `exp<N>_trades.csv` + `exp<N>_trade_summary.json` for every run.
2. CSV columns match the table above (or the generalised classification variant).
3. `correct` and `pnl_bps` computed in the runner — don't make the dashboard recompute.
4. Per-fold summary section includes streak + confidence-stratified accuracy.
5. Dashboard links each experiment row to its trade-log CSV/JSON.

## References

- Source: `autoresearch/CLAUDE.md` section "Trade-Level Win/Loss Logging (MANDATORY for every experiment)"
- López de Prado (2018) "Advances in Financial Machine Learning" Chapter 14 on backtest analysis.
- Related: `traditional-ml-metrics`, `heteroscedastic-loss`, `explainability-audit-14-section` Section 9 (trade attribution).
