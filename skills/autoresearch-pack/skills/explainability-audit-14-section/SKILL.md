---
name: explainability-audit-14-section
description: 14-section explainability and auditability report mandated for every new champion — executive summary, feature importance, SHAP-style local, feature drift, calibration, uncertainty sanity, regime distribution, trade attribution, risk audit, data-pipeline audit, model dump, limitations, deployment checklist. Triggers on "audit report", "explainability", "feature importance", "SHAP", "calibration", "audit_report.md".
metadata:
  category: verification
  source: autoresearch
  related: [winner-archive-protocol, forensic-audit-pipeline, traditional-ml-metrics]
---

# Explainability & Auditability Report (14 sections)

## When to use

- A new champion has been found (status=KEEP and composite > previous best).
- Preparing a model for deployment review.
- Auditing a suspiciously-good model — the audit will surface drift or calibration issues.

## The rule

> ### Explainability & Auditability Report (MANDATORY for every NEW BEST)
>
> When a new champion is found, produce a full data-scientist-grade audit to `autoresearch_results/winners/<exp_id>/audit_report.md`. This is not optional — a trading model without explainability is un-deployable.
>
> **Required sections (all of them):**
>
> 1. **Executive summary** — Champion test Sharpe, return, max drawdown, PSR, all 7 fold Sharpes. Regime-by-regime pass/fail.
>
> 2. **Feature importance (permutation method)** — For each of the 104 features, shuffle that column in the test set, re-evaluate, report the drop in test Sharpe. Rank features by importance. Cite: Breiman (2001) "Random Forests" section on variable importance. Save `feature_importance.csv` with columns `[feature_name, sharpe_drop, rank, domain_category]`.
>
> 3. **Top-N feature analysis** — For the top 10 most-impactful features, explain:
>    - What the feature measures (from features.py docs)
>    - Why it matters economically (e.g., "VIX = equity volatility, negatively correlated with USD risk appetite")
>    - Per-fold impact: is feature X strong in regime A but weak in regime B?
>
> 4. **SHAP-style local explanations** — For 10 random test-set predictions, compute per-feature contribution to the prediction. Use gradient * input as a cheap approximation. Save as `shap_local.csv`.
>
> 5. **Per-fold feature drift** — For each fold, compute mean/std of each feature vs the training set. Features with Z-score > 2 on a fold indicate distribution shift. Report top 5 drifted features per fold with explanation.
>
> 6. **Calibration analysis** — Plot predicted-return quantile vs realized-return mean. Ideal: monotonic. Report calibration error (mean absolute deviation from monotonic). Cite: Guo et al. (2017) "On Calibration of Modern Neural Networks."
>
> 7. **Uncertainty sanity** — Plot aleatoric vs prediction absolute error. Should be monotonic. Plot confidence vs hit-rate. Bucket predictions by confidence decile, report hit-rate per decile. Cite: Kendall & Gal (2017).
>
> 8. **Per-regime prediction distribution** — For each fold, plot histogram of predicted returns. Identify if the model is systematically biased (e.g., always predicting +0.01%) vs appropriately reactive.
>
> 9. **Trade attribution** — Decompose the cumulative return: for each test fold, report top-5 winning trades (date, pair, predicted, actual, P&L) and top-5 losers. Pattern analysis: are losses concentrated on specific dates/regimes?
>
> 10. **Risk audit** — Max drawdown period: which dates, what was the market doing, what features were the model reading. VaR-95, CVaR-95 per fold. Skewness, kurtosis of strategy returns.
>
> 11. **Data pipeline audit** — Reassert: zero train/val/test leakage, 90-day purge, 21-day embargo, 10-day label horizon buffer. Rerun `validate_purge_embargo()` and include the output verbatim. No assumptions — MEASURE.
>
> 12. **Model config complete dump** — Every hyperparameter + the Python version + torch version + numpy version + random seed. For true reproducibility.
>
> 13. **Known limitations & risks** — What regimes has this model NEVER been tested on? (e.g., hyperinflation, CB digital currencies, war shocks). Where will it most likely fail in live trading?
>
> 14. **Deployment checklist** — What monitoring is needed? What's the kill-switch criterion (max drawdown threshold, consecutive loss count)? What retraining cadence?
>
> **Implementation:** Add `run_audit_report.py` that takes a `best_model.pt` path and produces the full report. Run it automatically when `composite > prev_best` in the runner.

## Anti-patterns

- **Skipping sections that "don't apply"** — a classification task still needs a feature-importance, calibration, and risk-audit equivalent.
- **Free-text feature importance** ("VIX is important") instead of the permutation-method ranking with numeric Sharpe drop.
- **Calibration plotted without a numeric error** — report mean absolute deviation from monotonic.
- **Skipping section 11 (data-pipeline audit) because "we ran it earlier"** — rerun on the champion's exact split; capture verbatim output.
- **Deployment checklist that's aspirational** ("we should monitor X") — write the concrete monitoring rule and kill-switch threshold.

## Implementation checklist

1. `run_audit_report.py` accepts `--model best_model.pt --output winners/<id>/audit_report.md`.
2. Each of the 14 sections has a function; the script orchestrates them in order.
3. CSV side-outputs: `feature_importance.csv`, `shap_local.csv`, per-fold drift, per-fold calibration table.
4. The runner auto-invokes `run_audit_report.py` when `composite > prev_best`.
5. The winner README links to the audit report and summarises Section 13 (limitations) and Section 14 (deployment).

## References

- Source: `autoresearch/CLAUDE.md` section "Explainability & Auditability Report (MANDATORY for every NEW BEST)"
- Breiman (2001) "Random Forests" — permutation importance.
- Guo, Pleiss, Sun, Weinberger (2017) "On Calibration of Modern Neural Networks" — ICML.
- Kendall & Gal (2017) "What Uncertainties Do We Need in Bayesian Deep Learning for Computer Vision?" — NeurIPS.
- Related: `winner-archive-protocol`, `forensic-audit-pipeline`, `traditional-ml-metrics`.
