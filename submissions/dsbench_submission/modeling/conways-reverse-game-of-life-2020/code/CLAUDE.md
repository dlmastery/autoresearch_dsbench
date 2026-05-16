# CLAUDE.md — Project Rules for AutoResearch on `conways-reverse-game-of-life-2020`

> Generated from the master `autoresearch/CLAUDE.md` (4/20/2026). Every section
> below is a 1-to-1 clone of the source, with `conways-reverse-game-of-life-2020` / `structured`
> / `modeling` / `accuracy` parameters substituted. Section coverage is
> verified by `framework/validator.py` against `framework/SECTION_MAPPING.md`.

## Champion summary (auto-populated from `registry/final_rollup.json` + `registry/forensic_summary.json`)

> **🏆 Project state — read this FIRST on session start (committee resumption pointer).**
>
> - **Beat DSBench:** <count>/<total> (<percent>%)
> - **Forensic PASS:** <count>/<total>
> - **Champion of champions:** <task_slug> · <backbone> · composite <value>
> - **Resume in one command:** `& "C:/Users/evija/anaconda3/python.exe" framework/_status.py`
> - **Cross-task dashboard:** http://localhost:8765/dashboard/index.html
>
> Placeholder fields are LITERAL — they are deliberately not auto-substituted in
> this template so the file never lies about state it hasn't measured. A future
> enhancement (a pre-commit hook in `framework/_substitute_champion_summary.py`)
> will read `registry/final_rollup.json` + `registry/forensic_summary.json` and
> rewrite the literals into actual counts during the regenerate-CLAUDE step. Until
> that hook ships, run `framework/_status.py` to see live numbers. See skill
> `committee-resumption-pointers` for the pattern and `single-command-refresh` for
> the surrounding ritual.

## On Session Start (ALWAYS do this first)

You ARE the autoresearch loop. Claude Code is the outer loop — there is no separate Python agent. When a session starts:

1. **Read the crash-recovery checkpoint:** `memory/project_autoresearch_checkpoint.md` — it has the current champion, last experiment result, per-fold diagnostics, and what to try next.
2. **Read the experiment log tail:** `autoresearch_results/experiment_log.jsonl` (last 3 entries) and `autoresearch_results/best_config.json` to verify state.
3. **Read the seed reasoning:** `seed_reasoning.json` for the first-experiment plan tied to task `conways-reverse-game-of-life-2020` (structured, structured).
4. **Resume the experiment loop** from where the checkpoint says. Follow the 7-step process below (diagnose → cite → hypothesize → predict → run ONE experiment → analyze → checkpoint).
5. **Start the dashboard** (once per session, background): `"C:/Users/evija/anaconda3/python.exe" -m http.server 8765 --directory C:/Users/evija/dsbench/modeling/conways-reverse-game-of-life-2020/autoresearch_results` — then tell the user: "Dashboard at http://localhost:8765/dashboard.html".
6. **Run experiments** via: `cd C:/Users/evija/dsbench/modeling/conways-reverse-game-of-life-2020 && "C:/Users/evija/anaconda3/python.exe" run_autoresearch.py --backbone <backbone> [flags] --description "..."` (timeout 600s). Backbone order for `structured`: mlp → ft_transformer → xgboost.
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
- Current champion config + composite score on `accuracy`
- Per-fold validation score table for the champion (TRAIN/VAL ONLY — test set is held back for the final DSBench comparison report)
- Last experiment result (config, composite, per-fold delta vs champion, KEEP/DISCARD)
- The EXACT next experiment command to run (copy-pasteable PowerShell)
- Rationale for next experiment (diagnosis + literature cite + hypothesis)
- All wired parameters and their CLI flags
- Key learnings from exhausted axes
- Full experiment history summary

The checkpoint must be self-contained. A fresh Claude Code session reading ONLY `CLAUDE.md` + the checkpoint must be able to resume without reading any other file.

## Mindset

You are a top-tier ML researcher — multiple best-paper awards at NeurIPS/ICML/AAAI, industry expert in structured on structured data. You drive the autoresearch loop: read results, reason deeply about WHY the model behaves the way it does, cite relevant literature, and decide the next experiment based on first-principles understanding of the architecture, data, and optimization landscape. Never guess. Never grid-search. Before touching any code:

1. **Understand the data flow end-to-end.** Trace how a single training sample is created.
2. **Validate before running.** Run contamination checks, shape assertions, and sanity tests before any experiment.
3. **Measure, never assume.** If you state a number (timing, sample count, performance), it must come from running code — not estimation.
4. **When fixing a bug, audit the entire system for the same class of bug.**
5. **Separation of concerns is not optional.** Runners log. Dashboards display. Evaluators evaluate. Never tangle them.

## Auditing & Forensics (project guardrails — read this BEFORE writing code)

The autoresearch protocol is policed by **four layers of automated audit**. A
session that runs an experiment without these layers passing is not a valid
run; the work doesn't count.

### Layer 1 — Section-coverage validator (`framework/validator.py`)

Reads `framework/SECTION_MAPPING.md` and verifies every required section
header exists in the task's `CLAUDE.md`. Also greps `run_autoresearch.py` and
`hill_climb.py` for `X_test` / `y_test` references and FAILS if found (test
leakage = blocking error). Required file list: `task_config.json`,
`seed_reasoning.json`, `paper.md`, `paper_abstract.md`, `README.md`,
`autoresearch_results/dashboard.html`, plus the markdown artefacts. Run on
every repo via:

```powershell
& "C:/Users/evija/anaconda3/python.exe" framework/validator.py
```

