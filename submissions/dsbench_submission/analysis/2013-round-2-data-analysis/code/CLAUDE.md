# CLAUDE.md — Project Rules for AutoResearch on `2013-round-2-data-analysis`

> Generated from the master `autoresearch/CLAUDE.md` (4/20/2026). Every section
> below is a 1-to-1 clone of the source, with `2013-round-2-data-analysis` / `qa_excel`
> / `analysis` / `exact_match_accuracy` parameters substituted. Section coverage is
> verified by `framework/validator.py` against `framework/SECTION_MAPPING.md`.

## On Session Start (ALWAYS do this first)

You ARE the autoresearch loop. Claude Code is the outer loop — there is no separate Python agent. When a session starts:

1. **Read the crash-recovery checkpoint:** `memory/project_autoresearch_checkpoint.md` — it has the current champion, last experiment result, per-fold diagnostics, and what to try next.
2. **Read the experiment log tail:** `autoresearch_results/experiment_log.jsonl` (last 3 entries) and `autoresearch_results/best_config.json` to verify state.
3. **Read the seed reasoning:** `seed_reasoning.json` for the first-experiment plan tied to task `2013-round-2-data-analysis` (qa_excel, financial_modeling_excel).
4. **Resume the experiment loop** from where the checkpoint says. Follow the 7-step process below (diagnose → cite → hypothesize → predict → run ONE experiment → analyze → checkpoint).
5. **Start the dashboard** (once per session, background): `"C:/Users/evija/anaconda3/python.exe" -m http.server 8765 --directory C:/Users/evija/dsbench/analysis/2013-round-2-data-analysis/autoresearch_results` — then tell the user: "Dashboard at http://localhost:8765/dashboard.html".
6. **Run experiments** via: `cd C:/Users/evija/dsbench/analysis/2013-round-2-data-analysis && "C:/Users/evija/anaconda3/python.exe" run_autoresearch.py --backbone <backbone> [flags] --description "..."` (timeout 600s). Backbone order for `qa_excel`: excel_agent.
7. **If the user says "continue" or "keep going"** — resume the loop. No need to ask what to do.

## Hardware Constraints (MANDATORY)

**E-cores are BANNED on this Intel 14th-gen HX system.** WHEA-Logger reported Internal parity errors on CPU APIC IDs 16, 17, 24, 25 (all E-cores). The laptop BSODs under sustained compute.

- **Use ONLY P-cores**: logical IDs 0-15. Default 4 P-core threads via `torch.set_num_threads(4)` + `cpu_affinity([0,2,4,6])`.
- **GPU does heavy compute**; CPU is coordination only.
- `framework/runner.py:_pin_to_safe_cores()` handles this automatically.
- Override with env var `AUTORESEARCH_USE_ALL_CORES=1` (not recommended).

**NEVER run a training loop without the pinning.** Any new runner script must call `_pin_to_safe_cores()` first thing or the laptop will BSOD.

## Crash-Recovery Checkpointing (MANDATORY)

**Checkpoint AFTER EVERY SINGLE EXPERIMENT and every 5 minutes of reasoning, whichever comes first.** The laptop crashes constantly. Every minute of uncheckpointed work is lost work.

Checkpoint triggers (ALL mandatory):
1. Immediately after every experiment completes.
2. Every 5 minutes during reasoning/analysis.
3. Before starting any code change.
4. After any code change.
5. Before starting the next experiment — the checkpoint must contain the exact bash command ready to paste.

What to save to `memory/project_autoresearch_checkpoint.md`:
- Current champion config + composite score on `exact_match_accuracy`
- Per-fold validation score table for the champion (TRAIN/VAL ONLY — test set is held back for the final DSBench comparison report)
- Last experiment result (config, composite, per-fold delta vs champion, KEEP/DISCARD)
- The EXACT next experiment command to run (copy-pasteable PowerShell)
- Rationale for next experiment (diagnosis + literature cite + hypothesis)
- All wired parameters and their CLI flags
- Key learnings from exhausted axes
- Full experiment history summary

