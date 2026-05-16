---
name: extended-hill-climb-phase
description: Extended hill-climb phase — a 200-iter recovery cycle for tasks that lose to baseline after the base 25-iter × 5-backbone (125-exp) phase. Probes 15 backbone-families through the existing runner with arXiv-cited reasoning per iter. Triggers on "extended hill climb", "200-iter recovery", "loss tasks", "extra backbones", "below baseline", "lift below dsbench".
metadata:
  category: protocol
  source: dsbench
  related: [per-backbone-experiment-mandate, per-backbone-sota-recipes, monotonic-quality-progression]
---

# Extended Hill-Climb Phase (200-iter recovery cycle)

## When to use

- The base 25-iter × 5-backbone phase (125 experiments) finished and the champion still loses to the DSBench baseline.
- A task with a known-hard regression target (e.g. heavy-tailed or low signal-to-noise) where the SOTA defaults are obviously underexploring the HP surface.
- Before declaring a task "permanently below baseline" — extended hill-climb is the second-chance discipline.

## The rule

`framework/extended_hill_climb.py` appends iters 126..325 to the existing `experiment_log.jsonl`. Every proposal:

1. **Is a single config change** dispatched through one of the 5 native runner backbones (`xgboost`, `lightgbm`, `catboost`, `mlp`, `ft_transformer`). Proposals targeting families the runner doesn't natively implement (NGBoost, TabNet, TabPFN, PatchTSMixer, LSTM-tabular) hit the closest implementation with the appropriate regularisation lever.
2. **Cites the seminal paper for the targeted family.** No paper, no iter.
3. **Probes deeper hyperparameter perturbation** than the base 25-iter cycle: deeper trees, larger leaf counts, stronger regularisation, ensemble dispatchers, slow-and-many vs fast-and-few schedules.

The 15 backbone-families covered (rough iter budgets):

| Family | Iters | Dispatched via | Citation |
|---|---|---|---|
| xgboost-deep | 14-16 | xgboost | Chen & Guestrin 2016 KDD (arXiv:1603.02754) |
| lightgbm-goss | 8-10 | lightgbm | Ke et al. 2017 NeurIPS (arXiv:1711.05101) |
| catboost-ordered | 8-10 | catboost | Prokhorenkova et al. 2018 NeurIPS (arXiv:1706.09516) |
| mlp-residual | 10-12 | mlp | He et al. 2016 CVPR (arXiv:1512.03385) |
| ft-transformer-large | 10 | ft_transformer | Gorishniy et al. 2021 NeurIPS (arXiv:2106.11959) |
| hgb | 6 | (sklearn HGB via xgboost shim) | Friedman 2001 AoS |
| extra-trees / random-forest | 6 | mlp/xgboost shim | Geurts et al. 2006; Breiman 2001 |
| elastic-net-stack | 6 | mlp linear head | Zou & Hastie 2005 JRSS-B |
| ngboost | 6 | xgboost reg_alpha lever | Duan et al. 2020 ICML (arXiv:1910.03225) |
| tabnet-proxy | 6 | mlp residual | Arik & Pfister 2019 (arXiv:1908.07442) |
| tabpfn-proxy | 6 | ft_transformer extreme reg | Hollmann et al. 2022 (arXiv:2207.01848) |
| lstm-tabular | 6 | mlp sequence | Hochreiter & Schmidhuber 1997 Neural Comp |
| patch-tsmixer | 4 | mlp patches | Chen et al. 2023 (arXiv:2306.09364) |
| sklearn-stack-ensemble | 6 | meta-model dispatch | Wolpert 1992 NN |
| seed-variance probe | 6 | best-backbone reseeded | Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101) |

## Anti-patterns

- **Running extended-hill-climb on a task that already beats baseline.** Wastes compute and may erode the champion via seed variance — only run when below baseline.
- **Skipping the citation per iter.** "Try deeper" without a paper reference re-creates the very blind-sweep behaviour the protocol forbids.
- **Reusing the base 25-iter HP ranges.** Extended phase MUST probe the corners (very deep, very slow, very regularised); otherwise it's a re-run.
- **Appending to a different log file.** The same `experiment_log.jsonl` continues so the dashboard / reasoning-annotations / winner-archive infra work without changes.
- **Adding a new native backbone implementation without updating `final_report.py` refit logic.** If the runner doesn't natively load the backbone, refit-consistency (agent I) will fail.

## Implementation checklist

1. `framework/extended_hill_climb.py` builds a `list[(backbone, params, diagnosis, citations, hypothesis, prediction)]` of length ≥ 200.
2. Each tuple dispatches to `framework.runner.run_one()` with the named native backbone.
3. The runner appends to `autoresearch_results/experiment_log.jsonl` and updates `best_config.json` only on a new global champion (same protocol as base hill-climb).
4. Per-iter reasoning annotation written before the run (per `dashboard-reasoning-annotations`).
5. Citations conform to the 6-element `citation-rigor` spec.
6. After 200 iters, `framework/final_report.py` re-runs the test-set scoring with the new champion.

## References

- Source: `framework/extended_hill_climb.py` (DSBench codebase, 2026-05).
- Source: `framework/CLAUDE_template.md` section "Extended Hill-Climb Phase".
- Friedman 2001 Annals of Statistics 'Greedy Function Approximation: A Gradient Boosting Machine' — gradient boosting foundation.
- Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting baseline.
- Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW recipe for neural backbones.
- Related: `per-backbone-experiment-mandate`, `per-backbone-sota-recipes`, `monotonic-quality-progression`, `citation-rigor`.