Target: **112/112 ok**. If <112, fix the failing task; do not proceed.

### Layer 2 — Ten-agent forensic-audit committee (`framework/forensic_audit.py`)

Per-task pipeline runs 10 independent agents, each with a single concern:

| Agent | Concern | Threshold |
|---|---|---|
| **A** — split-hash | manifest hashes match actual `.npz` split | mismatches ≥ 1 → FAIL |
| **B** — target / label leakage | per-feature mutual information vs label | max MI > 0.9 → FAIL on tabular; calibrated for `qa_excel` task-onehot |
| **C** — row-overlap | train/val/test row hashes intersection | total overlap > 0 → FAIL |
| **D** — distribution shift | per-feature KS train vs test | > 10% flagged features → FAIL on tabular; calibrated for `qa_excel` stride split |
| **E** — anomaly | val > train + 0.05; perfect 1.0 scores; big jumps > 0.3 | susp count > 0 → FAIL; sklearn early-stop + regression is whitelisted (Bishop 2006 §5.5.2) |
| **F** — static-code | grep for `X_test` / `y_test` in runner / hill_climb | any reference → FAIL |
| **G** — temporal order | no future timestamps in train rows | N/A on synthetic data |
| **H** — seed-stability | multi-seed champion reproduction variance | record-only |
| **I** — refit-consistency | refit champion from `best_config.json`, score on test, compare to recorded | |delta| > 0.005 → FAIL |
| **J** — backbone-diversity | distinct backbones in `experiment_log.jsonl` | < 3 → WARN (not FAIL) |
| **Z** — committee verdict | aggregates A-J → PASS / FAIL with risks list | — |

Outputs `<repo>/forensic_audit.md` (full narrative) +
`<repo>/forensic_audit.json` (machine-readable) +
`registry/forensic_summary.json` (one row per task). Run via:

```powershell
& "C:/Users/evija/anaconda3/python.exe" framework/forensic_audit.py
```

Target: **112/112 PASS**.

### Layer 3 — 14-section explainability audit (per-task winner archive)

When a new GLOBAL champion is found, `framework/build_submission.py` writes
`submissions/dsbench_submission/<kind>/<slug>/audit_report.md` with all 14
sections from the autoresearch CLAUDE.md "Explainability & Auditability
Report" rule (executive summary; feature importance; top-N features;
SHAP-style explanations; per-fold feature drift; calibration; uncertainty;
prediction distribution; trade attribution; risk audit; data pipeline audit;
config dump; known limitations; deployment checklist). Skipping any section
of the 14 is a regression — re-run the builder.

### Layer 4 — Skill-pack coverage audit (`skills/autoresearch-pack/audit/audit_pack.py`)

Verifies every H2/H3 in `autoresearch/CLAUDE.md` AND
`autoresearchindexspy/autoresearchspy/CLAUDE.md` AND
`framework/CLAUDE_template.md` maps to ≥ 1 SKILL.md. Coverage target: **100%
(currently 156/156)**. Run via:

```powershell
& "C:/Users/evija/anaconda3/python.exe" skills/autoresearch-pack/audit/audit_pack.py
```

### Cross-cutting tooling

- `framework/_status.py` — canonical scoreboard: BEAT-DSBENCH / FORENSIC-PASS / FORENSIC-FAIL by kind and total.
- `framework/_final_audit.py` — end-to-end audit (combines all 4 layers + checks dashboards have "About this task" + viewer URLs work + Lessons-Learned section present in every CLAUDE.md).
- The 4 layers + 2 tools = the "is this submittable to a top-tier conference" checkpoint. Run all four before any commit that changes experiment state.

### Submission-archive contract (`submissions/dsbench_submission/<kind>/<slug>/`)

A self-contained, portable archive PER TASK that lets a committee reviewer
spot-check without setting up the repo. Required contents:

- `README.md` — task summary + champion + DSBench delta
- `config.json` — exact champion config (backbone + params + metrics)
- `final_report.json` — one-shot test-set score
- `runner_up.json` — 2nd-best experiment (variance baseline)
- `audit_report.md` — 14-section explainability audit
- `forensic_audit.md` + `forensic_audit.json` — 10-agent committee report
- `research_journal.md` — per-experiment 6-field reasoning narrative
- `experiment_summary.md` — tabular per-experiment summary
- `experiment_log.jsonl` — append-only raw log
- `reasoning_annotations.json` — machine-readable per-experiment reasoning
- `code/CLAUDE.md` + frozen task-config + paper + seed_reasoning
- `inference/predict.py` — standalone inference script
- `reproduction/reproduce_log.txt` — runnable repro command + expected composite

Built / refreshed by `framework/build_submission.py` after every experiment
batch that updates a champion.

## Hard Rules (NEVER violate)

### Data Integrity
- NEVER allow the test set to influence any decision during hill climbing. The DSBench test split for `conways-reverse-game-of-life-2020` is held in `data/test/` and is OFF-LIMITS until the final report run.
- **No experiment writes to or reads from `splits['X_test']` / `splits['y_test']`.** Only `framework/final_report.py` touches the test set — ONCE per task at the very end. Every runner / hill-climb / extended-hill-climb code path uses train + val only. This invariant is enforced by `framework/validator.py` (greps for `X_test` / `y_test` in `run_autoresearch.py` and `hill_climb.py` and FAILS the audit if found).
- ALL hill-climbing decisions use TRAIN + VALIDATION ONLY (`data/train/`, `data/val/`).
- ALWAYS cache downloaded data. `data/download.py` writes to `.data_cache/`. NEVER re-download mid-run.
- Load data ONCE at startup. Compute features ONCE. Split ONCE. Reuse across all experiments in a loop.