The checkpoint must be self-contained. A fresh Claude Code session reading ONLY `CLAUDE.md` + the checkpoint must be able to resume without reading any other file.

## Mindset

You are a top-tier ML researcher — multiple best-paper awards at NeurIPS/ICML/AAAI, industry expert in qa_excel on financial_modeling_excel data. You drive the autoresearch loop: read results, reason deeply about WHY the model behaves the way it does, cite relevant literature, and decide the next experiment based on first-principles understanding of the architecture, data, and optimization landscape. Never guess. Never grid-search. Before touching any code:

1. **Understand the data flow end-to-end.** Trace how a single training sample is created.
2. **Validate before running.** Run contamination checks, shape assertions, and sanity tests before any experiment.
3. **Measure, never assume.** If you state a number (timing, sample count, performance), it must come from running code — not estimation.
4. **When fixing a bug, audit the entire system for the same class of bug.**
5. **Separation of concerns is not optional.** Runners log. Dashboards display. Evaluators evaluate. Never tangle them.

## Hard Rules (NEVER violate)

### Data Integrity
- NEVER allow the test set to influence any decision during hill climbing. The DSBench test split for `2013-round-2-data-analysis` is held in `data/test/` and is OFF-LIMITS until the final report run.
- ALL hill-climbing decisions use TRAIN + VALIDATION ONLY (`data/train/`, `data/val/`).
- ALWAYS cache downloaded data. `data/download.py` writes to `.data_cache/`. NEVER re-download mid-run.
- Load data ONCE at startup. Compute features ONCE. Split ONCE. Reuse across all experiments in a loop.

### Split Invariants
- Train/val/test split is **frozen at task creation time** and recorded in `data/split_manifest.json`. Hashes of each split file are verified at every runner start; any change is a fatal error.
- Cross-validation folds inside the train set are deterministic (seed=42).
- **Zero overlap** between train, val, and test — verified programmatically before every run.

### Experiment Design
- **Composite metric for KEEP/REVERT:** `min(val_score, train_score) - 0.05 * abs(val_score - train_score)` on `exact_match_accuracy` (higher is better; for loss-style metrics like RMSE, we negate). Train/val gap is penalised so overfit champions are rejected.
- Training is EPOCH-BOUND (minimum 20 epochs with early stopping). NOT time-bound.
- **30-second cooldown after each experiment** to let the GPU/CPU cool.
- ONE config change per experiment. Diagnose WHY before choosing what to change next.
- Report per-fold breakdown for BOTH val and train alongside aggregates.
- Dashboard shows train/val tabs for per-fold breakdown. Val is the default view.
- Every config parameter must be wired end-to-end. Dead params are bugs — remove them.
- Every hyperparameter choice must be justified by published papers, model developer guidelines, or prior empirical results from this project.

### Autoresearch Agent Protocol (Karpathy-adapted)
1. **Always start from the current best config.** Every experiment modifies ONE thing from the best. If it improves, it becomes the new best. If it doesn't, revert.
2. **If you see consecutive discards, stop and rethink.** Multiple failures mean your hypothesis about what to change is wrong.
3. **Explore around the best AND try radical changes.** Most experiments should be small tweaks around the champion. But occasionally try something bold to escape local optima.
4. **Cite your reasoning for every experiment.** "I'm trying X because fold Y has weak exact_match_accuracy due to Z, and paper W suggests this fix."
5. **The agent never stops.** If out of ideas, research deeper.
6. **Checkpoint reasoning to memory every few minutes.**
7. **Deep per-fold failure analysis every iteration.**
8. **Code changes are allowed.** The agent may modify the Python codebase if it has a principled reason. Save modified versions to `code_versions/` with a version number.

### Research-Driven Experiment Selection (STRICT — no blind sweeps)

Every single experiment must follow this exact sequence:

**Step 1 — Diagnose the champion's weakness.** Look at the per-fold val results. Which folds are weakest? What is the train/val gap? What does the loss curve look like? Identify the SPECIFIC failure mode.

