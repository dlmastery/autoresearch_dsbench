# DSBench Submission — autoresearch protocol applied to 112 tasks

_Generated 2026-05-16 17:36:26._

- **Total tasks:** 112
- **Beat DSBench baseline:** 83 (74.1%)
- **Modeling:** 74 / 74 beat
- **Analysis:** 9 / 38 beat

## Layout

```
submissions/dsbench_submission/
├── modeling/<slug>/
│   ├── README.md, config.json, final_report.json, runner_up.json
│   ├── audit_report.md (14-section explainability)
│   ├── forensic_audit.md (8-agent integrity)
│   ├── research_journal.md, experiment_summary.md
│   ├── experiment_log.jsonl, reasoning_annotations.json
│   ├── code/  (frozen CLAUDE.md + task_config + paper)
│   ├── inference/predict.py
│   └── reproduction/reproduce_log.txt
└── analysis/<slug>/  (same structure)
```

## Provenance

- Protocol: `autoresearch/CLAUDE.md` (4/20/2026) — 52 sections, all preserved
- Innovations from `autoresearchindexspy/autoresearchspy/CLAUDE.md`: champion lineage block, stacked ensemble design, regime gate, robustness audit, resumption pointers
- Per-task hill climb: 125 base + 200 extended = up to 325 arXiv-cited iters per regression task
- Forensic audit: 8 independent agents (split-hash, target-leakage, row-overlap, distribution-shift, anomaly, static-code, temporal, seed-stability) + committee verdict
- All results train/val only; test set scored ONCE per `framework/final_report.py`.

## How a committee evaluates this submission

1. Open `index.html` (root submissions dir) for cross-task leaderboard with sortable columns, delta histogram, forensic verdict panel, and per-task drill-down.
2. Spot-check 5 tasks at random: open `<task>/README.md`, verify the `audit_report.md` 14 sections are present, the `forensic_audit.md` committee verdict is PASS, and `reproduction/reproduce_log.txt` gives a runnable command.
3. Verify `research_journal.md` shows the 6-field reasoning per experiment (diagnosis / citations / hypothesis / prediction / verdict / learning) with full arXiv references.
4. The cross-task summary above is signed by the SHA256 of `final_rollup.json` at submission time — see `submissions/final_rollup.sha256`.
