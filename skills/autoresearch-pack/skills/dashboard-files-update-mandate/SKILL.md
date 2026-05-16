---
name: dashboard-files-update-mandate
description: Dashboard files update mandate — every experiment updates JSONL, best_config, best_model, trade logs, reasoning_annotations, research_journal, experiment_summary, checkpoint, and (if champion) winner archive + audit + colab. Defines ownership per file (runner vs Claude) and the per-experiment ritual. Triggers on "dashboard files", "per-experiment ritual", "every file", "ownership table", "TODO-REWRITE", "_needs_rewrite".
metadata:
  category: dashboard
  source: autoresearch
  related: [dashboard-reasoning-annotations, github-pages-dashboard-sync, winner-archive-protocol, crash-recovery-checkpoint, mlops-documentation]
---

# Dashboard Files Update Mandate (every experiment)

## When to use

- After every experiment — before launching the next.
- Auditing whether the previous experiment is fully documented.
- Reviewing a PR that adds or removes a tracked artifact.

## The rule

> ### Dashboard Files Update Mandate (MANDATORY — every experiment, zero exceptions)
>
> **Every single experiment updates ALL the following files. If any file is stale after an experiment completes, that's a regression — stop and fix before moving on. No "I'll batch-update at the end." No "It's just a variance check."**
>
> **Ownership — who writes what:**
>
> | File | Written by | When | Content |
> |------|------------|------|---------|
> | `autoresearch_results/experiment_log.jsonl` | **runner (auto)** | every run, appended | full metrics: composite, test/val/train Sharpe, per-fold results, per-window classification metrics, uncertainty, timing, config |
> | `autoresearch_results/best_config.json` | **runner (auto)** | only when new GLOBAL champion | overwritten with full champion entry |
> | `autoresearch_results/best_model.pt` | **runner (auto)** | only when new GLOBAL champion | weights + scaler + config + feature_columns + provenance |
> | `autoresearch_results/trade_logs/exp<N>_trades.csv` | **runner (auto)** | every run | one row per test-day trade (date, fold, regime, prediction, direction, returns, confidence, aleatoric, epistemic, pnl_bps) |
> | `autoresearch_results/trade_logs/exp<N>_trade_summary.json` | **runner (auto)** | every run | per-fold totals, wins, losses, avg_win/loss bps, max win/loss, win_rate |
> | `autoresearch_results/reasoning_annotations.json` | **Claude BEFORE run + runner AFTER run** | every run, two-phase | diagnosis, citations, hypothesis, prediction (Claude); verdict, learning (runner fallback, Claude overrides) |
> | `autoresearch_results/research_journal.md` | **Claude** | every run, appended | markdown narrative of the full 7-step process (diagnosis → citations → hypothesis → prediction → verdict → learning) |
> | `autoresearch_results/experiment_summary.md` | **Claude** | every run, appended | short tabular entry per experiment (config delta, result, per-fold Sharpe, status, learning) |
> | `memory/project_autoresearch_checkpoint.md` | **Claude** | every run | update champion, update experiment history table, update next-command block |
> | `autoresearch_results/winners/<backbone>_exp<N>_<desc>/*` | **Claude** | only when new GLOBAL champion | README.md, config.json, model_checkpoint.pt (copy), code/ snapshot, inference/predict.py, per_fold_results.json, experiment_log_entry.json |
> | `autoresearch_results/winners/<backbone>_exp<N>_<desc>/audit_report.md` | **Claude** | only when new GLOBAL champion | 14-section audit per Explainability & Auditability Report spec |
> | `autoresearch_results/winners/<backbone>_exp<N>_<desc>/colab_train_and_infer.ipynb` | **Claude** | only when new GLOBAL champion | self-contained Colab notebook |
> | `autoresearch_results/dashboard.html` | **Claude (rarely)** | only when adding a new metric/tab | static HTML — reads the JSONL + annotations live |
>
> **Per-experiment ritual (repeat in order, every single run):**
>
> 1. **Before launch:** open `reasoning_annotations.json`, insert a new entry keyed by the upcoming `experiment_num` with `diagnosis`, `citations` (full reference), `hypothesis`, `prediction` (numeric target), `_manual: true`. If this entry isn't there, the experiment doesn't run.
> 2. **Before launch:** append a matching section to `research_journal.md` with the same 4 fields in markdown.
> 3. **Launch:** run the CLI command.
> 4. **Runner auto-updates:** JSONL, best_config (if champion), best_model (if champion), trade_logs CSV + JSON, reasoning_annotations verdict/learning fallback.
> 5. **After completion:** Claude reads the runner output, overwrites the `verdict` and `learning` fields in `reasoning_annotations.json` with richer analysis (per-fold narrative, which regimes won/lost, uncertainty profile). Updates the corresponding section in `research_journal.md`.
> 6. **After completion:** Claude appends a row to `experiment_summary.md`.
> 7. **After completion:** Claude updates `memory/project_autoresearch_checkpoint.md` with the new experiment in the history table, updated champion (if applicable), and the exact next-experiment command.
> 8. **If new champion:** Claude archives to `winners/<backbone>_exp<N>_<desc>/` — README, config copy, model copy, frozen code snapshot, inference predict.py, per-fold results, audit_report.md, Colab notebook. The archive must be self-contained.
>
> **Verification at the start of every experiment cycle:**
>
> Before launching Experiment N+1, confirm all of these are CURRENT for Experiment N:
>
> - [ ] `experiment_log.jsonl` has an entry for N (runner writes, verify)
> - [ ] `reasoning_annotations.json[N]` has all 7 fields non-empty and non-placeholder
> - [ ] `research_journal.md` has a section for N
> - [ ] `experiment_summary.md` has a row for N
> - [ ] `memory/project_autoresearch_checkpoint.md` references N in its history table
> - [ ] `trade_logs/expN_trades.csv` and `expN_trade_summary.json` exist
> - [ ] If N set a new champion: `winners/<backbone>_expN_<desc>/` exists with all required files
>
> If ANY checkbox is unchecked, stop and fix BEFORE launching N+1. This is how we keep the dashboard as authoritative, up-to-date institutional memory.
>
> **Placeholder strings are a bug.** The runner refuses to fabricate pre-run content. If a pre-run entry is missing, the runner inserts `"TODO-REWRITE"` sentinel values and a `_needs_rewrite: true` flag — Claude MUST rewrite those entries before launching the next experiment. Fix the process, not the string.

