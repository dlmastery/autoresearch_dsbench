# Postmortem 0004 — Conway's Reverse Game of Life misrouted as `binary_classification`

**Severity:** Medium
**Date:** 2026-05-15
**Owner:** framework author

## TL;DR

The Conway's Reverse Game of Life task is a **structured-prediction** problem: given a future cell configuration, predict the previous state across a 20x20 grid. It was initially registered with `problem_type: "classification_binary"` because each cell's prediction is a 0/1 — which is true at the cell level but wrong at the task level. The framework's tabular GBM backbones produced a per-cell accuracy near 0.50 (the random baseline), and the hill-climb couldn't improve because the wrong problem framing made every "axis" useless.

## Timeline

| Time | Event |
|---|---|
| Day 0 | `registry/modeling_tasks.json` registered `conway-s-reverse-game-of-life` with `problem_type: classification_binary`. |
| Day 0 + a few hours | Hill-climb runs 5 backbones × 25 iters on the task. Champion composite is 0.499 (chance). All XGBoost / LightGBM / CatBoost / MLP / FT-Transformer iterations converge to "predict 0 for all cells" or similar degenerate solutions. |
| Day 0 + late | Author inspects the per-fold val table. Notices that across all 125 experiments, val accuracy is in [0.49, 0.51]. This is suspicious — the random baseline on a real Conway task should be beatable. |
| Day 0 + later | Author reads the Kaggle task description and confirms it's a structured-prediction problem (per-grid-position prediction, not per-row classification). The framework's row-flattening loses all spatial structure. |
| Day +1 | Re-route to `problem_type: "structured"` and `task_type: "structured"`. The backbones change from GBM-centric to MLP / FT-Transformer / xgboost (per `generate_scaffolds.py:PROBLEM_TO_BACKBONES`). Re-runs the hill-climb. |
| Day +1 + a few hours | The structured-task accuracy is now slightly above chance (0.51) — still not great, but the framework is no longer giving a misleading 0.50 floor. |

## Root cause

**Technical:** Each cell prediction is binary, but each task instance is a **grid** of correlated binary predictions. Flattening the grid into 400 independent rows destroys the spatial structure that any non-trivial model needs. The "binary_classification" framing fits 400 independent per-cell models, which has no path to learning Conway dynamics.

**Systemic:** `registry/modeling_tasks.json` was built by inspecting Kaggle leaderboard categories and choosing the closest matching `problem_type` from the framework's enum. Conway's task isn't a clean fit for any of the four categories (`classification_binary` / `classification_multiclass` / `regression` / `qa_excel`). The author chose `classification_binary` because the labels are 0/1; the right choice was `structured`, which signals "this task needs special-case handling".

## Impact

- 1 task (`conway-s-reverse-game-of-life`) ran 125 useless experiments.
- ~3 hours of compute on the affected hill-climb iteration.
- No incorrect public claim — the DSBench-comparison column for this task was always BEAT-by-zero because both the framework's score AND the baseline were near chance.

## What went well

- The "val accuracy stuck at 0.50 for all 125 experiments" pattern is exactly the kind of anomaly the dashboard makes visible. The author noticed within a session.
- The fix is one row in `registry/modeling_tasks.json` plus a re-scaffold; no framework code change required.
- The framework's `problem_type: "structured"` was designed exactly for this case; the cost was just the misroute, not a missing capability.

## What went badly

- The `structured` problem-type doesn't have a dedicated SOTA backbone (it dispatches to a CNN-style PatchTSMixer or MLP). Conway is genuinely hard for tabular backbones; a proper fix would wire a U-Net-style backbone, which is out of scope for the current framework.
- The misroute was caught by hand-inspection. A pre-flight check that compared cell-level vs grid-level accuracy could have flagged this automatically.
- The `task_type` field is free-text and not validated. A typo would not be caught.

## Action items

| AI | Owner | Status | Tracking |
|---|---|---|---|
| Re-register Conway's Reverse Game of Life as `problem_type: "structured"` and regenerate scaffold | author | Done | `registry/modeling_tasks.json` |
| Document the structured-task ceiling in the per-task README | author | Open | TODO |
| Add a pre-flight check: if val accuracy stays in [0.49, 0.51] for the entire 25-iter exploration of any single backbone, FAIL Agent E with the new suspicion `degenerate_floor` | author | Open | TODO |
| Validate `problem_type` and `task_type` against an enum in `task_config.json` schema | author | Open | TODO |

## Related

- `registry/modeling_tasks.json`
- `framework/generate_scaffolds.py:PROBLEM_TO_BACKBONES`
- `framework/CLAUDE_template.md` § "Key Constants" (problem_type values).
- The `structured` branch of `framework/runner.py:load_or_make_data`.
