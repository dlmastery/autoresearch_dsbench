---
name: crash-recovery-checkpoint
description: Crash-recovery checkpointing rules — write a self-contained checkpoint after every experiment and every 5 minutes of reasoning. Triggers on "checkpoint", "crash recovery", "BSOD", "resume", "memory/project_autoresearch_checkpoint.md".
metadata:
  category: protocol
  source: autoresearch
  related: [session-startup, dashboard-files-update-mandate, committee-resumption-pointers]
---

# Crash-Recovery Checkpointing

## When to use

- After every experiment completes.
- Whenever you have been reasoning/analysing for ~3+ minutes without saving.
- Before starting any code change, and after any code change.
- Before launching the next experiment (the checkpoint must contain the next bash command, paste-ready).

## The rule

> **Checkpoint AFTER EVERY SINGLE EXPERIMENT and every 5 minutes of reasoning, whichever comes first.** This is the #1 non-negotiable rule. The laptop WILL crash. Every minute of uncheckpointed work is lost work.
>
> **Checkpoint trigger points (ALL mandatory):**
> 1. **Immediately after every experiment completes** — before any analysis or reasoning about results
> 2. **Every 5 minutes during reasoning/analysis** — if you've been thinking for 3+ minutes without saving, STOP and checkpoint
> 3. **Before starting any code change** — save current state so crash during edit doesn't lose experiment context
> 4. **After any code change** — save the new code state and what was changed
> 5. **Before starting the next experiment** — checkpoint must contain the exact bash command ready to paste
>
> What to save to `memory/project_autoresearch_checkpoint.md`:
> - Current champion config + composite score
> - Per-fold test Sharpe table for the champion
> - Last experiment result (config, composite, per-fold deltas vs champion, KEEP/DISCARD)
> - The EXACT next experiment command to run (copy-pasteable bash)
> - Rationale for next experiment (diagnosis + literature cite + hypothesis)
> - All wired parameters and their CLI flags
> - Key learnings from exhausted axes (so we don't re-try them)
> - Session start instructions (numbered steps)
> - **Full experiment history summary** — every experiment number, config delta, result, KEEP/DISCARD
>
> Also update `autoresearch_results/experiment_summary.md` with the all-experiments table.
>
> **During long reasoning/analysis (no experiment running):** still checkpoint every 5 minutes. Save your current thinking, diagnosis, and plan to the checkpoint file. If you've been reasoning for 3+ minutes without saving, STOP and checkpoint before continuing.
>
> **The checkpoint must be self-contained.** A fresh Claude Code session reading ONLY `CLAUDE.md` + the checkpoint must be able to resume without reading any other file. Include the bash command, the rationale, and enough per-fold context to make the next decision. A new session should be able to pick up EXACTLY where the previous one left off — same experiment number, same champion, same next-experiment rationale.

### Checkpoint + packaging cadence (append-only addition)

> - After **every** experiment: update `memory/project_autoresearch_checkpoint.md` AND `autoresearch_results/experiment_summary.md`.
> - After **every** session end or user-requested package: zip `autoresearch_results/` + `memory/` + `code_versions/` + frozen `model/` + `data/` + `evaluation/` + `run_autoresearch.py` + `CLAUDE.md`. Exclude `.data_cache/` (large, reproducible), `__pycache__/`, `.git/`.

## Anti-patterns

- **"I'll batch-checkpoint at the end of the session."** The session ends with a BSOD; everything between now and then is lost.
- **Sketchy one-line checkpoints** ("Exp24: failed, trying Exp25"). A new session cannot resume — it doesn't know what Exp25's command is, what changed, or why.
- **Checkpoint that points to other files for context** ("see research_journal.md"). The checkpoint must be self-contained — a fresh session reads ONLY `CLAUDE.md` + checkpoint.
- **Skipping the "next bash command" line.** Without the exact command, the next session has to re-derive it from logs, doubling time-to-experiment.
- **Updating the checkpoint AFTER editing code.** Save BEFORE the edit — if the edit BSODs the machine, you've lost the diagnosis context that motivated the edit.

## Implementation checklist

1. Confirm `memory/project_autoresearch_checkpoint.md` exists at session start.
2. After each experiment write/update these blocks IN ORDER:
   - **Current champion** (backbone, composite, per-fold Sharpe, file path of model_checkpoint.pt).
   - **Last experiment** (number, config delta, composite, KEEP/DISCARD, per-fold deltas).
   - **Next experiment** (full bash command paste-ready, diagnosis, citations, hypothesis, prediction).
   - **Experiment history table** (one row per experiment).
   - **Exhausted axes** (what NOT to retry).
3. Save the file. Do not proceed to the next experiment until saved.
4. On every code edit, repeat the checkpoint write BEFORE and AFTER the edit.

## References

- Source: `autoresearch/CLAUDE.md` section "Crash-Recovery Checkpointing (MANDATORY — laptop crashes constantly)"
- Source: `autoresearch/CLAUDE.md` section "Checkpoint + packaging cadence"
- Source: `autoresearchindexspy/autoresearchspy/CLAUDE.md` section "Crash-Recovery Checkpointing (MANDATORY — laptop crashes constantly)"
- Related: `session-startup`, `dashboard-files-update-mandate`, `committee-resumption-pointers`.
