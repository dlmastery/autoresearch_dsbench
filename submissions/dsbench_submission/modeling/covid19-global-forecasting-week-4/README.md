# DSBench submission — covid19-global-forecasting-week-4

- **Kind:** modeling
- **Problem:** regression
- **Metric:** rmse
- **Champion backbone:** mlp
- **Composite (train/val):** -0.3611
- **Test score:** -0.3356
- **DSBench baseline:** -1.0000
- **Delta vs DSBench:** +0.6644  (BEAT)

## Contents

- `config.json` — full champion configuration (backbone + params + metrics)
- `final_report.json` — one-shot test-set scoring vs DSBench baseline
- `runner_up.json` — second-best experiment for variance baseline
- `audit_report.md` — 14-section explainability audit (per autoresearch CLAUDE.md)
- `forensic_audit.md` — 8-agent forensic audit (cheating / leakage / drift)
- `research_journal.md` — full reasoning trace per experiment (diagnosis → citations → hypothesis → prediction → verdict → learning)
- `experiment_summary.md` — tabular summary of every experiment
- `experiment_log.jsonl` — append-only raw log of every experiment
- `reasoning_annotations.json` — machine-readable per-experiment reasoning
- `inference/predict.py` — standalone inference script
- `code/CLAUDE.md` — task-specific protocol clone (52 sections)
- `code/task_config.json` — task definition
- `reproduction/reproduce_log.txt` — command + expected composite for repro