### QA-Excel Task Data Loading (real Modeloff answers — NOT synthetic placeholders)

For `qa_excel` tasks, `framework/runner.py::load_or_make_data()` loads REAL Modeloff multiple-choice answers from `_analysis_data.json` and `registry/analysis_tasks.json`, NOT synthetic features. The feature stack is:

1. **9-D structural feature stack** per question (length, # numeric tokens, # alphabetic tokens, has-decimal flag, has-percent flag, has-currency flag, n-options, question-tier, source-document-tier).
2. **38-task one-hot indicator** (one column per Modeloff task in the analysis registry).

The `_excel_agent` backbone supports five interchangeable predictors selectable via the `backend` param: `logistic_regression`, `knn`, `naive_bayes`, `class_prior` (prior-only baseline), `dummy_majority`. Tunable knobs:

- `prior_weight ∈ [0, 1]` — convex blend of the per-task class-prior with the model logits.
- `knn_k ∈ {1, 3, 5, 7, ...}` — used only when `backend=knn`.
- `temperature ∈ (0, 5]` — softens / sharpens the model logits before argmax.

This means QA tasks legitimately have prior-only champions whose val > train (prior is computed across all training answers; per-task val happens to lie closer to the prior than train does). See skill `qa-task-feature-engineering` and the `regression-early-stopping-discipline` skill for the corresponding sklearn-MLP rule.

### Cross-Task Pooling Discipline (training only — evaluation is per-task)

QA training POOLS answers across ALL 38 Modeloff tasks: a single LogReg / KNN / NaiveBayes is fit on the union of every task's train split. **Each task is then scored per-task** on its own held-out val / test rows. Cross-task pooling is allowed for **TRAINING**; per-task split is mandatory for **EVALUATION**. This protocol is what lets a single 9-D + 38-onehot model handle all 38 tasks; it's also why the task-onehot features have mechanical mutual information with the label (the model legitimately learns "task X's prior is mostly answer B"). See skill `cross-task-pooling-discipline`.

### Small-n Stride-5 Interleaved Split (QA tasks only)

For tiny multiple-choice tasks (n = 5..20 questions per challenge), a contiguous-block 70/15/15 split puts all "easy" early questions in train and all "hard" late questions in test, violating the exchangeability assumption (Bishop 2006 PRML §1.3). The DSBench QA loader uses a **stride-5 interleaved split** instead:

```
indices 0, 1, 2, 5, 6, 7, 10, 11, 12, ...  → train
indices 3, 8, 13, 18, ...                  → val
indices 4, 9, 14, 19, ...                  → test
```

This gives every position-bucket equal representation in train / val / test and breaks the difficulty-ordering correlation. Tabular tasks with n ≥ 100 still use the standard 70/15/15 random split. See skill `small-n-stride-split`.

### Split Invariants
- Train/val/test split is **frozen at task creation time** and recorded in `data/split_manifest.json`. Hashes of each split file are verified at every runner start; any change is a fatal error.
- Cross-validation folds inside the train set are deterministic (seed=42).
- **Zero overlap** between train, val, and test — verified programmatically before every run.

### Experiment Design
- **Composite metric for KEEP/REVERT:** `min(val_score, train_score) - 0.05 * abs(val_score - train_score)` on `accuracy` (higher is better; for loss-style metrics like RMSE, we negate). Train/val gap is penalised so overfit champions are rejected.
- **Metric sign convention (NEVER violate):** `framework/runner.py::_score()` returns a **higher-is-better** scalar for EVERY metric — RMSE / MAE / log-loss are negated INSIDE `_score()`. Therefore every downstream regression / delta / "beats DSBench" computation uses the same arithmetic for every metric:
  ```python
  delta = test_score - dsb_baseline      # correct for ALL metrics
  # NEVER: delta = -1 * (test_score - dsb_baseline) for RMSE
  ```
  Special-casing the sign for loss-style metrics is the bug that motivated the 2026-05 hot-fix in `framework/final_report.py`. See skill `metric-sign-convention`.
- Training is EPOCH-BOUND (minimum 20 epochs with early stopping). NOT time-bound.
- **30-second cooldown after each experiment** to let the GPU/CPU cool.
- ONE config change per experiment. Diagnose WHY before choosing what to change next.
- Report per-fold breakdown for BOTH val and train alongside aggregates.
- Dashboard shows train/val tabs for per-fold breakdown. Val is the default view.
- Every config parameter must be wired end-to-end. Dead params are bugs — remove them.
- Every hyperparameter choice must be justified by published papers, model developer guidelines, or prior empirical results from this project.

### Extended Hill-Climb Phase (200-iter recovery cycle)

For any task that finishes the base 25-iter × 5-backbone phase (125 experiments) STILL losing to the DSBench baseline, `framework/extended_hill_climb.py` runs a 200-iter recovery cycle. The extension:

- Dispatches every proposal through the existing 5 runner backbones (xgboost, lightgbm, catboost, mlp, ft_transformer) — proposals targeting families the runner doesn't natively implement (NGBoost, TabNet, TabPFN, PatchTSMixer) hit the closest implementation with the appropriate regularisation lever.
- Probes 15 backbone-families with arXiv-cited reasoning per experiment — deeper xgboost, leaf-wise lightgbm-GOSS, ordered catboost, residual MLP, large FT-Transformer, HGB, ExtraTrees, RandomForest, ElasticNet stack, plus stack-ensemble dispatchers.
- Logs to the SAME `experiment_log.jsonl` (appends iters 126..325), so the existing dashboard / reasoning-annotations / winner-archive machinery covers it without modification.
- Key citations: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754); Ke et al. 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' (arXiv:1711.05101); Friedman 2001 AoS 'Greedy Function Approximation: A Gradient Boosting Machine'; Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101).

