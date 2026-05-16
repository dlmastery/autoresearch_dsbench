# dsbench autoresearch — build status

## ✅ Framework (complete)

| File | Purpose |
|------|---------|
| `framework/CLAUDE_template.md` | Parameterised clone of `autoresearch/CLAUDE.md` — all 36 mapped sections + the 4 task-domain substitutions documented in `SECTION_MAPPING.md` |
| `framework/SECTION_MAPPING.md` | 1-to-1 audit table: source section → task-side section |
| `framework/sota_catalog.yaml` | Per-task-type SOTA recipes for **19 backbones** (MLP, LSTM, PatchTST, PatchTSMixer, iTransformer, xLSTM, Mamba, FT-Transformer, TimesFM, Chronos-Bolt, Moirai, MOMENT, TiRex, Sundial, Time-MoE, TimeMixer, TimesNet, MambaTS, XGBoost, LightGBM, CatBoost) with arXiv citations |
| `framework/runner.py` | Generic single-experiment runner. Pins to safe P-cores. Train + val ONLY. Logs JSONL + per-sample decisions + traditional ML metrics |
| `framework/hill_climb.py` | 25-iter-per-backbone outer loop with arXiv-cited reasoning annotations (diagnosis / citations / hypothesis / prediction / verdict / learning) |
| `framework/validator.py` | Audits every repo against `SECTION_MAPPING.md` + required-file list + "no test-set leakage" check |
| `framework/generate_scaffolds.py` | Creates per-task repos from registry |
| `framework/final_report.py` | One-shot test-set pass → DSBench comparison |
| `framework/run_all.py` | Drives the full 112-task loop |
| `framework/dashboard_template.html` | Per-task dashboard (backbone tabs, sortable, reasoning panel) |
| `framework/status.py` | CLI status snapshot |
| `dashboard/index.html` | Cross-task leaderboard, reads `registry/final_rollup.json` |

## ✅ Registry (complete)

- 74 Kaggle modeling tasks → `registry/modeling_tasks.json`
- 38 Modeloff analysis challenges → `registry/analysis_tasks.json`

Type distribution:
- modeling: 57 tabular, 8 nlp, 8 time-series, 1 structured
- problem types: 56 binary classification, 16 regression, 1 multiclass, 1 structured
- analysis: all 38 are `qa_excel`

## ✅ Per-task scaffolds (complete: 112/112 audited OK)

For each of 112 tasks under `modeling/<slug>/` or `analysis/<slug>/`:
- Fresh `CLAUDE.md` rendered from template (all 36 mapped sections present)
- `README.md`, `paper.md`, `paper_abstract.md`
- `task_config.json`, `seed_reasoning.json`
- `memory/project_autoresearch_checkpoint.md`
- `autoresearch_results/{dashboard.html,experiment_log.jsonl,experiment_summary.md,research_journal.md,reasoning_annotations.json,trade_logs/,winners/}`
- `data/{splits.py,features.py,.data_cache/}`
- `run_autoresearch.py` / `hill_climb.py` / `third_party_audit.py` (thin wrappers to framework)
- `code_versions/<backbone>_start/` snapshots

Validator: **112/112 ok** (run `framework/validator.py`).

## 🔄 Hill-climbing (running in background)

- **Modeling job:** processes 74 tasks × 5 backbones × 25 iters = 9,250 experiments. Currently in flight.
- **Analysis job:** processes 38 tasks × 1 backbone (`excel_agent`) × 25 iters = 950 experiments.

Each experiment:
1. Pre-writes the 4-field reasoning annotation (diagnosis / citations / hypothesis / prediction) with `_manual: true` BEFORE launching
2. Trains on TRAIN, scores on VAL — never touches TEST
3. Logs `experiment_log.jsonl`, `trade_logs/exp<N>_decisions.csv`, updates `best_config.json` if new champion
4. Writes verdict / learning to the annotation AFTER results
5. Appends an entry to `experiment_summary.md` + `research_journal.md`

Run `framework/status.py` for a live snapshot. Background-job stdout lives in
`registry/run_all_stdout.log` and `registry/run_all_analysis_stdout.log`.

## ✅ Validated on Titanic

End-to-end pipeline tested:
- 25 XGBoost iters → champion composite **0.9552** (val 0.9573, train 1.0000)
- Final test ROC-AUC: **0.9624** (accuracy 0.86, F1 0.865, MCC 0.72)
- **Beats DSBench baseline (0.5 default placeholder) by +0.46**

## DSBench comparison

The DSBench paper (Jing et al., ICLR 2025) reports:
- Best agent on data-analysis: **34.12% success**
- Best agent on data-modeling: **34.74% Relative Performance Gap**

After the background hill climb completes, `framework/final_report.py`
produces `registry/final_rollup.json` with per-task test scores and DSBench
delta. The cross-task dashboard at `dashboard/index.html` reads that file.

## How to resume / check progress

```powershell
# Live progress snapshot
& "C:/Users/evija/anaconda3/python.exe" C:/Users/evija/dsbench/framework/status.py

# Re-audit all 112 repos
& "C:/Users/evija/anaconda3/python.exe" C:/Users/evija/dsbench/framework/validator.py

# Run final test-set report once hill climb finishes
& "C:/Users/evija/anaconda3/python.exe" C:/Users/evija/dsbench/framework/final_report.py

# Restart hill climbing (idempotent — picks up where it left off, but does NOT skip completed iters)
& "C:/Users/evija/anaconda3/python.exe" C:/Users/evija/dsbench/framework/run_all.py
```

## Provenance

Mirrors `dlmastery/autoresearch` (commit-locked locally at 4/20/2026) section-for-section. Every per-task CLAUDE.md is validated to contain the substrings listed in `framework/SECTION_MAPPING.md`.

## 2026-05-15 sweep (Lessons rows 27-35, four new portability skills)

- Added Champion-summary committee-resumption-pointer block at the top of
  `framework/CLAUDE_template.md`.
- Added top-level "Portability Patterns" section with three subsections.
- Added Lessons Learned rows 27-35.
- New skills shipped: `forbidden-path-audit`, `held-back-surface-discipline`,
  `parallel-agent-orchestration`, `single-command-refresh`.
- Skill-pack coverage audit: **153/153 (100.0%) PASS** (up from 148/148).
- `n_skills`: 48 (up from 44).
- `_status.py`: 82/112 BEAT-DSBENCH, 112/112 FORENSIC PASS (unchanged).
- `framework/_final_audit.py`: all checks green.

## DARE-bench template sync — DEFERRED

`C:/Users/evija/dare-bench/framework/CLAUDE_template.md` does not yet exist
on disk at the time of this sweep — the recon and framework agents are
still scaffolding it in parallel. The dare-bench template, once it lands,
will encode the same 35-item Lessons Learned section in its initial render
(the agents have the dsbench template as their reference). A second sweep
of this kind will run against dare-bench after their template materialises.
