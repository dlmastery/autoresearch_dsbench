# DSBench AutoResearch

**Autonomous DSBench solver** — Karpathy-style hill-climbing applied to each of the 74 Kaggle data-modeling tasks and 38 Modeloff data-analysis challenges of [DSBench (ICLR 2025)](https://github.com/LiqiangJing/DSBench).

Each benchmark is a stand-alone autoresearch repo with its own `CLAUDE.md`, `paper.md`, runner, hill-climbing loop, dashboard, audit reports, and winner archive — mirroring [`dlmastery/autoresearch`](https://github.com/dlmastery/autoresearch) verbatim. A shared framework provides the SOTA backbones (MLP, LSTM, PatchTST, iTransformer, xLSTM, Mamba, TimesFM, Chronos, XGBoost, LightGBM, CatBoost, MOMENT, Moirai, TiRex, Sundial, Time-MoE, TimeMixer, TimesNet, MambaTS) and a parameterised CLAUDE template, then a generator instantiates one task-specific clone per benchmark.

A validator/auditor compares every generated `CLAUDE.md` against the original autoresearch `CLAUDE.md` section-by-section and refuses to declare a task "ready" until all 52 sections survive, all artefacts exist, and at least 25 hill-climbing iterations per backbone have been logged on train/val (test set is held back for the final report-only comparison against DSBench).

## Goal

> Meet or beat DSBench's published baselines (best agent = 34.12% data-analysis success, 34.74% Relative Performance Gap on data-modeling, ICLR 2025) on **every benchmark**, by treating each task as its own autoresearch run.

## Layout

```
dsbench/
├── framework/                  # shared autoresearch harness
│   ├── CLAUDE_template.md      # parameterised clone of autoresearch CLAUDE.md
│   ├── SECTION_MAPPING.md      # 1-to-1 audit vs source CLAUDE.md
│   ├── sota_catalog.yaml       # per-task-type recipes (epochs, lr, opt, paper)
│   ├── runner.py               # generic single-experiment runner (LOGS ONLY)
│   ├── hill_climb.py           # 25-iters-per-backbone outer loop
│   ├── validator.py            # auditor — diffs each task's CLAUDE vs source
│   ├── generate_scaffolds.py   # creates per-task repos from registry
│   ├── backbones/              # MLP, LSTM, PatchTST, ..., GBM
│   └── evaluation/             # metrics, splits, audit-report builder
├── registry/
│   ├── modeling_tasks.json     # 74 Kaggle competitions
│   └── analysis_tasks.json     # 38 Modeloff challenges
├── modeling/<task_name>/       # 74 self-contained autoresearch repos
│   ├── CLAUDE.md               # fresh per-task, all 52 sections
│   ├── README.md, paper.md, paper_abstract.md
│   ├── memory/project_autoresearch_checkpoint.md
│   ├── autoresearch_results/
│   │   ├── experiment_log.jsonl
│   │   ├── best_config.json
│   │   ├── reasoning_annotations.json
│   │   ├── experiment_summary.md
│   │   ├── research_journal.md
│   │   ├── trade_logs/
│   │   ├── winners/
│   │   └── dashboard.html
│   ├── run_autoresearch.py
│   ├── hill_climb.py
│   └── third_party_audit.py
├── analysis/<challenge_name>/  # 38 self-contained autoresearch repos
│   └── (same structure)
└── dashboard/                  # cross-task roll-up of all 112 leaderboards
    └── index.html
```

## Quick start

```powershell
# 1. Build the shared framework + generate all 112 task scaffolds
& "C:/Users/evija/anaconda3/python.exe" framework/generate_scaffolds.py

# 2. Audit every generated repo against original autoresearch CLAUDE.md
& "C:/Users/evija/anaconda3/python.exe" framework/validator.py --strict

# 3. Run hill climbing on every task (25 iters per backbone, train/val only)
& "C:/Users/evija/anaconda3/python.exe" framework/hill_climb.py --all

# 4. Final DSBench-comparison report (touches test set ONCE)
& "C:/Users/evija/anaconda3/python.exe" framework/final_report.py
```

## Provenance

- Inherits 52 sections + protocol rules from [`autoresearch/CLAUDE.md`](C:/Users/evija/autoresearch/CLAUDE.md) (4/20/2026)
- Uses [`generalized_ml_autoresearch/templates/CLAUDE_template.md`](C:/Users/evija/autoresearch/generalized_ml_autoresearch/templates/CLAUDE_template.md) as the parameterisation reference
- DSBench data and baselines: [LiqiangJing/DSBench](https://github.com/LiqiangJing/DSBench) (ICLR 2025)

License: MIT (matches autoresearch).