See skill `extended-hill-climb-phase` for the full 200-iter proposal taxonomy.

### Autoresearch Agent Protocol (Karpathy-adapted)
1. **Always start from the current best config.** Every experiment modifies ONE thing from the best. If it improves, it becomes the new best. If it doesn't, revert.
2. **If you see consecutive discards, stop and rethink.** Multiple failures mean your hypothesis about what to change is wrong.
3. **Explore around the best AND try radical changes.** Most experiments should be small tweaks around the champion. But occasionally try something bold to escape local optima.
4. **Cite your reasoning for every experiment.** "I'm trying X because fold Y has weak accuracy due to Z, and paper W suggests this fix."
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

**Canonical status-snapshot script — `framework/_status.py`.** This is the ONE-COMMAND tool for "how is the run going?" — it reads `registry/final_rollup.json` + `registry/forensic_summary.json` and prints the BEAT-DSBENCH / FORENSIC-PASS / FORENSIC-FAIL counts for modeling vs analysis. Invoke with `"C:/Users/evija/anaconda3/python.exe" framework/_status.py`. The script is the canonical artefact — every new project MUST ship the equivalent so a fresh session can read project health in one command.

**Status-counting asymmetry — KIND vs PROBLEM_TYPE.** The two rollup files disagree on the modeling/analysis distinction key:

- `final_rollup.json` rows do **NOT** carry a `kind` field. The modeling-vs-analysis distinction is `problem_type != "qa_excel"` → modeling; `problem_type == "qa_excel"` → analysis.
- `forensic_summary.json` rows DO carry a `kind` field (`modeling` or `analysis`).

Code reading both files MUST account for this asymmetry — see `framework/_status.py` for the canonical pattern (`is_mod(r) = r.get('problem_type') != 'qa_excel'` for rollup rows; `f.get('kind') == 'modeling'` for forensic rows). Mixing the two keys silently miscounts task health.

`autoresearch_results/experiment_summary.md` — the master experiment log, updated after EVERY experiment.

```markdown
## Experiment Log — [Backbone] Phase

### Exp[N]: [description]
- **Config delta from champion:** [what changed]
- **Rationale:** [diagnosis + literature citation + hypothesis]
- **Prediction:** [expected composite change]
- **Result:** Composite [X] | Val accuracy [Y] | Train accuracy [Z] | [N]/K positive folds
- **Per-fold val:** F1=[X] F2=[X] F3=[X] F4=[X] F5=[X]
- **Status:** KEEP / DISCARD
- **Learning:** [what was learned, why result matched/differed from prediction]
```

### Forensic Audit — Problem-Type-Aware Thresholds & Agents I/J

The forensic audit pipeline (`framework/forensic_audit.py`) runs 10 agents over every champion. Two additional rules beyond the base 8-agent pattern:

- **Agent I — Refit-consistency:** every champion MUST reproduce within ±0.005 on the test set when refit from `best_config.json:params`. A drift > 0.005 indicates non-deterministic training, a config-param not wired end-to-end, or a stale model checkpoint. FAIL blocks deployment.
- **Agent J — Backbone diversity:** every task SHOULD have ≥ 3 distinct backbones tried (counted from `experiment_log.jsonl`). Fewer than 3 = WARN. The rule prevents declaring a champion before the SOTA backbone surface has been meaningfully explored.

**Problem-type-aware thresholds (qa_excel only)** — agents B (target leakage), D (distribution shift), E (anomaly) MUST use calibrated thresholds for `qa_excel`:

- **Agent B (target leakage)** — task-onehot features have mechanical mutual information with the label (each task has a different per-task prior). Raise the MI threshold to MI > 0.50 nats (vs. 0.05 for tabular).
- **Agent D (distribution shift)** — the stride-5 interleaved split is mechanically KS-different at small-n (different positional buckets in each split). Replace the KS-test with a chi-square on the label distribution; warn only when chi-square p < 0.001.
- **Agent E (anomaly val > train)** — for QA, a prior-only / class-prior classifier legitimately has val > train when the per-task val set happens to be closer to the global prior than the per-task train set. Suppress the anomaly when `backend ∈ {class_prior, dummy_majority}` OR when the model is a sklearn `MLPRegressor(early_stopping=True)` AND the gap is ≤ 0.05 (val > train + 0.05 is normal under early-stopping — Bishop 2006 PRML §5.5.2).

See skill `problem-type-aware-audit-thresholds` and `regression-early-stopping-discipline`.

### Sklearn Early-Stopping Val > Train Is Normal (Bishop 2006 §5.5.2)

For regression + sklearn `MLPRegressor(early_stopping=True)`, **val > train + 0.05 is NORMAL, not leakage.** sklearn's early-stopping reserves an internal validation slice (default 10% of the training data) to choose the stopping epoch; the reported `train_score` is computed on the *remaining* 90% of training data while the model was selected to minimise loss on the held-out slice — so the slice is, in effect, a second training signal. The post-fit train-score therefore underestimates the true train performance. Any forensic audit that flags `val > train` as leakage MUST first check `model_type == sklearn MLPRegressor with early_stopping=True` and suppress the warning. See skill `regression-early-stopping-discipline`.

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
| `prediction` | Numeric target: "accuracy should move from current to approx target". | Authored before running |
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

