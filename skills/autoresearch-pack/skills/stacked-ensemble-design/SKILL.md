---
name: stacked-ensemble-design
description: Stacked ensemble design — val-weighted N-component ensemble where each component is an independently-tuned champion, weights derived from per-component val-set composite. Includes the SPY 12-component +0.277 gain demonstration. Triggers on "stacked ensemble", "val-weighted ensemble", "ensemble weights", "12-component", "ensemble averaging", "model stacking".
metadata:
  category: engineering
  source: autoresearchindexspy
  related: [regime-gate, sub-period-robustness-audit, monotonic-quality-progression, winner-archive-protocol]
---

# Stacked Ensemble Design (val-weighted multi-component)

## When to use

- A single backbone's seed variance is large (autoresearch LSTM observed σ=0.96 composite).
- The 50-experiment mandate is complete and individual experiments plateau.
- Multiple independent champions exist across backbones/feature-streams — combine for variance reduction.

## The rule

> ### Three stacked validated KEEPs (from spy session-complete state)
>
> 1. Asian/EU pre-market block (+0.330 composite over daily-only) — `data/asian_premarket.py`
> 2. Val-weighted 12-component ensemble (+0.277) — `_ensemble_val_weighted.py`
> 3. Regime gate `rvol60d > 15%` (+0.134) — `_ensemble_regime_gated.py`
>
> **Cumulative gain**: -0.373 (daily-only) → **+0.368** (champion) = +0.741 stacked.

### Stacked-ensemble construction (val-weighted N-component)

1. **Component selection.** Choose N independently-tuned champions (or near-champions). Examples: distinct seeds of the same backbone; distinct backbones (LSTM + PatchTST + XGBoost); distinct feature streams (daily-only + with Asian pre-market). In the SPY project, N=12 was the sweet spot.
2. **Per-component val composite.** Evaluate each component on the union val set under the project's composite metric.
3. **Softmax weights.** `w_i = softmax(val_composite_i / T)` with T chosen so the top-3 components carry 60-80% of the mass; uniform-weight is a fallback if `T → ∞`.
4. **Test-time averaging.** `final_pred(x) = sum_i w_i * pred_i(x)`. For classification, average softmax-probs then argmax; for regression, average means and combine variances (Lakshminarayanan et al. 2017).
5. **Composite on union test.** Compare ensemble composite vs single-best-component composite under the project's keep/revert metric. If both val and test improve, the ensemble becomes the new champion.

### Implementation invariants

- Components must be INDEPENDENT in some axis (seed, architecture, feature stream). Identical-config rerun ensembles offer minimal gain.
- Weights derived from val ONLY — never test. Test is held out for the final composite measurement.
- Persist the component list + weights + per-component checkpoint hashes in `best_config.json`.
- Reproduction = re-running each component AND verifying the same weighted blend.

### Spy concrete example (12-component val-weighted)

The SPY champion `_ensemble_val_weighted.py` blends 12 components spanning multiple backbones (LSTM seeds, PatchTST configs, GBM variants) with weights driven by per-component val composite. The blend added **+0.277 composite** over the best single component (which was already a +0.330 gain over the daily-only baseline). The composition is reproduced by `python -m autoresearchspy._ensemble_val_weighted`.

## Anti-patterns

- **Equal-weight ensembles** without checking that all components are roughly equally good. A weak component drags the blend.
- **Weights computed on test** — direct overfitting to the holdout. Use val.
- **N too small (≤ 3)** — variance reduction is shallow; aim for N ≥ 6 distinct configs.
- **All components from the same backbone, same seed.** Variance reduction is near-zero — diversify.
- **Skipping the component-hash provenance.** Without it, you can't tell if a regression is from drift in a single component.

## Implementation checklist

1. `ensemble_spec.json` lists components by `{path, val_composite, weight, hash}`.
2. `_ensemble_val_weighted.py` reads the spec, loads each checkpoint, averages predictions.
3. Compute ensemble's val and test composite under the project metric.
4. Ensemble KEEP rule: val AND test composite must improve over the single best component.
5. Archive the ensemble as a winner (same `winner-archive-protocol`) including the component list.
6. Reproduction script runs each component then re-blends — verifies hash match.

## References

- Source: `autoresearchindexspy/autoresearchspy/CLAUDE.md` top-of-file "Three stacked validated KEEPs" block and `_ensemble_val_weighted.py` reference.
- Lakshminarayanan, Pritzel, Blundell 2017 NeurIPS 'Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles' (arXiv:1612.01474) — variance reduction theory.
- Wolpert 1992 'Stacked Generalization' — original stacking idea.
- Related: `regime-gate`, `sub-period-robustness-audit`, `monotonic-quality-progression`, `winner-archive-protocol`.
