# Data Model — Task Config, Experiment Log, Reasoning Annotations

> Audience: an engineer who needs to read or write any of the artefacts the framework produces.

## 1. Task config (`task_config.json`)

One file per task. Frozen at scaffold-generation time. Read by `framework.runner.TaskConfig.load`.

```json
{
  "name": "titanic",
  "slug": "titanic",
  "kind": "modeling",
  "problem_type": "classification_binary",
  "task_type": "tabular",
  "metric": "roc_auc",
  "iterations_per_backbone": 25,
  "backbones": ["xgboost", "lightgbm", "catboost", "mlp", "ft_transformer"],
  "dsbench_baseline": 0.50
}
```

| Field | Type | Notes |
|---|---|---|
| `name` | str | Human-readable identifier, used in dashboards. |
| `slug` | str | Filesystem-safe identifier; matches the directory name under `modeling/` or `analysis/`. |
| `kind` | enum | `"modeling"` or `"analysis"`. |
| `problem_type` | enum | `classification_binary` / `classification_multiclass` / `regression` / `structured` / `qa_excel`. |
| `task_type` | str | `tabular` / `nlp` / `time-series` / `structured` / `qa-excel`. Free-text label used in dashboards. |
| `metric` | enum | `roc_auc` / `accuracy` / `macro_f1` / `rmse` / `mae` / `r2` / `exact_match_accuracy`. Higher-is-better after `runner._score` normalisation. |
| `iterations_per_backbone` | int | Default `25`. Per-backbone mandate, see [`../adr/0005_25_iters_per_backbone.md`](../adr/0005_25_iters_per_backbone.md). |
| `backbones` | list[str] | Ordered, ≤ 5 entries. The hill-climb consumes them sequentially. |
| `dsbench_baseline` | float \| null | Higher-is-better. RMSE baselines are pre-negated. |

## 2. Split manifest (`data/split_manifest.json`)

Written by `framework.runner._write_manifest`. Hashes are SHA-256 (16-char prefix) of `np.ndarray.tobytes()`.

```json
{
  "task_slug": "titanic",
  "n_train": 623, "n_val": 134, "n_test": 134,
  "n_features": 32,
  "hashes": {
    "X_train": "a4e8...", "y_train": "12cd...",
    "X_val":   "5f01...", "y_val":   "9c0a...",
    "X_test":  "77be...", "y_test":  "0fde..."
  },
  "generated_at": "2026-05-15 14:22:11",
  "warning": "test set is FROZEN — only used by framework/final_report.py"
}
```

The hashes are checked by Agent A of the forensic audit; mismatches FAIL the task.

## 3. Experiment log (`autoresearch_results/experiment_log.jsonl`)

One JSON object per line. Append-only. Written by `framework.runner._append_log` after every experiment.

```json
{
  "experiment_num": 7,
  "backbone": "xgboost",
  "description": "depth=10 lr=0.04 — push capacity past iter-2 depth=8 win",
  "params": {"iterations": 400, "max_depth": 10, "lr": 0.04},
  "metric": "roc_auc",
  "train_score": 0.9931,
  "val_score": 0.9573,
  "composite": 0.9555,
  "train_metrics": {"accuracy": 0.99, "f1": 0.99, "mcc": 0.97, "roc_auc": 0.9931},
  "val_metrics":   {"accuracy": 0.86, "f1": 0.87, "mcc": 0.72, "roc_auc": 0.9573},
  "elapsed_sec": 4.31,
  "timestamp": "2026-05-15 14:24:08",
  "task_slug": "titanic",
  "uses_test_set": false
}
```

`uses_test_set: false` is structural — `runner.run_one` never queries `X_test`. The flag exists so a downstream auditor can grep for any row claiming `true`.

## 4. Best-config (`autoresearch_results/best_config.json`)