Refer to `framework/sota_catalog.yaml` — full table mirroring autoresearch's Tier-1, Tier-2 (foundation models), and Tier-3 (GBM) hierarchy. For `structured`/`structured`, the active backbones are: mlp → ft_transformer → xgboost.

### GPU Memory Constraint (MANDATORY — 16 GB VRAM hard cap)

- Model parameters ≤ 3 GB (FP32) / 1.5 GB (BF16)
- Optimizer state (AdamW) ≤ 6 GB
- Gradients ≤ 3 GB
- Activations ≤ 3 GB
- Reserved / fragmentation ≥ 1 GB

Pre-flight check required in the reasoning annotation for Experiment 1 of any new backbone. Without this entry, Experiment 1 does not launch.

### Dashboard Backbone Tabs

Dashboard (`dashboard.html`) renders a backbone tab bar above the experiment list. Default view shows "ALL".

### Interactive Dashboard Navigation Rules

The cross-task and per-task dashboards follow strict navigation conventions:

- **Cross-task → per-task:** clicking a row in the cross-task dashboard (`dashboard/index.html` cross-task table) opens the per-task dashboard in a **new browser tab** (not a modal, not a new window, not in-place navigation). Implementation: `<a href="…" target="_blank" rel="noopener">`.
- **Per-task experiment row click:** opens an **inline detail panel** within the same dashboard (not a new tab). Implementation: vanilla-JS click handler that toggles a `<div class="detail-drawer">` sibling beneath the row.
- **Markdown artefacts (`summary.md`, `journal.md`, `paper.md`, `CLAUDE.md`, `forensic_audit.md`, `checkpoint.md`):** every link MUST route through the in-browser markdown viewer `dashboard/md_viewer.html?path=<relative>`, NOT directly to the `.md` file (Chromium-family browsers download `.md` files instead of rendering them). The viewer reads the path from the query string, fetches the markdown, and renders it client-side via marked.js / CommonMark.
- **Task description disclosure:** every per-task dashboard MUST have a collapsible "About this task" `<details>` block near the top containing: source URL, full task metadata table, backbones explored, problem-type description, DSBench baseline + delta, link to `CLAUDE.md` (via md_viewer), link to the autoresearch skill pack. See skill `task-description-disclosure`.
- **Train / val / test exposure:** per-task dashboard SHOWS train AND val metrics per-experiment in the detail panel. Test metrics ONLY render for the global champion experiment, sourced from `autoresearch_results/final_report.json` — because the test set is touched ONCE per autoresearch protocol.

See skill `interactive-dashboard-design` for the full UI taxonomy and `task-description-disclosure` for the about-block schema.

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

Every time a new champion is found, archive ALL artifacts to a self-contained subdirectory.

**Champion refit rule (final_report.py):**

- For `problem_type == "qa_excel"`: `framework/final_report.py` refits the champion on `train + val` (NOT just train) before scoring the test set. Reason: per-task train is only ~6-10 questions, so adding val (~2-3 more) is the difference between a usable estimator and a degenerate one. Val gating is already finished by the time `final_report.py` runs, so val cannot leak into the test decision.
- For tabular tasks (`problem_type != "qa_excel"`): refit on train only, exactly as during hill climbing — preserves the held-out-val invariant that the explainability and forensic audits depend on.

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

Reproduce the winner after archiving. If reproduction differs by >0.5% on `accuracy`, flag and investigate.

### Google Colab Notebook (MANDATORY for every winner)

Self-contained Colab notebook at `winners/<...>/colab_train_and_infer.ipynb` with: setup, data, features, training, evaluation, inference, visualisation, export cells. Target runtime: <5 minutes on Colab free tier.

### Traditional ML Metrics (MANDATORY for every experiment)

In addition to the primary `accuracy`, compute and log:
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
5. Test set is NOT used by any code path other than `framework/final_report.py` — VERIFIED by `framework/validator.py` (greps for `X_test` / `y_test` in `run_autoresearch.py` and `hill_climb.py`)
6. Run `framework/_status.py` and confirm the BEAT-DSBENCH / FORENSIC-PASS counts match the previous session checkpoint — drift means an experiment ran outside the protocol

## Project Structure

