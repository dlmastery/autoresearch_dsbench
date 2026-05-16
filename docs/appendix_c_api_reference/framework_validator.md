# API Reference — `framework.validator`

> Layer 1 of the 4-layer audit gate: section-coverage validator.

## Module: `framework.validator`

`C:/Users/evija/dsbench/framework/validator.py`

## Public functions

### `audit_repo(repo) -> dict`

Audit a single task repo. Returns:

```python
{
    "repo": "C:/Users/evija/dsbench/modeling/titanic",
    "missing_files": [],
    "missing_sections": [],
    "warnings": [],
    "n_experiments": 125,
    "ok": True,
}
```

### `_required_sections() -> list[str]`

Parse `framework/SECTION_MAPPING.md` and return the list of required substring headers. The mapping has 44 rows; every row's "Task CLAUDE.md location" cell becomes a required substring.

### Required files

Defined as a module-level constant `REQUIRED_FILES`:

```python
[
    "CLAUDE.md",
    "README.md",
    "paper.md",
    "paper_abstract.md",
    "task_config.json",
    "seed_reasoning.json",
    "run_autoresearch.py",
    "hill_climb.py",
    "third_party_audit.py",
    "memory/project_autoresearch_checkpoint.md",
    "autoresearch_results/dashboard.html",
    "autoresearch_results/experiment_summary.md",
    "autoresearch_results/research_journal.md",
    "autoresearch_results/reasoning_annotations.json",
    "data/splits.py",
]
```

A missing file marks the task `ok: false`.

### Test-set leakage check

For each of `run_autoresearch.py` and `hill_climb.py`, the validator greps for `X_test` and `y_test`. Any hit produces a warning AND marks the task `ok: false` — test leakage is a blocking error. See [`../appendix_b_adrs/0002_train_val_only_for_hill_climb.md`](../appendix_b_adrs/0002_train_val_only_for_hill_climb.md).

## CLI

```powershell
# All 112 tasks
& "C:/Users/evija/anaconda3/python.exe" framework/validator.py

# Strict mode (exit code 1 on any failure)
& "C:/Users/evija/anaconda3/python.exe" framework/validator.py --strict
```

Output: per-task ok / not-ok summary, followed by `<n>/<total> ok`. Detailed failures are written to `registry/audit_report.json`.

## Related

- [`../part_3_processes/09_code_review.md`](../part_3_processes/09_code_review.md) — Layer 2 of the audit gate.
- [`../appendix_b_adrs/0015_four_layer_audit_gate.md`](../appendix_b_adrs/0015_four_layer_audit_gate.md)
- `framework/SECTION_MAPPING.md` — the source of required substrings.
