# API Reference — `framework.hill_climb` and `framework.extended_hill_climb`

> The outer loops that drive `runner.run_one` through 25 + 200 cited proposals.

## Module: `framework.hill_climb`

`C:/Users/evija/dsbench/framework/hill_climb.py`

### Constants

| Constant | Value | Notes |
|---|---|---|
| `ITERATIONS_PER_BACKBONE` | `25` | Mandatory floor per [`../appendix_b_adrs/0005_25_iters_per_backbone.md`](../appendix_b_adrs/0005_25_iters_per_backbone.md). |
| `EXTENDED_ITERATIONS` | `200` | Cap for the extended phase; used by `extended_hill_climb.py`. |
| `COOLDOWN_SEC` | `0` (test mode) | Production runs use `30` per `framework/CLAUDE_template.md`. |

### `_xgb_proposals() -> list[tuple]`

Return `[(params, diagnosis, citation, hypothesis, prediction), ...]` for the 25 XGBoost iters. The first 10 are hand-curated; iters 11-25 are programmatically generated from `_xgb_extended()`.

The same shape is provided by `_lgbm_proposals()`, `_catboost_proposals()`, `_mlp_proposals()`, `_ft_proposals()`, and `_excel_agent_proposals()` for the respective backbones.

### `run_one_iteration(repo, backbone, params, description, citation, hypothesis, prediction, experiment_num) -> dict`

Wraps `runner.run_one` with pre/post reasoning-annotation writes:

1. Writes the 4 pre-experiment fields (`diagnosis`, `citations`, `hypothesis`, `prediction`) into `reasoning_annotations.json` keyed on `experiment_num`.
2. Calls `runner.run_one(...)`.
3. Writes the 2 post-experiment fields (`verdict`, `learning`) — synthesised from the result if Claude is not authoring.

### CLI

```powershell
& "C:/Users/evija/anaconda3/python.exe" framework/hill_climb.py --repo C:/Users/evija/dsbench/modeling/<slug>
```

Runs 25 iters × 5 backbones (or 25 × 1 for `qa_excel`) and appends them to `experiment_log.jsonl`. Idempotent — picks up at the next iter when the log is non-empty.

## Module: `framework.extended_hill_climb`

`C:/Users/evija/dsbench/framework/extended_hill_climb.py`

### `_common_proposals() -> list[tuple[str, dict, str, str, str, str]]`

Return `[(backbone, params, diagnosis, citations, hypothesis, prediction), ...]` — 200 proposals covering 15 backbone families. Each tuple targets one of the existing runner backbones (proposals targeting non-native families dispatch to the closest implementation with the appropriate regularisation lever). Citations are anchored to each backbone family's seminal paper.

### CLI

```powershell
& "C:/Users/evija/anaconda3/python.exe" framework/extended_hill_climb.py --repo C:/Users/evija/dsbench/modeling/<slug>
```

Appends iters 126..325 to the same `experiment_log.jsonl`. Triggered automatically by `framework/run_extended.py` for tasks identified by `framework/_losses.py`.

## Module: `framework.run_extended`

Driver that:
1. Reads `registry/losses.json` (written by `_losses.py`).
2. For each loss task, invokes `extended_hill_climb.py`.
3. Aggregates results back into `registry/final_rollup.json` after refit.

## Related

- [`framework_runner.md`](framework_runner.md)
- [`../part_3_processes/14_larger_testing.md`](../part_3_processes/14_larger_testing.md)
- [`../part_4_tools/18_build_systems.md`](../part_4_tools/18_build_systems.md)