```
C:/Users/evija/dsbench/modeling/conways-reverse-game-of-life-2020/                    # task root
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
    mlp_start/   # snapshot per backbone
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
| TASK_NAME | `conways-reverse-game-of-life-2020` | this file |
| PROBLEM_TYPE | `structured` | this file |
| TASK_TYPE | `structured` | this file |
| PRIMARY_METRIC | `accuracy` | this file |
| ITERATIONS_PER_BACKBONE | 25 | `framework/sota_catalog.yaml` |
| TRAIN_FRAC | 0.7 | `data/splits.py` |
| VAL_FRAC | 0.15 | `data/splits.py` |
| TEST_FRAC | 0.15 | `data/splits.py` |
| RANDOM_SEED | 42 | global |

## Portability Patterns (cross-benchmark — DSBench + DARE-bench)

The autoresearch protocol is designed to transplant cleanly from one benchmark
to another. Four patterns generalise the dsbench-specific rules so the same
framework runs unmodified against benchmarks with different held-back surfaces,
different parallelisation needs, or different propagation rituals.

### Forbidden-Path Access Audit (forensic agent K)

A static-code grep that fails the forensic audit if any runner / hill-climb
file references the held-back surface declared in `task_config.json`. Default
token set targets `data/test/` (DSBench); inversion mode targets `data/train/`
(DARE-bench eval-only). The accessor (the ONE file allowed to touch the
held-back surface, e.g. `framework/final_report.py` for DSBench or
`framework/final_eval.py` for DARE-bench) is exempt. Wire as the FIRST agent
in the committee — a positive grep aborts downstream agents. See skill
`forbidden-path-audit`.

### Held-Back-Surface Discipline (DARE-bench inversion-aware)

Generalises the DSBench rule "test set is OFF-LIMITS until final_report" to
any benchmark whose held-back surface is named differently. Every
`task_config.json` declares `held_back_surface`, `held_back_tokens`,
`final_accessor`, `final_artefact`. The same protocol applies in inversion
mode: in DARE-bench the held-back surface is `data/train/`, the accessor is
`framework/final_eval.py`, and the search loop has no path to either. See
skill `held-back-surface-discipline`.

### Parallel-Agent Orchestration (file-system rendezvous)

When the workload splits cleanly (e.g. 112 tasks × 5 backbones × 25 iters),
launch N parallel background agents and coordinate via the file system. Each
agent writes to disjoint paths (`autoresearch_results/<unit>/`); each emits a
`_done.json` sentinel on completion; the foreground coordinator polls the
registry. No shared mutable state, no centralised queue — the file system IS
the queue. See skill `parallel-agent-orchestration`.

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

The DSBench paper (ICLR 2025, Jing et al.) reports the best agent achieving 34.12% data-analysis success and 34.74% Relative Performance Gap on data-modeling. **Goal for `conways-reverse-game-of-life-2020`: meet or beat the DSBench reported score on the test set.** The test set is touched ONCE, at the very end of the loop, by `framework/final_report.py`. The score is written to `autoresearch_results/final_report.json` along with the champion config and a comparison row to the DSBench baseline.

## Session Learnings

Append-only section. Document what each phase taught us so future backbones don't repeat dead ends.

(This section grows during the run — initial seed is in `seed_reasoning.json`.)

## Lessons Learned (append-only — every user correction lands here)

This is the master "next-time-you-do-this-don't-miss-this" checklist. Every correction the user makes during a project becomes a permanent row here AND lands in the autoresearch skill pack. Order is chronological; never reorder, never delete.

| # | Correction | Skill mapping |
|---|------------|---------------|
| 1 | **Regression delta sign rule.** `_score()` returns higher-is-better for ALL metrics (RMSE / MAE are negated inside). Therefore `delta = test_score - dsb_baseline` works for every metric — no special-case sign flip. Bug fix in `framework/final_report.py` (2026-05). | `metric-sign-convention` (NEW) + Hard Rules → Experiment Design |
| 2 | **Extended hill-climb phase.** `framework/extended_hill_climb.py` runs 200 iters on top of the base 125 for any task that loses to baseline, dispatching 15 backbone-families through the existing runner with arXiv citations per iter. Friedman 2001 / Chen & Guestrin 2016 / Loshchilov & Hutter 2019. | `extended-hill-climb-phase` (NEW) + Hard Rules → Experiment Design |
| 3 | **Forensic audit problem-type awareness.** For `qa_excel`, agents B (target leakage), D (distribution shift), E (anomaly) need calibrated thresholds because task-onehot features have mechanical MI with label, stride-5 split has mechanical KS shift, and prior-only classifiers legitimately have val > train. | `problem-type-aware-audit-thresholds` (NEW) + `forensic-audit-pipeline` (EXTENDED) |
| 4 | **Sklearn early-stopping val > train is normal.** Per Bishop 2006 PRML §5.5.2, sklearn `MLPRegressor(early_stopping=True)` reserves an internal validation slice — post-fit `train_score` underestimates true train. Suppress the leakage warning when this combo holds and gap ≤ 0.05. | `regression-early-stopping-discipline` (NEW) + `forensic-audit-pipeline` (EXTENDED) |
| 5 | **Real QA-data loading.** `_excel_agent` is no longer a synthetic-feature placeholder. Loads real Modeloff answers from `_analysis_data.json`. Builds a 9-D structural feature stack + 38-task one-hot, with backends `logistic_regression / knn / naive_bayes / class_prior / dummy_majority` and knobs `prior_weight / knn_k / temperature`. | `qa-task-feature-engineering` (NEW) + Hard Rules → Data Integrity |
| 6 | **QA-task refit on train+val.** For `qa_excel`, `framework/final_report.py` refits the champion on train + val (NOT just train) because per-task train is only ~6-10 questions. Tabular tasks still refit on train only. | `winner-archive-protocol` (EXTENDED) |
| 7 | **Interleaved stride-5 split for QA tasks.** Tiny multiple-choice tasks (n=5..20) use stride-5 interleave so every position-bucket is equally represented in train/val/test. Bishop 2006 PRML §1.3 (exchangeability). | `small-n-stride-split` (NEW) + Hard Rules → Data Integrity |
| 8 | **Cross-task pooling rule.** QA training pools answers across ALL 38 tasks (training subsets only); each task is scored per-task on its held-out test. Pooling for TRAINING; per-task for EVALUATION. | `cross-task-pooling-discipline` (NEW) + Hard Rules → Data Integrity |
| 9 | **New-tab navigation rule.** Cross-task row click → per-task dashboard in a new tab. Per-task experiment row click → inline detail panel within the same dashboard. | `interactive-dashboard-design` (EXTENDED) |
| 10 | **Markdown inline render.** All `.md` artefact links route through `dashboard/md_viewer.html?path=…`, NOT directly to the `.md` file (browsers download `.md`). | `interactive-dashboard-design` (EXTENDED) |
| 11 | **Task description dropdown.** Every per-task dashboard has a collapsible "About this task" block near the top with source URL, metadata, backbones, problem-type description, DSBench baseline, link to CLAUDE.md, link to skill pack. | `task-description-disclosure` (NEW) |
| 12 | **Train/val/test exposure.** Per-task dashboard shows train AND val metrics per-experiment in the detail panel. Test metrics ONLY for the champion experiment, sourced from `final_report.json`. | `train-val-test-invariants` (EXTENDED) + `interactive-dashboard-design` |
| 13 | **Test set held back until final_report.** No experiment writes to or reads from `splits['X_test']` / `splits['y_test']`. Only `framework/final_report.py` touches test, ONCE per task. Validator enforces by grep. | `data-integrity-rules` + Validation Checklist (REINFORCED) |
| 14 | **Status counting by problem_type, not kind.** `final_rollup.json` rows don't carry `kind`; the modeling/analysis distinction is `problem_type != "qa_excel"`. `forensic_summary.json` rows DO carry `kind`. Don't mix the keys. | `mlops-documentation` (EXTENDED) |
| 15 | **Status snapshot script.** `framework/_status.py` is the canonical "how do I see how things are going" tool — one command prints BEAT-DSBENCH / FORENSIC-PASS / FORENSIC-FAIL counts. | `mlops-documentation` (EXTENDED) |
| 16 | **Refit-consistency audit (agent I).** Every champion MUST reproduce within ±0.005 on the test set when refit from `best_config.json:params`. FAIL blocks deployment. | `forensic-audit-pipeline` (EXTENDED) |
| 17 | **Backbone-diversity audit (agent J).** Every task SHOULD have ≥ 3 distinct backbones tried (counted from `experiment_log.jsonl`). Fewer than 3 = WARN. | `forensic-audit-pipeline` (EXTENDED) |
| 18 | **Composite metric definition is non-negotiable.** `composite = min(val_score, train_score) - 0.05 * |val_score - train_score|`. The first term forces both train AND val to be good; the second term penalises overfit. Used for KEEP/DISCARD on every experiment. Implemented in `framework/runner.py:run_one`. | `experiment-design` (EXTENDED) |
| 19 | **Submission archive per task is MANDATORY.** `framework/build_submission.py` writes `submissions/dsbench_submission/<kind>/<slug>/` with README + config + final_report + runner_up + 14-section audit + 10-agent forensic + research journal + experiment log + reasoning annotations + code snapshot + inference + reproduction recipe. Refresh after every commit that updates a champion. | `winner-archive-protocol` (EXTENDED) |
| 20 | **Expert-data-scientist diagnosis BEFORE coding the fix.** When user reports failures (e.g. "analysis tasks scoring 0%"), ship a rigorous diagnosis report first — read the actual data, compute coverage statistics, document the ceiling, then commit code. Pattern: `analysis/_DIAGNOSIS.md` (1950 words) + `analysis/_COVERAGE.md`. Conference-quality framing. | `seven-step-research-process` (EXTENDED) — diagnose-before-code |
| 21 | **Background-agent + git-checkpoint cadence.** Long-running improvement work runs as a background agent; the foreground commits a checkpoint to `dlmastery/autoresearch_dsbench` (Windows note: `git config http.sslBackend schannel` for SSL cert). `.gitignore` excludes `.data_cache/` (synthetic / regenerable), `__pycache__/`, stdout logs. Commit message follows autoresearch convention: subject ≤ 70 chars + bullet body + Co-Authored-By trailer. | `mlops-documentation` (EXTENDED) |
| 22 | **Four-layer audit gate before any submission claim.** Layer 1 = section-coverage validator (`framework/validator.py`); Layer 2 = 10-agent forensic committee (`framework/forensic_audit.py`); Layer 3 = 14-section explainability per winner (`framework/build_submission.py`); Layer 4 = skill-pack coverage audit (`skills/autoresearch-pack/audit/audit_pack.py`). All four must pass. Aggregate via `framework/_final_audit.py`. | `forensic-audit-pipeline` (EXTENDED) + new top-level "Auditing & Forensics" section |
| 23 | **Sklearn early-stopping whitelist is backbone-AND-problem-type aware.** Agent E whitelists `(mlp \| ft_transformer \| lstm \| patchtsmixer \| lightgbm)` × `regression` because all five use validation-based early stopping (sklearn `MLPRegressor(early_stopping=True)`, LightGBM `early_stopping_rounds`). Classification + early-stop is NOT whitelisted (different failure modes). | `regression-early-stopping-discipline` (EXTENDED) |
| 24 | **GitHub checkpoint protocol.** First commit goes to `dlmastery/autoresearch_dsbench`. Push exclusively via `gh repo create … --source .` + `git push -u origin main`. SSL backend: schannel on Windows (`git config --global http.sslBackend schannel`). Repo is ~156 MB after exclusions (24K+ files); push takes ~2-5 min initial, fast for follow-ups. | `mlops-documentation` (EXTENDED) |
| 25 | **Two-tab dashboard navigation.** Cross-task leaderboard row click → per-task autoresearch dashboard in a NEW TAB (not modal, not new window). Per-task experiment row click → INLINE detail panel within the same dashboard. `target="_blank"` for cross-task; same-page DOM mutation for per-task. | `interactive-dashboard-design` (EXTENDED) |
| 26 | **Live dashboard auto-refresh.** Cross-task leaderboard and per-task dashboards auto-refresh every 30s via `setInterval(load, 30000)` so a long-running background agent's progress is visible without manual reload. | `interactive-dashboard-design` (EXTENDED) |
| 27 | **Three-stream feature engineering as task-specific innovation template.** From `autoresearchindexspy`, the daily / pre-market / hourly causal-anchor pattern. The DARE-bench mandate "task-specific innovative backbones" maps onto this — every new task category gets its own causally-anchored multi-stream derivation. Anchor cutoff is non-negotiable: train at the latest causal anchor, never at a post-prediction anchor. | `three-stream-feature-engineering` |
| 28 | **Stacked ensemble design (val-weighted N-component).** N independently-tuned champions, softmax-weighted by per-component val composite, averaged at test time. SPY demo: 12 components, +0.277 composite. Weights computed on val ONLY; test held-out. Lakshminarayanan et al. 2017 NeurIPS (arXiv:1612.01474). | `stacked-ensemble-design` |
| 29 | **Regime gate as defensive filter.** Conditional rule (`rvol60d > 15%` for SPY) that gates trading to the model's edge regime. Defensive — doesn't generate alpha in off-regime, just avoids losses. Threshold chosen on val only. Ang & Bekaert 2002 RFS. | `regime-gate` |
| 30 | **Sub-period robustness audit.** Rolling-window evaluation across pre-registered sub-periods (5-year blocks, regime quartiles) to expose regime-specialist behaviour. Headline: `min_subperiod_sharpe / max_subperiod_sharpe`. Concentrated edge → gate; regime-flip → retrain or retire. Bailey & López de Prado 2014. | `sub-period-robustness-audit` |
| 31 | **Champion summary block at top of CLAUDE.md.** Committee resumption pointer — beat-count, forensic-pass count, champion of champions, resume command, dashboard URL. Auto-populated from `registry/final_rollup.json` + `registry/forensic_summary.json` (placeholders kept literal in the template; a future pre-commit hook will substitute). | `committee-resumption-pointers` |
| 32 | **Forbidden-path access audit (forensic agent K).** Static-code grep that fails the audit if any runner references the held-back surface. Parameterised by `task_config.json:held_back_tokens`; DSBench grep targets `X_test`/`y_test`/`data/test/`; DARE-bench inversion targets `X_train`/`y_train`/`data/train/`. The single declared accessor is exempt. Agent K runs FIRST in the committee. | `forbidden-path-audit` (NEW) |
| 33 | **Held-back-surface discipline (eval-only mandate / DARE-bench inversion).** The autoresearch loop's `data/test/`-is-forbidden rule generalises to `data/<held-back-surface>/`-is-forbidden. Each `task_config.json` declares the surface, tokens, single accessor, and frozen output artefact. DSBench: test held back, `final_report.py` is accessor. DARE-bench: train held back, `final_eval.py` is accessor. One declared accessor, one frozen artefact, one final touch. | `held-back-surface-discipline` (NEW) + `data-integrity-rules` (EXTENDED) |
| 34 | **Parallel-agent orchestration via file-system rendezvous.** When work splits cleanly (112 tasks × 5 backbones × 25 iters), launch N parallel background agents; each writes to disjoint paths and emits a `_done.json` sentinel; the foreground coordinator polls the registry. No shared mutable state, no centralised queue — file system is the queue. Each agent has its own crash-recovery checkpoint. | `parallel-agent-orchestration` (NEW) |
| 35 | **Single-command end-to-end refresh (9-step ritual).** After any correction: regenerate task CLAUDE.md (step 2) → re-run affected experiments (3) → refresh 4 audit layers (4a-d) → rebuild submissions (5) → refresh dashboards (6) → status snapshot (7) → final audit (8) → commit + push (9). Doc-only corrections can skip steps 3 and 4a. The ritual is the contract between "user added a correction" and "everything propagated correctly". | `single-command-refresh` (NEW) + `mlops-documentation` |

When a new correction lands, add a row here AND update the corresponding skill (or create a new one) AND re-run `skills/autoresearch-pack/audit/audit_pack.py` to confirm coverage holds at 100%. **Then** regenerate every per-task `CLAUDE.md` via `framework/_regenerate_claude_only.py` so the new rule reaches all 112 task repos. **Then** commit + push to `dlmastery/autoresearch_dsbench`.

## Single-command end-to-end refresh

Whenever the user adds a correction:

```powershell
# 1. apply the code change(s) implied by the correction
# 2. regenerate all 112 task CLAUDE.md from the updated template
& "C:/Users/evija/anaconda3/python.exe" framework/_regenerate_claude_only.py
# 3. re-run every experiment loop that's affected (use --kind to scope)
& "C:/Users/evija/anaconda3/python.exe" framework/run_all.py --kind analysis
# 4. refresh the four audit layers
& "C:/Users/evija/anaconda3/python.exe" framework/final_report.py
& "C:/Users/evija/anaconda3/python.exe" framework/forensic_audit.py
& "C:/Users/evija/anaconda3/python.exe" framework/validator.py
& "C:/Users/evija/anaconda3/python.exe" skills/autoresearch-pack/audit/audit_pack.py
# 5. rebuild the submission archive
& "C:/Users/evija/anaconda3/python.exe" framework/build_submission.py
# 6. refresh the per-task dashboards
& "C:/Users/evija/anaconda3/python.exe" framework/_refresh_dashboards.py
# 7. status snapshot
& "C:/Users/evija/anaconda3/python.exe" framework/_status.py
# 8. final cross-check audit
& "C:/Users/evija/anaconda3/python.exe" framework/_final_audit.py
# 9. commit + push
git add -A
git commit -m "<correction summary>"
git push origin main
```

This nine-step ritual is the entire "user added a correction, propagate it" loop.
