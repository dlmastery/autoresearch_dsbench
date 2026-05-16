---
name: regime-gate
description: Regime gate — a conditional rule that gates trading to specific regimes where the model has an edge. SPY example uses `rvol60d > 15%` to confine the ensemble to volatile regimes. Triggers on "regime gate", "conditional gate", "rvol60d", "regime filter", "trade-or-skip".
metadata:
  category: engineering
  source: autoresearchindexspy
  related: [stacked-ensemble-design, sub-period-robustness-audit, per-sample-decision-logging]
---

# Regime Gate (conditional trade-or-skip filter)

## When to use

- The robustness audit (see `sub-period-robustness-audit`) reveals a model is great in some regimes and break-even/negative in others.
- A model has an obvious "edge regime" (e.g. crisis-trade specialist) and a "no-edge regime".
- You want to deploy a model whose unconditional Sharpe is mediocre but whose conditional Sharpe is strong.

## The rule

> ### Regime gate `rvol60d > 15%` (+0.134 composite, from SPY session-complete state)
>
> **Critical caveat**: the SPY model is a CRISIS-TRADE SPECIALIST. Sub-period sharpe 2008-2012 = +1.10, 2021-2025 = -0.67. Regime gate prevents trading in low-vol bull regimes (only ~30% of days in 2024-2025) but doesn't generate alpha there. See `autoresearchspy/autoresearch_results/champion_verification/robustness_audit.txt`.

### Construction pattern

1. **Identify the edge regime.** Run the robustness audit. If the model's per-sub-period Sharpe is bimodal (+1.10 / -0.67) along an observable axis (realised vol, VIX level, term-structure slope), there's a candidate gate.
2. **Define the gate variable as strictly causal.** Must be observable at or before the prediction's anchor. For SPY, `rvol60d = rolling-60-day realised vol of SPY` is causal w.r.t. the next-day prediction.
3. **Choose the gate threshold.** Optimise the threshold on val ONLY — never test. Grid `{10%, 12%, 15%, 18%, 20%, 25%}` is a typical starting set.
4. **Two-mode strategy.** Above gate: trade per model. Below gate: skip (flat / 100% cash).
5. **Evaluate.** Composite on test under the gated strategy must beat the unconditional strategy on BOTH val and test (quality ratchet).
6. **Caveat in the deployment doc.** The gate is a CONDITIONAL — it doesn't generate alpha in the off-regime, just avoids losses. Communicate the trade frequency expected (e.g. SPY: ~30% of days in 2024-2025).

### Why the gate adds composite

- The unconditional Sharpe is dragged down by the off-regime period.
- Gating removes those low-edge days; the conditional Sharpe is what remains.
- The `n_negative_folds` term of the composite improves because gated folds with bad results now show ~0 (no trade) rather than negative.

## Anti-patterns

- **Threshold chosen on test data.** Direct overfitting. Use val only.
- **Non-causal gate variable** (e.g. realised vol over a window that includes the prediction day). Leakage.
- **Selling the gate as "alpha generator"** — it's a defensive filter, not a signal generator. Communicate clearly.
- **No off-regime fallback strategy** — what does the portfolio do on no-trade days? Document: cash, hedge, or alternative model.
- **Gate that's too aggressive** (trades only on extreme regimes that occur 5% of days). Trade frequency falls below deployable.

## Implementation checklist

1. Define `gate(x)` as a causal function of features available at the anchor.
2. Optimise threshold on val composite; freeze threshold before touching test.
3. Apply gate at inference: `if gate(x): pred = model(x) else: pred = 0` (skip).
4. Recompute per-fold Sharpe, MCC, win-rate under the gate; report alongside unconditional.
5. Deployment doc explicitly describes gate variable, threshold, trade frequency, off-regime fallback.

## References

- Source: `autoresearchindexspy/autoresearchspy/CLAUDE.md` top-of-file champion summary; `_ensemble_regime_gated.py` reference; `robustness_audit.txt`.
- Ang & Bekaert (2002) 'International Asset Allocation with Regime Shifts' RFS — regime-conditional strategy theory.
- Related: `stacked-ensemble-design`, `sub-period-robustness-audit`, `per-sample-decision-logging`.