## Anti-patterns

- **Batch updates** at end of session. Each missed update breaks crash recovery.
- **"It's just a variance check"** — variance checks still need annotation, journal, summary, checkpoint updates.
- **Skipping the verification checklist** before Experiment N+1. The bug always hides where you didn't check.
- **Letting `TODO-REWRITE` sentinels survive.** They confess broken process; fix immediately.
- **Editing only the runner's auto-fields.** Claude's `verdict` + `learning` enrichment is the authoritative voice.

## Implementation checklist

1. Per-experiment ritual is encoded as an 8-step sequence (above) — follow every time.
2. Before launching Experiment N+1, run the 7-checkbox verification on Experiment N.
3. If a champion: trigger archive + audit + Colab generation in addition to standard updates.
4. Sync dashboard to `docs/` (see `github-pages-dashboard-sync`) before commit.
5. Runner's auto-output never lands a placeholder; if it can't compute, it emits `TODO-REWRITE` so Claude knows.

## References

- Source: `autoresearch/CLAUDE.md` section "Dashboard Files Update Mandate (MANDATORY — every experiment, zero exceptions)"
- Related: `dashboard-reasoning-annotations`, `github-pages-dashboard-sync`, `winner-archive-protocol`, `crash-recovery-checkpoint`, `mlops-documentation`.
