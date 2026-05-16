---
name: parallel-agent-orchestration
description: Parallel-agent orchestration — when autoresearch work splits cleanly (e.g. 112 tasks × 5 backbones × 25 iters), launch parallel background agents and coordinate via the file system. Each agent writes to disjoint paths; the main agent reads completion signals (a `<path>/_done.json` or a registry row update). Triggers on "parallel agents", "background agent", "file-system rendezvous", "disjoint output paths", "fan-out / fan-in", "agent orchestration".
metadata:
  category: protocol
  source: dsbench
  related: [crash-recovery-checkpoint, architecture-separation-of-concerns, mlops-documentation, committee-resumption-pointers]
---

# Parallel-Agent Orchestration (file-system rendezvous)

## When to use

- The autoresearch workload trivially partitions (e.g. one agent per task slug; one agent per backbone).
- A single foreground session would take days; parallel agents finish in hours.
- The main agent's role is "coordinator + auditor", not "executor".
- A long-running improvement loop needs to make progress while the foreground does interactive work (e.g. the user adds a correction; the foreground commits a checkpoint; the background keeps running).

## The rule

> **When work splits cleanly into N disjoint slices, launch N parallel background agents and coordinate via the file system.** Each agent writes to a unique path (`autoresearch_results/<task>/`, `submissions/<kind>/<slug>/`, etc.); the main agent monitors completion by polling the file system for `_done.json` markers or by re-reading the central registry. No agent-to-agent communication is required — the file system is the rendezvous.

### The pattern

1. **Partition.** The work is a flat list of independent units (tasks, backbones, sub-period audits). No two units write to the same output path.
2. **Spawn.** Launch each unit as a background Bash / PowerShell process with `run_in_background=true`. Each process invokes the same entry point with a different `--task <slug>` (or equivalent) argument.
3. **Disjoint outputs.** Each agent writes to `autoresearch_results/<unit>/...`. The path is the implicit lock — no two agents touch the same files.
4. **Completion signal.** Each agent writes `<unit_root>/_done.json` (or `_done.txt`) as its last action. The main agent polls for these files to determine fan-in.
5. **Registry update.** Each agent appends one row to a central JSONL or atomically updates a per-task JSON file under `registry/`. The main agent re-reads the registry to get the rollup.
6. **Foreground coordinator.** The main session checkpoints to git periodically, runs the validator / forensic / audit pack, and tells the user when fan-in completes.
7. **Crash recovery.** A background agent crashed mid-run is restartable from its own checkpoint (`memory/project_autoresearch_checkpoint.md` per task). The orchestrator doesn't need to know the unit failed — the missing `_done.json` is the signal.

### Concrete DSBench example

```
foreground session:
  - kicks off 6 background agents (one per task batch of ~19 tasks)
  - each agent runs: python framework/run_all.py --kind modeling --batch 1
  - each writes to autoresearch_results/<slug>/... + registry/forensic_summary.json (append-only)
  - foreground polls registry every 5 min; runs _status.py; commits checkpoints

background agents (×6):
  - read their batch slice from registry/task_list.json
  - run hill-climb on each task in slice
  - write _done.json to their batch_root when slice complete
  - update registry/forensic_summary.json (atomic per-task replace)
```

### Why file-system rendezvous

- **No shared mutable state.** Agents can't race on a queue or a lock.
- **Crash-tolerant.** A crashed agent leaves a partial output; restarting picks up where it left off (per `crash-recovery-checkpoint`).
- **Audit-friendly.** Every agent's outputs are inspectable post-hoc; nothing lives only in RAM.
- **Visible.** The orchestrator and the user can both `ls` the output tree to see progress.

## Anti-patterns

- **Shared mutable file** (single `experiment_log.jsonl` with concurrent appends from N agents) — append races corrupt the file. One log per agent; merge offline.
- **Implicit locking via OS** (`flock` on Linux, `LockFileEx` on Windows) — works but obscures the contract. Disjoint paths are explicit.
- **Centralised queue / message bus** for a workload this static — over-engineered. The file system is the queue.
- **Foreground that blocks on a single background agent** — defeats the parallelism. The orchestrator should be non-blocking and audit-driven.
- **No `_done.json` markers** — the orchestrator can't tell "agent X is still working" from "agent X crashed silently". Always emit a completion sentinel.
- **Background agents that modify each other's output paths** — even read-only access is risky if the other agent re-writes mid-read.

## Implementation checklist

1. The workload is partitioned in a registry file (`registry/task_list.json`) with a `batch` or `agent_id` column.
2. Each agent's entry point takes a `--batch` / `--task` flag and only touches paths under that scope.
3. Output paths are flat under `autoresearch_results/<unit>/...` — never nested by agent.
4. Each agent emits `<unit_root>/_done.json` with timestamp + final score on completion.
5. The orchestrator polls every N minutes via `framework/_status.py` (which reads the registry, not the agents).
6. Git checkpoints from the foreground commit only foreground-owned files; background-owned files are committed by a separate "fan-in" commit after all `_done.json` markers exist.
7. Each agent has its own `memory/project_autoresearch_checkpoint.md` so a restart finds the right resume point.

## References

- DSBench session log (2026-05) — the 112-task sweep ran as 6 parallel background agents coordinating via `registry/forensic_summary.json`.
- Hyndman & Athanasopoulos 2021 'Forecasting: Principles and Practice' (3e) — the partition-then-merge cross-validation pattern is the conceptual ancestor.
- Andrew Ng's "Machine Learning Yearning" (2018) — chapter on parallel iteration emphasises the file-system rendezvous.
- Related: `crash-recovery-checkpoint`, `architecture-separation-of-concerns`, `mlops-documentation`, `committee-resumption-pointers`.