Same schema as one experiment log entry, but overwritten on every new global champion (composite ratchet). `framework.runner._update_best_if_champion` enforces "only-if-strictly-greater" so ties keep the older entry. `framework.final_report.report_repo` reads this file for the one-shot test refit.

## 5. Reasoning annotations (`autoresearch_results/reasoning_annotations.json`)

Keyed by experiment number (as string). Authored by Claude **before** the experiment (4 fields) and **after** (2 fields).

```json
{
  "7": {
    "diagnosis": "Champion (iter-2 depth=8) achieved val=0.9520 with train/val gap 0.04. Per-fold breakdown shows fold-3 lagging by 1.2% AUC...",
    "citations": "Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — depth-vs-iter tradeoff section 4 argues...",
    "hypothesis": "Increase max_depth 8→10 with proportional lr drop 0.05→0.04 to keep the per-tree contribution constant. Mechanism: deeper trees model 3rd-order interactions...",
    "prediction": "Composite should move from 0.9543 to approximately 0.9550-0.9580. If gap > 0.05 the iter is exhausted as a direction.",
    "verdict": "KEEP — composite 0.9555, +0.0012 vs champion. Fold-3 recovered as predicted; fold-1 marginally regressed.",
    "learning": "Depth=10 is the new ceiling for this task. Going to depth=12 next would require lr ≤ 0.03 to keep per-tree contribution bounded.",
    "_manual": true
  }
}
```

Word-floor enforced by Layer 4 of the audit gate; see [`../adr/0015_four_layer_audit_gate.md`](../adr/0015_four_layer_audit_gate.md).

## 6. Trade logs (`autoresearch_results/trade_logs/exp<N>_decisions.csv`)

Per-sample decision log on the validation split. Written by `framework.runner._write_trade_log`.

```csv
sample_id,actual,prediction,correct,confidence
0,1,1,1,0.97
1,0,0,1,0.92
2,1,0,0,0.55
...
```

Companion `exp<N>_decision_summary.json` carries `n_val`, `accuracy`, and (for classification) per-fold totals.

## 7. Final report (`autoresearch_results/final_report.json`)

Written once per task by `framework.final_report.report_repo`. The only artefact that legally touched the test set.

```json
{
  "task": "titanic",
  "problem_type": "classification_binary",
  "metric": "roc_auc",
  "champion_backbone": "xgboost",
  "champion_composite": 0.9555,
  "champion_val": 0.9573,
  "champion_train": 0.9931,
  "test_score": 0.9624,
  "test_metrics": {"accuracy": 0.86, "f1": 0.865, "mcc": 0.72, "roc_auc": 0.9624},
  "dsbench_baseline": 0.50,
  "delta_vs_dsbench": 0.4624,
  "beats_dsbench": true,
  "timestamp": "2026-05-15 16:01:44"
}
```

## 8. Cross-task rollup (`registry/final_rollup.json`)

A list with one row per task, schema = the final-report dict above. Read by `framework/_status.py`, `framework/_summary.py`, `framework/_losses.py`, and the cross-task dashboard.

Companion `registry/forensic_summary.json` carries `kind` (modeling/analysis), `verdict` (PASS/FAIL), and per-agent risks. **Note the asymmetry:** rollup rows do not carry `kind` (modeling-vs-analysis is `problem_type != "qa_excel"`); forensic rows do carry `kind` explicitly. See [`../adr/0014_github_checkpoint_protocol.md`](../adr/0014_github_checkpoint_protocol.md) Lesson 14.

## 9. Submission archive (per task)

`submissions/dsbench_submission/<kind>/<slug>/` contains the 14 files documented in [`09_submission_archive.md`](09_submission_archive.md). The archive is a stable contract — every change goes through `framework/build_submission.py`.

## 10. Related

- [`03_runtime.md`](03_runtime.md) — how these artefacts get produced.
- [`08_dashboards.md`](08_dashboards.md) — how they get displayed.
- [`../reference/api_runner.md`](../reference/api_runner.md) — the API that writes them.
