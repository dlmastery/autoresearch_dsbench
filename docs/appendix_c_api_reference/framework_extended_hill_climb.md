# API Reference — `framework.extended_hill_climb`

> The 200-iter extended-recovery hill-climb for tasks still losing to their DSBench baseline after the base 125-iter loop.

## Module: `framework.extended_hill_climb`

`C:/Users/evija/dsbench/framework/extended_hill_climb.py`

## Purpose

The base hill-climb (`framework.hill_climb`) runs 25 iters × 5 backbones = 125 experiments per modeling task. Tasks that finish the base loop still losing to `dsbench_baseline` are routed to this script for up to 200 additional iterations across **15 backbone families**.

The extended phase preserves the One-Knob Rule ([Ch. 8](../part_3_processes/08_style_guides_and_rules.md)) and the Six-Field Annotation Rule ([Ch. 10](../part_3_processes/10_documentation.md)). Proposals append to the same `experiment_log.jsonl` (no separate log).

## Public functions

### `run_extended(repo: Path, max_extra: int = 200) -> None`

Run up to `max_extra` extended iterations against task at `repo`. Stops early if the task beats its DSBench baseline by > 0.02 on the composite.

**Side effects:**

- Appends rows to `<repo>/autoresearch_results/experiment_log.jsonl` (iter numbers 126…325).
- Updates `<repo>/autoresearch_results/best_config.json` if a champion lands.
- Writes `<repo>/autoresearch_results/reasoning_annotations.json` entries with `_manual: false` for auto-generated annotations.

### Backbone families covered

| Family | Iters | Citation |
|---|---|---|
| `xgboost-deep` | 16 | Chen, Guestrin 2016 KDD *XGBoost: A Scalable Tree Boosting System* arXiv:1603.02754 |
| `lightgbm-goss` | 10 | Ke et al. 2017 NeurIPS *LightGBM* arXiv:1711.05101 |
| `catboost-ordered` | 8 | Prokhorenkova et al. 2018 NeurIPS *CatBoost* arXiv:1706.09516 |
| `mlp-residual` | 12 | Liu et al. 2024 ICLR *ResMLP for Tabular* |
| `ft-transformer-large` | 12 | Gorishniy et al. 2021 *Revisiting DL for Tabular* arXiv:2106.11189 |
| `hgb` | 8 | Friedman 2001 *Greedy Function Approximation* + sklearn HistGB docs |
| `extra-trees` | 6 | Geurts, Ernst, Wehenkel 2006 MLJ *Extremely Randomized Trees* |
| `random-forest` | 8 | Breiman 2001 *Random Forests* |
| `elastic-net-stack` | 6 | Zou, Hastie 2005 JRSS *Regularization and Variable Selection via the Elastic Net* |
| `ngboost-proxy` | 8 | Duan et al. 2020 ICML *NGBoost* |
| `tabnet-proxy` | 8 | Arik, Pfister 2021 AAAI *TabNet* |
| `tabpfn-proxy` | 6 | Hollmann et al. 2023 ICLR *TabPFN* |
| `lstm-tabular` | 8 | Hochreiter, Schmidhuber 1997 *LSTM* |
| `patch-tsmixer` | 8 | Ekambaram et al. 2023 KDD *TSMixer* |
| `sklearn-stack-ensemble` | 6 | Wolpert 1992 *Stacked Generalization* |

Total potential iters: 130. The framework rounds up to 200 by drawing additional seed-perturbation iters across families.

## CLI

```powershell
& "C:/Users/evija/anaconda3/python.exe" framework/extended_hill_climb.py --repo <task-path> [--max-extra 200]
```

Or driven by the wrapper `framework/run_extended.py` which iterates over every task whose `final_report.json` shows `beats_dsbench: false`.

## Related

- [Ch. 14 — Larger Testing](../part_3_processes/14_larger_testing.md): the 200-iter extension as part of the testing pyramid.
- [ADR 0006](../appendix_b_adrs/0006_extended_200_iter_phase.md): the decision rationale.
- [`framework/hill_climb.py`](../../framework/hill_climb.py): the base 125-iter loop.
- [`framework/sota_catalog.yaml`](../../framework/sota_catalog.yaml): per-family training recipes.
