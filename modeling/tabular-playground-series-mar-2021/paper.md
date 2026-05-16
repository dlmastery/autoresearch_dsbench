# AutoResearch on tabular-playground-series-mar-2021 — Paper

## 1. Introduction

DSBench `tabular-playground-series-mar-2021` is a classification_binary benchmark on tabular data; see https://www.kaggle.com/competitions/tabular-playground-series-mar-2021. We apply the autoresearch loop with per-backbone 25-iter hill climbing, arXiv-cited reasoning per experiment, and a frozen test split touched only by `framework/final_report.py`.

## 2. Method

2.1 **Composite metric:** `min(val_score, train_score) - 0.05 * abs(val_score - train_score)`. This penalises overfit by 5 cents per absolute gap unit.

2.2 **Backbone catalog:** xgboost, lightgbm, catboost, mlp, ft_transformer. Each backbone starts from `framework/sota_catalog.yaml` defaults and is hill-climbed for 25 iters with arXiv-cited perturbations (see `autoresearch_results/research_journal.md`).

2.3 **Train/val/test split:** 70/15/15 with seed 42, recorded in `data/split_manifest.json`. Hashes are verified at every runner start.

## 3. Hill-Climb Trajectory

See `autoresearch_results/experiment_summary.md` for the per-experiment table and `autoresearch_results/research_journal.md` for diagnosis / hypothesis / verdict narratives.

## 4. Final DSBench Comparison

See `autoresearch_results/final_report.json` after `framework/final_report.py` runs the one-and-only test-set pass.

## References

See `autoresearch_results/reasoning_annotations.json` for the full per-experiment citation table.
