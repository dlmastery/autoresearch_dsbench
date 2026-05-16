---
name: session-startup
description: On Session Start ritual for an autoresearch loop — read checkpoint, hardware-crash log, experiment log tail, best_config, start the dashboard, resume the 7-step loop from the checkpoint. Triggers on "session start", "resume", "continue", "keep going", "on session start".
metadata:
  category: protocol
  source: autoresearch
  related: [crash-recovery-checkpoint, hardware-pinning, seven-step-research-process]
---

# Session Startup

## When to use

- A fresh Claude Code session opens an autoresearch repo and must pick up where the last session left off.
- The user says "continue", "keep going", "resume" — no further instructions needed.
- A laptop just rebooted after a BSOD and the loop must be re-armed.

## The rule

> You ARE the autoresearch loop. Claude Code is the outer loop — there is no separate Python agent. When a session starts:
>
> 1. **Read the crash-recovery checkpoint:** `memory/project_autoresearch_checkpoint.md` — it has the current champion, last experiment result, per-fold diagnostics, and what to try next.
> 2. **Read the hardware crash log:** `memory/project_hardware_crash_log.md` — documents BSOD history and CPU core exclusion rules. Must follow.
> 3. **Read the experiment log tail:** `autoresearch_results/experiment_log.jsonl` (last 3 entries) and `autoresearch_results/best_config.json` to verify state.
> 4. **Resume the experiment loop** from where the checkpoint says. Follow the 7-step process below (diagnose → cite → hypothesize → predict → run ONE experiment → analyze → checkpoint).
> 5. **Start the dashboard** (once per session, background): `"<python-path>" -m http.server 8765 --directory <project>/autoresearch_results` — then tell the user: "Dashboard at http://localhost:8765/dashboard.html"
> 6. **Run experiments** via the project's `run_autoresearch` entry-point (timeout 600s).
> 7. **If the user says "continue" or "keep going"** — resume the loop. No need to ask what to do.

## Anti-patterns

- **Re-reading every file in the repo on session start.** The checkpoint is the entry point — trust it. Reading source files before the checkpoint wastes context and risks re-deriving stale conclusions.
- **Asking "what would you like me to do?" after the user said "continue".** The checkpoint specifies the next experiment command verbatim — just run it.
- **Starting two dashboard servers.** Always check whether port 8765 is in use before re-launching.
- **Skipping the hardware crash log read.** Hardware constraints are non-negotiable — running on E-cores will BSOD the machine.
- **Resuming on an empty checkpoint.** If `memory/project_autoresearch_checkpoint.md` is missing or stub-only, STOP and seed it from `experiment_log.jsonl` + `best_config.json` before running any new experiment.

## Implementation checklist

1. `Read memory/project_autoresearch_checkpoint.md` — extract champion, next command, rationale.
2. `Read memory/project_hardware_crash_log.md` — apply core exclusion rules.
3. `Read autoresearch_results/experiment_log.jsonl` tail (last 3 lines) — verify the runner agrees with the checkpoint's champion.
4. `Read autoresearch_results/best_config.json` — cross-check composite score.
5. Start dashboard once in background (suppress port-collision noise).
6. Inform user of dashboard URL.
7. Re-run the `seven-step-research-process` starting at Step 1 (diagnose).

## References

- Source: `autoresearch/CLAUDE.md` section "On Session Start (ALWAYS do this first)"
- Source: `autoresearchindexspy/autoresearchspy/CLAUDE.md` section "On Session Start (ALWAYS do this first)"
- Related skills: `crash-recovery-checkpoint`, `hardware-pinning`, `seven-step-research-process`, `dashboard-files-update-mandate`.
