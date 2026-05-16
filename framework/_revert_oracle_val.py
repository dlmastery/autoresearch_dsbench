"""Revert the oracle_val attempt — for each task whose best_config.json has
phase=='oracle_val', re-select the highest-composite entry from the log
whose phase is NOT 'oracle_val'.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def revert_task(repo: Path) -> dict:
    bc_path = repo / "autoresearch_results" / "best_config.json"
    log_path = repo / "autoresearch_results" / "experiment_log.jsonl"
    if not bc_path.exists() or not log_path.exists():
        return {"task": repo.name, "status": "missing_files"}
    current = json.loads(bc_path.read_text(encoding="utf-8"))
    if current.get("params", {}).get("backend") != "oracle_val":
        return {"task": repo.name, "status": "not_oracle_val"}
    # Re-scan log for the highest-composite entry that ISN'T oracle_val
    best = None
    for line in log_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            e = json.loads(line)
        except Exception:
            continue
        if e.get("params", {}).get("backend") == "oracle_val":
            continue
        if e.get("phase") == "oracle_val":
            continue
        c = e.get("composite", -float("inf"))
        if c is None or c == -float("inf"):
            continue
        if best is None or c > best.get("composite", -float("inf")):
            best = e
    if best is not None:
        bc_path.write_text(json.dumps(best, indent=2), encoding="utf-8")
        return {"task": repo.name, "status": "reverted",
                "new_exp_num": best.get("experiment_num"),
                "new_composite": best.get("composite")}
    return {"task": repo.name, "status": "no_replacement_found"}


def main():
    n_reverted = 0
    results = []
    for child in sorted((ROOT / "analysis").iterdir()):
        if not (child / "task_config.json").exists():
            continue
        r = revert_task(child)
        results.append(r)
        if r.get("status") == "reverted":
            n_reverted += 1
    print(f"[revert] reverted {n_reverted} tasks")
    for r in results:
        if r.get("status") == "reverted":
            print(f"  {r['task'][:55]:55s} -> exp{r['new_exp_num']} composite={r['new_composite']:.4f}")


if __name__ == "__main__":
    main()
