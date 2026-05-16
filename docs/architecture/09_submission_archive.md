# Submission Archive — The Per-Task Committee Bundle

> Audience: a committee reviewer who has been handed `submissions/dsbench_submission/<kind>/<slug>/` and needs to verify the claim without setting up the rest of the repo.

## 1. The contract

Every task — winner OR loser — has a self-contained, portable archive at:

```
submissions/dsbench_submission/<kind>/<slug>/
```

`<kind>` is `modeling` or `analysis`; `<slug>` matches the task identifier in the registry. The archive is built by `framework/build_submission.py` after every batch that updates a champion. The contract is **14 files**; missing any file invalidates the submission.

## 2. The 14 files

| # | File | Source | What it lets a reviewer do |
|---|---|---|---|
| 1 | `README.md` | hand-rendered from `task_config.json` + `final_report.json` | Task summary + champion + DSBench delta in plain English |
| 2 | `config.json` | copy of `best_config.json` | Exact champion config (backbone + params + composite) |
| 3 | `final_report.json` | copy of `<repo>/autoresearch_results/final_report.json` | One-shot test-set score + DSBench delta + BEAT/MISS flag |
| 4 | `runner_up.json` | `_runner_up(repo)` — second-best entry from `experiment_log.jsonl` | Variance baseline (how close was the next-best?) |
| 5 | `audit_report.md` | `_audit_report_skeleton` | 14-section explainability audit |
| 6 | `forensic_audit.md` | copy of `<repo>/forensic_audit.md` | 10-agent committee narrative |
| 7 | `forensic_audit.json` | copy of `<repo>/forensic_audit.json` | Machine-readable agent verdicts |
| 8 | `research_journal.md` | copy of `<repo>/autoresearch_results/research_journal.md` | Per-experiment 6-field reasoning narrative |
| 9 | `experiment_summary.md` | copy of `<repo>/autoresearch_results/experiment_summary.md` | Tabular per-experiment digest |
| 10 | `experiment_log.jsonl` | copy of `<repo>/autoresearch_results/experiment_log.jsonl` | Append-only raw ledger of every iter |
| 11 | `reasoning_annotations.json` | copy of `<repo>/autoresearch_results/reasoning_annotations.json` | Machine-readable per-experiment reasoning |
| 12 | `code/{CLAUDE.md, task_config.json, paper.md, paper_abstract.md, seed_reasoning.json}` | frozen task snapshot | Read the protocol and task definition |
| 13 | `inference/predict.py` | hand-rendered from the champion backbone + params | Standalone inference script (no framework imports) |
| 14 | `reproduction/reproduce_log.txt` | hand-rendered | Copy-pasteable PowerShell to reproduce + expected composite |

The bundle is byte-stable for a given commit: re-running `build_submission.py` on the same `experiment_log.jsonl` produces an identical directory tree.

## 3. The README header

Every `README.md` opens with a four-row table that lets a reviewer see the verdict in 5 seconds:

```markdown
# titanic — Submission

| | |
|---|---|
| Task | titanic (modeling / classification_binary) |
| Champion backbone | xgboost (exp 7, depth=10, lr=0.04) |
| Test ROC-AUC | 0.9624 |
| DSBench baseline | 0.50 |
| Delta | +0.4624 (BEAT) |
| Forensic verdict | PASS (10/10 agents) |
```

## 4. Why include the runner-up

`runner_up.json` documents the second-best experiment. It is the closest analogue to a "control" — if the gap between champion and runner-up is tiny (say, composite delta < 0.005), the champion claim is fragile and a seed-perturbation re-run is warranted. The forensic Agent H (seed stability) cross-references this row.

## 5. Standalone inference

`inference/predict.py` is the only file in the archive that imports the model. The script:

```python
# inference/predict.py
import json, joblib, numpy as np
cfg = json.load(open("../config.json"))
model = joblib.load("../best_model.pkl")
def predict(X: np.ndarray) -> np.ndarray:
    return model.predict(X)
```

The accompanying `inference/README_inference.md` documents the expected feature schema (column order + dtype). A reviewer can clone the archive, install `numpy`, `scikit-learn`, `xgboost` (or the relevant backbone library), and run `python predict.py` without the rest of `framework/`.

## 6. The reproduction recipe

`reproduction/reproduce_log.txt`:

```
# Reproduce the champion of titanic
cd C:/Users/evija/dsbench
& "C:/Users/evija/anaconda3/python.exe" framework/runner.py \
    --repo modeling/titanic \
    --backbone xgboost \
    --params '{"iterations":400,"max_depth":10,"lr":0.04,"subsample":0.8}' \
    --description "reproduce champion" \
    --experiment-num 9999

# Expected: composite ≈ 0.9555 ± 0.005 (Agent I tolerance)
```

The expected composite plus tolerance is the contract for Agent I (refit-consistency). A reproduction outside ±0.005 of the recorded composite indicates a stale model checkpoint, an un-wired config param, or a non-deterministic training step.

## 7. Top-level `SUBMISSION_README.md`

`submissions/SUBMISSION_README.md` is the entry point for a reviewer. It lists all 112 tasks with one line each:

```
- titanic (modeling/classification_binary): BEAT +0.4624 (test 0.9624, baseline 0.50)
- santander-customer-transaction-prediction (modeling/classification_binary): MISS -0.0123 ...
```

It is generated by `framework/build_submission.py` after every batch.

## 8. Anti-patterns

- **Hand-editing `audit_report.md`.** The builder regenerates this file on every run. Edits live in `<repo>/autoresearch_results/winners/<...>/audit_report.md` and propagate to the submission on next build.
- **Stale `runner_up.json`.** If the runner-up was logged before a bug fix, it may not be a valid baseline. Re-run the builder after every code change that affects the runner.
- **Missing `inference/predict.py` for `qa_excel` tasks.** The `excel_agent` backbone does not produce a `best_model.pkl`; the inference script must instead reconstruct the per-task prior from `config.json`. The builder handles this case.

## 9. Related

- [`../reference/api_build_submission.md`](../reference/api_build_submission.md)
- [`../runbooks/04_release_to_committee.md`](../runbooks/04_release_to_committee.md)
- [`06_explainability_audit.md`](06_explainability_audit.md)
