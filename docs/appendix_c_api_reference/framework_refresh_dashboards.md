# API Reference — `framework._refresh_dashboards`

> The single-command dashboard refresh. Reads every per-task state; regenerates every dashboard + the cross-task rollup.

## Module: `framework._refresh_dashboards`

`C:/Users/evija/dsbench/framework/_refresh_dashboards.py`

## Purpose

After any per-task state change (experiment landed, audit run, champion changed) the dashboards must be regenerated to reflect the current state. This script is the *single-command end-to-end refresh* — Lessons-Learned row 21. Running it leaves every dashboard in a coherent state with respect to the on-disk rollup.

## What it produces

| Output | Built from |
|---|---|
| `registry/final_rollup.json` | Every `<task>/autoresearch_results/final_report.json` |
| `registry/forensic_summary.json` | Every `<task>/forensic_audit.json` |
| `dashboard/index.html` | The rollup files + the cross-task dashboard template |
| `dashboard/md_viewer.html` | Static; regenerated for cache-busting |
| `dashboard/task_detail.html` | Static; regenerated for cache-busting |
| Per-task `autoresearch_results/dashboard.html` × 112 | Each task's experiment log + annotations + audit |

## Public functions

### `refresh_all() -> None`

Walk every task; reload its on-disk state; regenerate its dashboard; aggregate into the rollup files; regenerate the cross-task dashboard.

### `refresh_task(slug: str) -> None`

Refresh only the named task's dashboard + update its row in the rollup files.

## CLI

```powershell
& "C:/Users/evija/anaconda3/python.exe" framework/_refresh_dashboards.py [--slug <slug>] [--force]
```

`--force` regenerates even unchanged tasks (useful after a dashboard template change).

## Idempotence

Running the script twice produces the same output (modulo timestamps in the dashboard footer). The script is the canonical "single command" for the SWE-book chapter 22 large-scale-change pattern.

## Wall-clock

~30 seconds for the full 112-task refresh on the reference hardware. Per-task `--slug` mode is ~200 ms.

## Failure modes

- **Missing `final_report.json` for a task.** The rollup row is written as `final_report: null`; the dashboard shows the task as `pending`.
- **Malformed `forensic_audit.json`.** The forensic summary row is `verdict: error` and the task is flagged in the cohort scoreboard.
- **Dashboard template syntax error.** Hard fail; the script exits non-zero. Caught early because the template change is itself a commit subject.

## Related

- [Ch. 18 — Build Systems](../part_4_tools/18_build_systems.md): the build pipeline this script is part of.
- [Ch. 22 — Large-Scale Changes](../part_4_tools/22_large_scale_changes.md): the LSC playbook that ends with this script.
- [Ch. 24 — Continuous Delivery](../part_4_tools/24_continuous_delivery.md): the dashboards as delivery artefacts.
- [`framework/_final_audit.py`](../../framework/_final_audit.py): the audit-gate aggregator that runs after this refresh.
