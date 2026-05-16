# API Reference — `framework.generate_scaffolds`

> The scaffold generator. Reads the registry, instantiates per-task repos from the template, runs the validator.

## Module: `framework.generate_scaffolds`

`C:/Users/evija/dsbench/framework/generate_scaffolds.py`

## Purpose

Generates one self-contained per-task directory for each row in `registry/modeling_tasks.json` (74 tasks) and `registry/analysis_tasks.json` (38 tasks). Each generated directory is a thin wrapper around `framework/`.

## What each per-task scaffold contains

| File / directory | Source | Purpose |
|---|---|---|
| `CLAUDE.md` | Rendered from `framework/CLAUDE_template.md` | Task-parameterised protocol document. |
| `task_config.json` | Generated from registry row | Frozen task identity (slug, kind, problem_type, metric, backbones, baseline). |
| `seed_reasoning.json` | Generated | First-experiment plan tied to the task. |
| `data/splits.py` | Generated | Per-task data loader (calls `framework.runner.load_or_make_data`). |
| `data/.data_cache/` | Created at first run by runner | Cache for `splits.npz`. |
| `data/split_manifest.json` | Created at first run by runner | Hash-pinned manifest. |
| `autoresearch_results/dashboard.html` | Rendered from `framework/dashboard_template.html` | Per-task dashboard. |
| `autoresearch_results/experiment_log.jsonl` | Empty stub | Populated by the runner. |
| `autoresearch_results/best_config.json` | Empty stub | Populated by the runner. |
| `autoresearch_results/reasoning_annotations.json` | Empty `{}` | Populated by Claude. |
| `autoresearch_results/trade_logs/` | Empty directory | Populated per experiment. |
| `autoresearch_results/winners/` | Empty directory | Per-champion archive. |
| `autoresearch_results/research_journal.md` | Empty stub | Populated per experiment. |
| `autoresearch_results/experiment_summary.md` | Empty stub | Populated per experiment. |
| `memory/project_autoresearch_checkpoint.md` | Generated stub | Initialised; updated after every experiment. |
| `run_autoresearch.py` | Generated | Thin wrapper around `framework.runner.run_one`. |
| `hill_climb.py` | Generated | Thin wrapper around `framework.hill_climb.run`. |
| `third_party_audit.py` | Generated | Thin wrapper around the validator. |
| `code_versions/<backbone>_start/` | Created on first run per backbone | Snapshot of the backbone's code before its 25-iter phase. |
| `README.md`, `paper.md`, `paper_abstract.md` | Generated stubs | Task references. |

## Public functions

### `generate_one(task_row: dict) -> Path`

Generate one task scaffold from a registry row. Returns the scaffold directory.

### `generate_all() -> list[Path]`

Iterate over both registry files; generate every task; run the validator at the end.

## CLI

```powershell
& "C:/Users/evija/anaconda3/python.exe" framework/generate_scaffolds.py [--kind modeling|analysis] [--slug <slug>]
```

Without flags, regenerates all 112 scaffolds.

## Wall-clock

~30 seconds for the full 112-task regeneration. Re-runs are idempotent (existing per-task `experiment_log.jsonl`, `reasoning_annotations.json`, `best_config.json` are preserved; only the templated files are overwritten).

## Related

- [Ch. 8 — Style Guides and Rules](../part_3_processes/08_style_guides_and_rules.md): the template the scaffold is rendered from.
- [Ch. 22 — Large-Scale Changes](../part_4_tools/22_large_scale_changes.md): the LSC playbook that uses this script.
- [`framework/CLAUDE_template.md`](../../framework/CLAUDE_template.md): the template.
- [`framework/SECTION_MAPPING.md`](../../framework/SECTION_MAPPING.md): the section contract the validator checks.
- [`framework/_regenerate_claude_only.py`](../../framework/_regenerate_claude_only.py): a lighter variant that only refreshes `CLAUDE.md` files.