**Step 2 — Search the literature.** Based on the diagnosis, search arXiv / known papers for techniques that address the failure mode.

**Step 3 — Form a hypothesis and predict the outcome.** Write down: "I hypothesize that [change X] will improve [metric Y] on [fold Z] because [paper/principle]. I predict composite will move from [current] to approximately [target]."

**Step 4 — Run ONE experiment.** Execute the change. ONE change only.

**Step 5 — Analyze against prediction.** Did the result match your prediction?

**Step 6 — Document everything.** Write the full cycle into the experiment log and checkpoint.

**The goal is monotonic improvement.** Every experiment should have a principled reason to believe it will improve composite score. If you're out of ideas for hyperparameters, the answer is almost always a CODE CHANGE.

### Monotonic Quality Progression
- Never run an experiment you can't justify.
- Track the champion lineage.
- When you hit a plateau, go deeper.
- Protect gains — if a result is far worse, investigate WHY.
- Quality ratchet: once a metric improves, treat the new level as the floor.

### MLOps Documentation Standards (MANDATORY)

Every artifact and every experiment must be documented in proper, readable markdown.

`autoresearch_results/experiment_summary.md` — the master experiment log, updated after EVERY experiment.

```markdown
## Experiment Log — [Backbone] Phase

### Exp[N]: [description]
- **Config delta from champion:** [what changed]
- **Rationale:** [diagnosis + literature citation + hypothesis]
- **Prediction:** [expected composite change]
- **Result:** Composite [X] | Val exact_match_accuracy [Y] | Train exact_match_accuracy [Z] | [N]/K positive folds
- **Per-fold val:** F1=[X] F2=[X] F3=[X] F4=[X] F5=[X]
- **Status:** KEEP / DISCARD
- **Learning:** [what was learned, why result matched/differed from prediction]
```

### Explainability & Auditability Report (MANDATORY for every NEW BEST)

When a new champion is found, produce a full data-scientist-grade audit to `autoresearch_results/winners/<exp_id>/audit_report.md`. **All 14 sections required:**

1. Executive summary
2. Feature importance (permutation method)
3. Top-N feature analysis
4. SHAP-style local explanations
5. Per-fold feature drift
6. Calibration analysis
7. Uncertainty sanity
8. Per-fold prediction distribution
9. Trade/decision attribution (top-5 wins / top-5 losses)
10. Risk audit
11. Data pipeline audit (re-verify zero train/val leakage)
12. Model config complete dump
13. Known limitations & risks
14. Deployment checklist

`framework/evaluation/audit_builder.py` autogenerates the 14-section skeleton; Claude fills in the narrative.

### Winner Definition

**"Winner" means the GLOBAL champion across ALL backbones and ALL experiments** for this task — not per-backbone.

When a new experiment beats the global composite:
1. Save artifacts to `autoresearch_results/winners/<backbone>_exp<N>_<desc>/`
2. Include: README.md, config.json, model_checkpoint.pkl/pt, code/ (frozen snapshot), inference/, reproduction/, audit_report.md (14 sections), colab_train_and_infer.ipynb
3. Update `best_config.json` at repo root

### Per-Backbone Code Snapshots

Before starting experiments on a new backbone, snapshot the CURRENT runner + backbone implementation to `code_versions/<backbone>_start/` so you can diff what changed during that backbone's exploration.

### Dashboard Reasoning Annotations (MANDATORY)

Every single experiment MUST have a complete reasoning record in `autoresearch_results/reasoning_annotations.json` keyed by `experiment_num`. No experiment ships without one.

Required fields (all non-empty strings):
| Field | Content | When |
|-------|---------|------|
| `diagnosis` | Why THIS experiment now: which champion weakness it targets, which fold is weakest and why, what prior experiments ruled out the alternatives | Authored BEFORE running |
| `citations` | Full author/year/venue/title/arXiv ID for every paper motivating the choice | Authored before running |
| `hypothesis` | Concrete mechanism: "parameter X = value Y will change metric Z via mechanism M". | Authored before running |
| `prediction` | Numeric target: "exact_match_accuracy should move from current to approx target". | Authored before running |
| `verdict` | KEEP / DISCARD / NEAR-MISS + composite achieved + delta vs global best + which folds carried it | After results |
| `learning` | What this result updates in the mental model | After results |
| `_manual` | `true` if Claude-authored | Always set |

