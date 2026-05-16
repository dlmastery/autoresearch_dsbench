---
name: sub-period-robustness-audit
description: Sub-period robustness audit — evaluate a champion across rolling sub-periods (e.g. 2008-2012, 2013-2017, 2018-2025) to detect regime-dependence. Flag champions whose performance is concentrated. Triggers on "sub-period robustness", "rolling-window evaluation", "regime dependence", "crisis-trade specialist", "robustness_audit.txt".
metadata:
  category: verification
  source: autoresearchindexspy
  related: [regime-gate, forensic-audit-pipeline, explainability-audit-14-section]
---

# Sub-Period Robustness Audit

## When to use

- After a new global champion is found.
- Before deploying a model with a long evaluation history (>5 years).
- When suspicious "single-period luck" might be present.

## The rule

> **Critical caveat from SPY**: model is a CRISIS-TRADE SPECIALIST. Sub-period sharpe 2008-2012 = +1.10, 2021-2025 = -0.67. Regime gate prevents trading in low-vol bull regimes (only ~30% of days in 2024-2025) but doesn't generate alpha there. See `autoresearchspy/autoresearch_results/champion_verification/robustness_audit.txt`.

### Audit construction

1. **Define non-overlapping sub-periods** spanning the test horizon. Typical splits:
   - **By calendar:** 5-year blocks (2008-2012, 2013-2017, 2018-2022, 2023-2025).
   - **By regime:** crisis / recovery / expansion / late-cycle.
   - **By volatility:** rvol60d quartiles.
2. **Per-sub-period metrics.** For each sub-period compute composite, Sharpe, MCC, win-rate, max drawdown.
3. **Report the spread.** The headline is `min_subperiod_sharpe / max_subperiod_sharpe`. Ratios near 1 mean robustness; ratios near 0 (or negative) mean regime-dependence.
4. **Flag concentration.** If >50% of test composite comes from <30% of test days, the model is concentrated and likely has a "deployment ramp" risk.
5. **Document caveats.** Write findings verbatim to `champion_verification/robustness_audit.txt` (or equivalent). Link from the winner README.

### When to act on findings

- **Concentrated edge:** install a `regime-gate` to confine trading to the edge regime.
- **Regime-flip:** if the latest sub-period reverses sign, the model's mechanism may have broken — retrain or retire.
- **Stable edge:** deploy with standard monitoring.

## Anti-patterns

- **Single aggregate Sharpe published, no sub-period table.** Hides the +1.10 / -0.67 split that disqualifies deployment.
- **Sub-periods chosen to make the model look good.** Use pre-registered splits (calendar blocks or volatility quartiles), not custom-fit cuts.
- **Reporting only the "good" sub-period** in the README — full table or it's a sales pitch, not an audit.
- **Skipping the audit because "the model has 7-fold breakdown"** — the 7 folds may all fall in one regime era.
- **No actionable recommendation** (gate, retrain, retire) attached to the audit findings.

## Implementation checklist

1. `_ensemble_robustness.py` (or equivalent) computes per-sub-period metrics on the champion's test predictions.
2. Output: a table in `robustness_audit.txt` with columns `sub_period | days | composite | sharpe | mcc | win_rate | max_dd`.
3. Headline line: `min_sub_sharpe = X, max_sub_sharpe = Y, ratio = Z`.
4. Concentration metric: `pct_composite_from_top_30pct_days`.
5. Recommendation block: `Action: [deploy | gate | retrain | retire]` with rationale.
6. Linked from the winner README and the dashboard's audit panel.

## References

- Source: `autoresearchindexspy/autoresearchspy/CLAUDE.md` top-of-file critical-caveat block; `_ensemble_robustness.py` reference; `robustness_audit.txt` reference.
- Bailey & López de Prado (2014) 'The Deflated Sharpe Ratio' — multi-trial significance, complementary to sub-period audit.
- Related: `regime-gate`, `forensic-audit-pipeline`, `explainability-audit-14-section`.
