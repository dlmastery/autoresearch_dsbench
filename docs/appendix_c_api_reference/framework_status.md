# API Reference — `framework._status` and rollup utilities

> One-command status snapshots. The canonical "how is the run going?" tool.

## Module: `framework._status`

`C:/Users/evija/dsbench/framework/_status.py`

### Behaviour

Reads `registry/final_rollup.json` + `registry/forensic_summary.json` and prints:

```
BEAT-DSBENCH:   modeling=82/74  analysis=8/38   total=90/112
FORENSIC PASS:  modeling=74/74  analysis=38/38  total=112/112
FORENSIC FAIL:  modeling=0/74

=== modeling FORENSIC FAILS ===
```

### Critical asymmetry

The two rollup files disagree on the modeling-vs-analysis distinction key (Lesson 14):

- **`final_rollup.json` rows DO NOT carry a `kind` field.** The modeling-vs-analysis distinction is `problem_type != "qa_excel"` → modeling; `problem_type == "qa_excel"` → analysis.
- **`forensic_summary.json` rows DO carry a `kind` field** (`modeling` or `analysis`).

Code reading both files MUST account for this asymmetry — the canonical pattern is:

```python
def is_mod(r):     return r.get("problem_type") != "qa_excel"  # rollup row
def is_mod_f(f):   return f.get("kind") == "modeling"           # forensic row
```

Mixing the two keys silently miscounts task health.

## CLI

```powershell
& "C:/Users/evija/anaconda3/python.exe" framework/_status.py
```

No arguments.

## Companion utilities

| Module | Purpose |
|---|---|
| `framework/_summary.py` | Top-10 BEATs per kind + backbone-win histogram. |
| `framework/_losses.py` | Loss list per kind + write `registry/losses.json` for the extension driver. |
| `framework/_audit_summary.py` | Forensic PASS/FAIL summary + still-losing-tasks table. |
| `framework/_final_audit.py` | End-to-end cross-check audit; combines all 4 layers + 7 additional checks. |

Each is a 30-60 line script — read the source to see the exact print format.

## Related

- [`../appendix_b_adrs/0014_github_checkpoint_protocol.md`](../appendix_b_adrs/0014_github_checkpoint_protocol.md) Lesson 14.
- [`../part_4_tools/16_version_control_and_branches.md`](../part_4_tools/16_version_control_and_branches.md)
- Skill `mlops-documentation`.