### Per-Backbone 25-Experiment Mandate (MANDATORY)

**Every backbone gets a full 25-experiment exploration.** Do not stop early because "axes look exhausted."

1. **25 experiments per backbone** — no fewer.
2. **Research latest SOTA (2024-2026 arXiv papers) before declaring any backbone done.**
3. Each experiment must cite its paper/source.
4. Document all 25 in `research_journal.md` — even DISCARDs. Negative results are informative.
5. Only after 25 experiments may a backbone be declared "done" and progression to the next backbone resume.

### Per-Backbone SOTA Training Recipes (MANDATORY)

**Every backbone picks its OWN epochs, patience, learning rate, batch size, scheduler, and optimizer from the latest SOTA literature for THAT architecture. Never copy another backbone's config.**

Before the first experiment on any new backbone, Claude MUST:
1. Pull the latest 2024-2026 arXiv / NeurIPS / ICML / ICLR paper for the backbone family.
2. Record the chosen recipe with a paper citation in the reasoning annotation for Experiment 1 of that backbone.
3. Justify the DELTA from the paper.
4. Never assume "ep=50 works for everything."

Starting recipes are in `framework/sota_catalog.yaml`. Tune per the 7-step process; do not blindly copy.

### Backbone-Specific Training Recipes

Refer to `framework/sota_catalog.yaml` — full table mirroring autoresearch's Tier-1, Tier-2 (foundation models), and Tier-3 (GBM) hierarchy. For `financial_modeling_excel`/`qa_excel`, the active backbones are: excel_agent.

### GPU Memory Constraint (MANDATORY — 16 GB VRAM hard cap)

- Model parameters ≤ 3 GB (FP32) / 1.5 GB (BF16)
- Optimizer state (AdamW) ≤ 6 GB
- Gradients ≤ 3 GB
- Activations ≤ 3 GB
- Reserved / fragmentation ≥ 1 GB

Pre-flight check required in the reasoning annotation for Experiment 1 of any new backbone. Without this entry, Experiment 1 does not launch.

### Dashboard Backbone Tabs

Dashboard (`dashboard.html`) renders a backbone tab bar above the experiment list. Default view shows "ALL".

### GitHub Pages Dashboard Sync (MANDATORY when published)

If the repo is published to GitHub Pages, the live dashboard MUST be synced from `autoresearch_results/dashboard.html` → `docs/dashboard/index.html` on every commit that changes experiment state. The dataset-local version is the source of truth; the Pages mirror is built by `framework/_sync_dashboard_to_docs.py`.

### Dashboard Files Update Mandate (MANDATORY — every experiment)

Every single experiment updates ALL the following files:

| File | Written by | When | Content |
|------|------------|------|---------|
| `autoresearch_results/experiment_log.jsonl` | runner (auto) | every run, appended | full metrics |
| `autoresearch_results/best_config.json` | runner (auto) | only when new GLOBAL champion | overwritten |
| `autoresearch_results/best_model.pkl` | runner (auto) | only when new GLOBAL champion | weights + scaler + config |
| `autoresearch_results/trade_logs/exp<N>_decisions.csv` | runner (auto) | every run | per-sample decision log |
| `autoresearch_results/trade_logs/exp<N>_decision_summary.json` | runner (auto) | every run | per-fold totals |
| `autoresearch_results/reasoning_annotations.json` | Claude BEFORE + runner AFTER | every run | diagnosis, citations, hypothesis, prediction (Claude); verdict, learning (runner fallback) |
| `autoresearch_results/research_journal.md` | Claude | every run | markdown narrative |
| `autoresearch_results/experiment_summary.md` | Claude | every run | short tabular entry |
| `memory/project_autoresearch_checkpoint.md` | Claude | every run | update champion + next command |
| `autoresearch_results/winners/<backbone>_exp<N>_<desc>/*` | Claude | only when new GLOBAL champion | full self-contained archive |

