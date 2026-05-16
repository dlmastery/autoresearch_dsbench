# API Reference — `framework.forensic_audit`

> The 10-agent forensic committee. See [`../part_3_processes/09_code_review.md`](../part_3_processes/09_code_review.md) for the design.

## Module: `framework.forensic_audit`

`C:/Users/evija/dsbench/framework/forensic_audit.py`

## Public functions

### `audit_repo(repo) -> dict`

Run agents A-J + Z on the task at `repo`. Returns a dict:

```python
{
    "task": "titanic",
    "kind": "modeling",
    "agents": {
        "A_split_hash": {"ok": True, "mismatches": {}, "n_train": 623, ...},
        "B_target_leakage": {"ok": True, "max_mi": 0.04, ...},
        ...
        "Z_committee_verdict": {"verdict": "PASS", "warnings": []},
    },
    "verdict": "PASS",
    "warnings": [],
}
```

**Side effects:** writes `<repo>/forensic_audit.md` (narrative) and `<repo>/forensic_audit.json` (machine-readable).

### Agent functions

Each agent is a top-level function `agent_<letter>_<name>(repo) -> dict` returning at minimum `{"agent": "...", "ok": bool}`. Implementing a new agent is one function plus a wiring entry in the `_run_all_agents` dispatcher.

| Function | Concern |
|---|---|
| `agent_a_split_hash(repo)` | Manifest hashes vs cached `splits.npz` |
| `agent_b_target_leakage(repo)` | Per-feature MI vs label (problem-type-aware threshold) |
| `agent_c_row_overlap(repo)` | Train/val/test row hash intersection |
| `agent_d_distribution_shift(repo)` | Per-feature KS (tabular) / chi-square (qa_excel) |
| `agent_e_anomaly(repo)` | val > train, perfect 1.0, jumps > 0.3, with whitelist |
| `agent_f_static_code(repo)` | grep `X_test` / `y_test` in runner code |
| `agent_g_temporal_order(repo)` | No future timestamps in train |
| `agent_h_seed_stability(repo)` | Multi-seed champion variance (RECORD-ONLY) |
| `agent_i_refit_consistency(repo)` | Champion refits within ±0.005 of recorded test score |
| `agent_j_backbone_diversity(repo)` | ≥ 3 distinct backbones in log (WARN if not) |
| `agent_z_committee(results)` | Aggregator |

## CLI

```powershell
# all tasks
& "C:/Users/evija/anaconda3/python.exe" framework/forensic_audit.py

# one task
& "C:/Users/evija/anaconda3/python.exe" framework/forensic_audit.py --repo modeling/titanic
```

After a full run, `registry/forensic_summary.json` carries one row per task: `{task, kind, verdict, warnings}`. This is the file `framework/_status.py` reads to print FORENSIC-PASS / FAIL counts.

## Output schema

`<repo>/forensic_audit.json`:

```json
{
  "task": "titanic",
  "kind": "modeling",
  "verdict": "PASS",
  "warnings": [],
  "agents": {
    "A_split_hash": {"ok": true, "n_train": 623, "n_val": 134, "n_test": 134},
    "B_target_leakage": {"ok": true, "max_mi": 0.041, "top_features": [...]},
    "C_row_overlap": {"ok": true, "train_val": 0, "train_test": 0, "val_test": 0},
    "D_distribution_shift": {"ok": true, "flagged_pct": 6.2},
    "E_anomaly": {"ok": true, "suspicions": [], "suppressed": []},
    "F_static_code": {"ok": true, "x_test_refs": [], "y_test_refs": []},
    "G_temporal_order": {"ok": true, "note": "N/A on synthetic data"},
    "H_seed_stability": {"std_composite": 0.012, "note": "record-only"},
    "I_refit_consistency": {"ok": true, "delta": 0.0009},
    "J_backbone_diversity": {"ok": true, "n_distinct": 5}
  }
}
```

## Related

- [`../part_3_processes/09_code_review.md`](../part_3_processes/09_code_review.md)
- [`../appendix_b_adrs/0004_10_agent_forensic_committee.md`](../appendix_b_adrs/0004_10_agent_forensic_committee.md)
- [`../appendix_b_adrs/0010_sklearn_early_stopping_whitelist.md`](../appendix_b_adrs/0010_sklearn_early_stopping_whitelist.md)
- [`../part_3_processes/09_code_review.md`](../part_3_processes/09_code_review.md)
