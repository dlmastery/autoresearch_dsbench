# Chapter 16 — Version Control and Branches

> *Parallel to:* SWE-book Chapter 16 *"Version Control and Branch Management"* (Winters, Manshreck, Wright 2020).

**Thesis.** Version control is the project's memory of every state it has ever been in. The SWE-book chapter 16 argues for a single trunk, frequent commits, and minimal branching. The DSBench project is a single trunk (`main` on <https://github.com/dlmastery/autoresearch_dsbench>), no feature branches, and the **Checkpoint-After-Every-Experiment Rule**: the next experiment's exact PowerShell command must be in the crash-recovery checkpoint *before* the previous experiment's results are read.

## 16.1 Trunk-based development

The project has one branch: `main`. There are no feature branches. There are no release branches. There are no environment branches. There are tags for cohort runs (`v2026-05-15-cohort`) but tags are not branches.

The rationale matches the SWE-book chapter 16: a single trunk means a single source of truth. With a single operator and an LLM collaborator that has no memory, multiple branches would multiply the state space the collaborator has to reason about. One branch = one state.

The discipline:

- Commits land directly on `main`.
- Each commit passes the four-layer audit gate before push (informal; single operator).
- Commits are *small enough to revert* (no commit changes > 2,000 lines outside of scaffold regeneration).
- Scaffold regeneration commits are *separate* from logic-change commits.

The two-commit pattern for a framework change:

1. **Logic commit.** Change `framework/runner.py` or `framework/forensic_audit.py`. Add SKILL.md if applicable. Add ADR if structural. Add Lessons-Learned row if a correction.
2. **Regeneration commit.** Run `framework/_regenerate_claude_only.py` to refresh all 112 per-task `CLAUDE.md` files. Commit the regenerated files.

Splitting the two commits means the human can `git revert <regeneration commit>` if the regeneration introduces a problem, without losing the logic change.

## 16.2 The Checkpoint-After-Every-Experiment Rule

The crash-recovery checkpoint is the project's most-aggressively-updated artefact. The rule:

> Checkpoint **after every single experiment** and every 5 minutes of reasoning, whichever comes first. The next experiment's exact PowerShell command must be in the checkpoint *before* the previous experiment's results are read.

What goes into `memory/project_autoresearch_checkpoint.md`:

1. Current champion config + composite score on the task's metric.
2. Per-fold validation score table for the champion (TRAIN / VAL only — Test-Set Embargo).
3. Last experiment result (config, composite, per-fold delta vs champion, KEEP / DISCARD).
4. The EXACT next experiment command to run (copy-pasteable PowerShell).
5. Rationale for the next experiment (diagnosis + literature citation + hypothesis).
6. All wired parameters and their CLI flags.
7. Key learnings from exhausted axes.
8. Full experiment history summary.

Triggers (all mandatory):

1. Immediately after every experiment completes.
2. Every 5 minutes during reasoning.
3. Before starting any code change.
4. After any code change.
5. Before starting the next experiment — the checkpoint must contain the exact command, ready to paste.

The rule's purpose: the LLM collaborator's session can die at any time (BSOD on E-core thread misuse, Windows update reboot, accidental Ctrl-C). The checkpoint must let a fresh Claude session resume by reading only `CLAUDE.md` + the checkpoint, with no access to any other file.

## 16.3 The hardware-forced checkpoint discipline

A specific source of crashes that makes the checkpoint rule non-negotiable: WHEA-Logger reports internal parity errors on CPU APIC IDs 16, 17, 24, 25 — all E-cores — on the reference 14th-gen HX laptop. Sustained compute on E-cores BSODs the machine within ~3 minutes. The runner pins to P-cores 0, 2, 4, 6 via `_pin_to_safe_cores()`, but the safety margin is thin.

The checkpoint discipline means: even if the machine BSODs mid-experiment, the only lost work is the experiment that was running. The checkpoint already names what to do next. Resumption is a single PowerShell paste away.

This pattern — making the recovery procedure a *first-class artefact* — is the SWE-book chapter 16 recommendation for version control: optimise for resumption, not for theoretical correctness of an ongoing process. The checkpoint is the equivalent of the SWE-book's stash-style "save your work and walk away" pattern, pushed to its strongest form.

## 16.4 schannel SSL and the GitHub push

A specific operational issue: the reference machine runs Windows-native `git`, which uses the `schannel` SSL backend by default. `schannel` does not respect the system CA bundle the same way OpenSSL does, and a fresh Windows install often fails to push to <https://github.com/...> with `unable to access ... SSL certificate problem: unable to get local issuer certificate`. The fix:

```powershell
git config --global http.sslBackend openssl
git config --global http.sslCAInfo "C:/Program Files/Git/mingw64/ssl/certs/ca-bundle.crt"
```

The issue and the fix are documented in [postmortem 0005](../appendix_a_postmortems/0005_git_push_ssl_cert_failure.md). The fix is a one-time global config change, not a per-repo config change.

## 16.5 Commit messages

The convention is the SWE-book chapter 16 standard: subject ≤ 70 chars, body explains why. Examples from the actual commit log:

> `CLAUDE.md: add Auditing & Forensics section + 9 new corrections (18-26)`
>
> Adds the four-layer audit gate to the template; 9 new Lessons-Learned rows
> that cover (18) composite sign convention, (19) skill-pack coverage gate,
> (20) X_test grep enforcement, (21) single-command refresh, (22) parallel-agent
> orchestration tradeoff, (23) two-tab navigation, (24) MD viewer inline render,
> (25) forbidden-path audit, (26) status-counting asymmetry.

> `Initial checkpoint: DSBench autoresearch — 82/112 beat, 112/112 forensic PASS`
>
> First public commit. 112-task cohort. 25-iter base + 200-iter extended.
> Forensic committee 10 agents. 14-section explainability per champion.
> 44-skill autoresearch-pack with 148/148 coverage.

The two examples illustrate the project's commit style: the subject names the change, the body names the rationale and the rules it codifies.

## 16.6 The `.gitignore` contract

The `.gitignore` excludes:

- `_appendix_rows.json`, `_extract_*.py`, `_reset_*.py`, `_diagnose.py` at the repo root — these are scratch scripts.
- `.data_cache/` per task — large, regenerable.
- `__pycache__/` everywhere.
- `*.pyc` everywhere.
- IDE folders (`.idea/`, `.vscode/` are not currently ignored but easy to add).

What is *not* ignored:

- `experiment_log.jsonl` per task. The ledger is part of the truth.
- `reasoning_annotations.json` per task. The rationale is part of the truth.
- `final_report.json` per task. The test-set result is part of the truth.
- `forensic_audit.{md,json}` per task. The audit record is part of the truth.
- `submissions/dsbench_submission/<kind>/<slug>/` — the per-task submission archive.
- `dashboard/index.html` and per-task `autoresearch_results/dashboard.html`. The presentation layer is part of the truth.

The principle: anything the audit gate reads is committed; anything that's a downstream computation of those is regeneratable and may or may not be committed.

## 16.7 Tags vs branches

The project uses tags, not branches, for cohort runs:

- `v2026-05-15-cohort` — first 82/112 BEAT cohort.

Tags are lightweight (no force-push concerns) and serve the SWE-book's "version pinning" purpose. A reviewer can `git checkout v2026-05-15-cohort` to see exactly the state that produced the 82/112 number.

No release branches. The project does not have a release process in the SWE-book sense — every commit on `main` is "released" in that the cohort scoreboard updates from it.

## 16.8 What we do not version control

Three artefacts are deliberately excluded from version control:

1. **Raw Kaggle CSVs.** Licensed by Kaggle; not redistributable.
2. **Raw Modeloff PDFs.** Licensed by Modeloff; not redistributable. The `_analysis_data.json` we derive from them *is* redistributable as parsed data.
3. **Local Anaconda installation.** `C:/Users/evija/anaconda3/` is not part of the repo. The reproducibility contract is "install Python 3.11, install numpy / sklearn / xgboost / lightgbm / catboost / torch, point `python.exe` at the runner". A `requirements.txt` would be helpful future work.

## 16.9 The "single push" cadence

A cohort run produces dozens of file changes (every per-task `experiment_log.jsonl`, every `best_config.json`, every dashboard, the rollup files). The cadence is: run the cohort, run `_final_audit.py`, commit, push, *once*. We do not commit mid-cohort; the audit gate would not be green mid-cohort.

This is the SWE-book chapter 16 pattern: commits should be coherent units of work. A mid-cohort commit would not be coherent (some tasks done, some not, scoreboard half-baked).

## 16.10 Related

- [Ch. 23 — Continuous Integration](23_continuous_integration.md): the audit gate that runs before every push.
- [Ch. 24 — Continuous Delivery](24_continuous_delivery.md): the submission-archive build that runs before the push.
- [Postmortem 0005](../appendix_a_postmortems/0005_git_push_ssl_cert_failure.md): the schannel fix.
- [ADR 0014](../appendix_b_adrs/0014_github_checkpoint_protocol.md): the checkpoint protocol.