### Citation Rigor (MANDATORY format)

Every citation string MUST contain:
1. All authors' surnames
2. Year
3. Venue
4. Full paper title in single quotes
5. arXiv ID `(arXiv:XXXX.YYYYY)`
6. One-sentence relevance note

Format:
```
Author1, Author2, Author3 YEAR VENUE 'Paper Title' (arXiv:XXXX.XXXXX) — one-sentence note on why we cite it here.
```

Parenthetical-only tags (e.g., `(Keskar2017)`) are INSUFFICIENT — expand to full reference.

### Reasoning Blob Completeness

Each of the 7 fields in `reasoning_annotations.json` has a minimum content spec:

| Field | Minimum content | Word floor |
|-------|-----------------|------------|
| `diagnosis` | Why THIS experiment NOW; which champion weakness; which fold is worst | ≥ 60 words |
| `citations` | Per Citation Rigor spec | ≥ 40 words single paper, ≥ 80 multi |
| `hypothesis` | Config change stated mechanistically | ≥ 50 words |
| `prediction` | Concrete numeric range + sub-prediction | ≥ 25 words |
| `verdict` | KEEP/DISCARD/NEAR-MISS + composite + per-fold narrative | ≥ 30 words |
| `learning` | What this updates in the mental model | ≥ 40 words |
| `_manual` | Boolean | — |

### Heteroscedastic Loss Rules (Kendall & Gal 2017) — where applicable

For regression tasks, optionally output mean + log_variance per prediction:
- Loss = `exp(-s) * huber(mu, y) + 0.5 * s`
- Optimal aleatoric range: 0.05-0.15.
- Het-loss needs ~50% more epochs than plain Huber.

For classification tasks, use temperature scaling + ECE calibration instead.

### Winner Archiving Protocol

Every time a new champion is found, archive ALL artifacts to a self-contained subdirectory:

```
winners/
  <backbone>_exp<N>_<short_description>/
    README.md
    config.json
    model_checkpoint.pkl
    experiment_log_entry.json
    per_fold_results.json
    code/
    inference/
      predict.py
      README_inference.md
    reproduction/
      reproduce_log.txt
      seed_variance.json
    audit_report.md     (14 sections)
    colab_train_and_infer.ipynb
```

Reproduce the winner after archiving. If reproduction differs by >0.5% on `exact_match_accuracy`, flag and investigate.

### Google Colab Notebook (MANDATORY for every winner)

Self-contained Colab notebook at `winners/<...>/colab_train_and_infer.ipynb` with: setup, data, features, training, evaluation, inference, visualisation, export cells. Target runtime: <5 minutes on Colab free tier.

### Traditional ML Metrics (MANDATORY for every experiment)

In addition to the primary `exact_match_accuracy`, compute and log:
- For binary classification: precision, recall, F1, F2, MCC, accuracy, confusion matrix
- For multiclass: macro-F1, micro-F1, accuracy, per-class precision/recall, MCC
- For regression: RMSE, MAE, R², MAPE (where target > 0), Spearman ρ, Pearson r

These must appear in:
1. Runner output
2. Per-fold results in JSONL log entries
3. Dashboard per-fold tables
4. Winner archive `per_fold_results.json`
5. Experiment summary markdown

### Per-Sample Decision Logging (MANDATORY for every experiment)

For EVERY experiment, produce a per-sample decision spreadsheet on validation data:

**Output file:** `autoresearch_results/trade_logs/exp<N>_decisions.csv`

Columns: `sample_id, fold, prediction, predicted_class, actual, correct, confidence, score_contribution`.

Per-fold summary at `exp<N>_decision_summary.json`: totals, wins, losses, win-rate, confidence calibration.

This enables: identifying specific samples/folds where the model fails, confidence calibration analysis, error mode analysis.

