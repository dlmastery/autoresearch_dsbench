# CLI Reference — Every Command in the Project

> Every script in `framework/` exposed as a CLI. All commands assume working directory `C:/Users/evija/dsbench/` and interpreter `C:/Users/evija/anaconda3/python.exe`.

## Pipeline commands (in order of typical use)

### Scaffold generation

```powershell
& "C:/Users/evija/anaconda3/python.exe" framework/generate_scaffolds.py
```

Reads `registry/modeling_tasks.json` + `registry/analysis_tasks.json`. Writes 112 per-task repos under `modeling/<slug>/` and `analysis/<slug>/`. Idempotent.

### Single experiment

```powershell
& "C:/Users/evija/anaconda3/python.exe" framework/runner.py `
    --repo <task-dir> --backbone <name> `
    --params '<json-dict>' --description '<text>' --experiment-num <int>
```

See [`framework_runner.md`](framework_runner.md).

### Per-task hill-climb

```powershell
& "C:/Users/evija/anaconda3/python.exe" framework/hill_climb.py --repo <task-dir>
```

Runs 25 iters × N backbones. Idempotent.

### All-tasks driver

```powershell
& "C:/Users/evija/anaconda3/python.exe" framework/run_all.py [--kind modeling|analysis]
```

Drives `hill_climb.py` for every task. Without `--kind`, runs both.

### Extended 200-iter

```powershell
& "C:/Users/evija/anaconda3/python.exe" framework/run_extended.py
& "C:/Users/evija/anaconda3/python.exe" framework/extended_hill_climb.py --repo <task-dir>
```

The driver picks tasks from `registry/losses.json`; the per-task script runs the 200-iter recovery cycle.

### Final report

```powershell
& "C:/Users/evija/anaconda3/python.exe" framework/final_report.py [--repo <task-dir>]
```

ONE-SHOT test-set refit. Writes `final_report.json` per task + `registry/final_rollup.json` cross-task.

### Submission archive

```powershell
& "C:/Users/evija/anaconda3/python.exe" framework/build_submission.py [--repo <task-dir>]
```

See [`framework_build_submission.md`](framework_build_submission.md).

### Dashboard refresh

```powershell
& "C:/Users/evija/anaconda3/python.exe" framework/_refresh_dashboards.py
```

Regenerate per-task `dashboard.html` from `framework/dashboard_template.html` with the "About this task" block.

### CLAUDE.md regeneration

```powershell
& "C:/Users/evija/anaconda3/python.exe" framework/_regenerate_claude_only.py
```

Re-render every per-task `CLAUDE.md` from `framework/CLAUDE_template.md`.

## Audit commands

### Layer 1 — Section coverage

```powershell
& "C:/Users/evija/anaconda3/python.exe" framework/validator.py [--strict]
```

### Layer 2 — Forensic committee

```powershell
& "C:/Users/evija/anaconda3/python.exe" framework/forensic_audit.py [--repo <task-dir>]
```

### Layer 4 — Skill-pack coverage

```powershell
& "C:/Users/evija/anaconda3/python.exe" skills/autoresearch-pack/audit/audit_pack.py
```

### Aggregator

```powershell
& "C:/Users/evija/anaconda3/python.exe" framework/_final_audit.py
```

End-to-end cross-check: all 4 layers + 7 additional checks (Lessons-Learned, About-dropdown, md_viewer routes, etc.).

## Status / introspection

```powershell
& "C:/Users/evija/anaconda3/python.exe" framework/_status.py          # BEAT / FORENSIC counts
& "C:/Users/evija/anaconda3/python.exe" framework/_summary.py         # Top-10 BEATs + backbone wins
& "C:/Users/evija/anaconda3/python.exe" framework/_losses.py          # Loss list per kind
& "C:/Users/evija/anaconda3/python.exe" framework/_audit_summary.py   # Forensic + still-losing
```

## Dashboard server (manual start)

```powershell
& "C:/Users/evija/anaconda3/python.exe" -m http.server 8501 --directory C:/Users/evija/dsbench
```

Open `http://localhost:8501/dashboard/index.html`.

## Git operations

```powershell
git -C C:/Users/evija/dsbench status
git -C C:/Users/evija/dsbench add -A
git -C C:/Users/evija/dsbench commit -F C:/Users/evija/dsbench/.commit_msg.txt
git -C C:/Users/evija/dsbench push origin main

# One-time per-machine TLS fix (Windows)
git config --global http.sslBackend schannel
```

## Related

- [`../README.md`](../README.md) — operational procedures combining these commands.
- `framework/CLAUDE_template.md` § "Single-command end-to-end refresh" — the 9-step propagation ritual.
