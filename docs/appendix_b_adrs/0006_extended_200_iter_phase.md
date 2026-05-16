# ADR-0006: 200-iter extended recovery cycle for tasks losing to DSBench

## Status

Accepted (2026-05-15). Lesson 2 in `framework/CLAUDE_template.md`.

## Context

After the base 125-experiment hill-climb (5 backbones × 25 iters), a non-trivial fraction of modeling tasks still lose to their DSBench baseline. The base loop covers the **dominant axes** (depth, lr, subsample, colsample, reg_lambda, num_leaves, early-stop iter, seed) of 5 backbone families. It does not exhaust the SOTA frontier:

- xgboost-deep (depth ∈ {10, 12} with lr ∈ {0.01, 0.03} and `iterations=1200`) is undersampled.
- LightGBM's GOSS regime at `num_leaves ∈ {127, 255}` is not in the base 25.
- CatBoost's ordered-boosting recipe is not in the base.
- Tabular foundation models (TabPFN, TabNet, NGBoost) are not in the base.
- Stacked-ensemble dispatchers are not in the base.

A naive expansion ("run 50 iters per backbone instead of 25") doubles the compute everywhere. Better: **conditionally** run a 200-iter extension only on tasks that didn't beat DSBench in the base phase.

## Decision

`framework/extended_hill_climb.py` runs a **200-iteration recovery cycle** on any task that finishes the base 125 still losing to its DSBench baseline. The extension:

- **Same runner backbones.** Dispatches proposals through the existing 5 runner backbones (`xgboost`, `lightgbm`, `catboost`, `mlp`, `ft_transformer`); proposals targeting families the runner doesn't natively implement (NGBoost, TabNet, TabPFN, PatchTSMixer, stacking) hit the closest implementation with the appropriate regularisation lever.
- **15 backbone families.** xgboost-deep, lightgbm-goss, catboost-ordered, mlp-residual, ft-transformer-large, hgb, extra-trees, random-forest, elastic-net-stack, ngboost-proxy, tabnet-proxy, tabpfn-proxy, lstm-tabular, patch-tsmixer, sklearn-stack-ensemble.
- **Citation discipline preserved.** Every iter cites its motivating paper — Chen & Guestrin 2016 KDD (arXiv:1603.02754); Ke et al. 2017 NeurIPS (arXiv:1711.05101); Prokhorenkova et al. 2018 NeurIPS (arXiv:1706.09516); Hollmann et al. 2023 ICLR 'TabPFN'; Arik & Pfister 2021 AAAI 'TabNet'; Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).
- **Appends to the same `experiment_log.jsonl`.** Iters 126..325 join the base 1..125. The dashboard, reasoning annotations, and winner-archive machinery cover the extension without modification.

Stopping condition: 200 iters complete OR the task beats its DSBench baseline by composite delta > 0.02 (early-success exit), whichever comes first.

## Consequences

**Easier:**

- Compute scales with **need**, not budget — winning tasks stop at 125; losing tasks try harder.
- A reviewer reads one log file per task regardless of which phase ran.
- New backbone families slot in by adding a proposal block to `_common_proposals()`.

**Harder:**

- Tasks that beat DSBench in the base phase don't get the extension's deeper search. A task that wins by composite +0.001 might have won by +0.05 with the extension. Mitigated by the per-task seed-variance run inside the base 25.

**Riskier:**

- The "proxy" dispatchers (TabPFN-proxy via FT-Transformer with extreme regularisation) are not faithful reproductions of the target backbone. They are best-effort approximations; a reviewer should not treat a TabPFN-proxy champion as a real TabPFN claim. The submission archive's `audit_report.md` § 13 (Known limitations) documents the substitution.

## Related

- [`../part_3_processes/14_larger_testing.md`](../part_3_processes/14_larger_testing.md)
- Skill `extended-hill-climb-phase`.
- `framework/extended_hill_climb.py` and `framework/run_extended.py`.