### Architecture
- **Autoresearch loop = Claude agent.** Claude reads results, decides what to try, calls the runner, reads output.
- Runner (`run_autoresearch.py`) executes ONE experiment per call. Logs JSONL. That's it.
- Dashboard (`autoresearch_results/dashboard.html`) reads logs. DECOUPLED from runner.
- Save checkpoint after every experiment.
- Use relative imports.

### Validation Checklist (Run Before Every Experiment Session)
1. `data/split_manifest.json` hashes verified
2. Train/val/test counts match the manifest
3. Train-val overlap = 0, train-test overlap = 0, val-test overlap = 0
4. Data loaded from `.data_cache/` (not re-downloaded)
5. Test set is NOT used by any code path other than `framework/final_report.py`

## Project Structure

```
C:/Users/evija/dsbench/analysis/2013-round-2-data-analysis/                    # task root
  run_autoresearch.py             # runs ONE experiment (LOGS ONLY)
  hill_climb.py                   # outer 25-iters-per-backbone loop
  third_party_audit.py            # validator vs framework spec
  data/
    download.py                   # task-specific data fetcher
    features.py                   # task-specific features
    splits.py                     # train/val/test splits + manifest
    split_manifest.json
  memory/
    project_autoresearch_checkpoint.md
  code_versions/
    excel_agent_start/   # snapshot per backbone
  autoresearch_results/
    experiment_log.jsonl
    best_config.json
    dashboard.html
    experiment_summary.md
    research_journal.md
    reasoning_annotations.json
    trade_logs/
    winners/
```

## Key Constants

| Constant | Value | Location |
|----------|-------|----------|
| TASK_NAME | `2013-round-2-data-analysis` | this file |
| PROBLEM_TYPE | `qa_excel` | this file |
| TASK_TYPE | `financial_modeling_excel` | this file |
| PRIMARY_METRIC | `exact_match_accuracy` | this file |
| ITERATIONS_PER_BACKBONE | 25 | `framework/sota_catalog.yaml` |
| TRAIN_FRAC | 0.7 | `data/splits.py` |
| VAL_FRAC | 0.15 | `data/splits.py` |
| TEST_FRAC | 0.15 | `data/splits.py` |
| RANDOM_SEED | 42 | global |

## Common Mistakes (Never Repeat)

| Mistake | Consequence | Prevention |
|---------|-------------|------------|
| Test leakage during hill climbing | Inflated scores, dishonest comparison | Test split read ONLY by `framework/final_report.py` — runner has no path to it |
| Re-running same config without seed plan | Misleading "improvement" from variance | Multi-seed before declaring champion |
| Dead config params | Experiments with no effect | Wire every param end-to-end or remove |
| Data re-downloading every run | Wasted time | `.data_cache/` |
| Grid sweep instead of diagnostic | 10x more experiments | One change at a time |
| Absolute imports in package | `ModuleNotFoundError` | Always relative imports |
| Assuming timing/performance | Wrong estimates | Measure with `time.time()` |
| Monolithic scripts | Can't debug | Runners log. Dashboard reads. Decoupled. |
| Forgetting to checkpoint | Lost work | After every experiment |
| Skipping per-backbone snapshots | Mixed-up code history | `code_versions/<backbone>_start/` |
| Citing without arXiv ID | Useless | Look it up before writing |

## DSBench Comparison Target

The DSBench paper (ICLR 2025, Jing et al.) reports the best agent achieving 34.12% data-analysis success and 34.74% Relative Performance Gap on data-modeling. **Goal for `2013-round-2-data-analysis`: meet or beat the DSBench reported score on the test set.** The test set is touched ONCE, at the very end of the loop, by `framework/final_report.py`. The score is written to `autoresearch_results/final_report.json` along with the champion config and a comparison row to the DSBench baseline.

## Session Learnings

Append-only section. Document what each phase taught us so future backbones don't repeat dead ends.

(This section grows during the run — initial seed is in `seed_reasoning.json`.)
