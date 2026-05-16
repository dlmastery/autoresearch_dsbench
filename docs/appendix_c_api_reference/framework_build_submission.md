# API Reference — `framework.build_submission`

> Packages the 14-file per-task submission archive. See [`../part_4_tools/24_continuous_delivery.md`](../part_4_tools/24_continuous_delivery.md) for the contract.

## Module: `framework.build_submission`

`C:/Users/evija/dsbench/framework/build_submission.py`

## Public functions

### `build_submission(repo) -> Path`

Build the per-task submission archive at `submissions/dsbench_submission/<kind>/<slug>/`. Returns the destination path.

The archive contains the 14 files documented in [`../part_4_tools/24_continuous_delivery.md`](../part_4_tools/24_continuous_delivery.md):

1. `README.md` — task summary + champion + DSBench delta.
2. `config.json` — copy of `<repo>/autoresearch_results/best_config.json`.
3. `final_report.json` — copy of `<repo>/autoresearch_results/final_report.json`.
4. `runner_up.json` — second-best experiment (via `_runner_up(repo)`).
5. `audit_report.md` — 14-section explainability audit (via `_audit_report_skeleton`).
6. `forensic_audit.md` — copy of `<repo>/forensic_audit.md`.
7. `forensic_audit.json` — copy of `<repo>/forensic_audit.json`.
8. `research_journal.md` — copy of `<repo>/autoresearch_results/research_journal.md`.
9. `experiment_summary.md` — copy of `<repo>/autoresearch_results/experiment_summary.md`.
10. `experiment_log.jsonl` — copy of the full append-only log.
11. `reasoning_annotations.json` — copy.
12. `code/{CLAUDE.md, task_config.json, paper.md, paper_abstract.md, seed_reasoning.json}`.
13. `inference/predict.py` — standalone inference script.
14. `reproduction/reproduce_log.txt` — runnable repro command.

### `_audit_report_skeleton(repo, champion, final) -> str`

Generate the 14-section `audit_report.md` skeleton. Section content is populated from `best_config.json`, `final_report.json`, and the trade-log CSVs. Manual additions (Sections 10 and 13) survive re-builds.

### `_runner_up(repo) -> dict | None`

Return the second-best entry from `experiment_log.jsonl`, sorted by composite descending. Used as the variance baseline in the submission.

## CLI

```powershell
# All tasks
& "C:/Users/evija/anaconda3/python.exe" framework/build_submission.py

# One task
& "C:/Users/evija/anaconda3/python.exe" framework/build_submission.py --repo modeling/titanic
```

Also writes `submissions/SUBMISSION_README.md` listing all 112 tasks with BEAT/MISS verdict and delta.

## Related

- [`../part_4_tools/24_continuous_delivery.md`](../part_4_tools/24_continuous_delivery.md)
- [`../part_3_processes/10_documentation.md`](../part_3_processes/10_documentation.md)
- [`../part_4_tools/24_continuous_delivery.md`](../part_4_tools/24_continuous_delivery.md)
