"""Drive 200-iter extended hill climb across all loss/forensic-warning tasks."""
from __future__ import annotations

import argparse
import json
import sys
import time
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from framework.extended_hill_climb import extended_hill_climb  # noqa: E402
from framework.runner import TaskConfig  # noqa: E402


def _next_exp_num(repo: Path) -> int:
    log = repo / "autoresearch_results" / "experiment_log.jsonl"
    if not log.exists():
        return 1
    n = sum(1 for _ in log.read_text(encoding="utf-8").splitlines() if _.strip())
    return n + 1


def regression_loss_tasks() -> list[Path]:
    """The 16 original regression modeling tasks."""
    out: list[Path] = []
    for child in sorted((ROOT / "modeling").iterdir()):
        cfg_p = child / "task_config.json"
        if not cfg_p.exists():
            continue
        cfg = json.loads(cfg_p.read_text(encoding="utf-8"))
        if cfg.get("problem_type") == "regression":
            out.append(child)
    return out


def forensic_fail_tasks(kind: str = "modeling") -> list[Path]:
    summary_p = ROOT / "registry" / "forensic_summary.json"
    if not summary_p.exists():
        return []
    summary = json.loads(summary_p.read_text(encoding="utf-8"))
    out: list[Path] = []
    for r in summary:
        if r.get("verdict") == "FAIL" and r.get("kind") == kind:
            out.append(ROOT / kind / r["task"])
    return out


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--target", choices=("regression", "analysis", "forensic_fails"),
                   default="regression")
    args = p.parse_args()
    if args.target == "regression":
        repos = regression_loss_tasks()
    elif args.target == "forensic_fails":
        repos = forensic_fail_tasks("modeling")
    else:
        # analysis tasks
        repos = sorted([d for d in (ROOT / "analysis").iterdir()
                        if (d / "task_config.json").exists()])
    print(f"[run_extended] target={args.target} repos={len(repos)}")
    log_path = ROOT / "registry" / f"run_extended_{args.target}.jsonl"
    for i, repo in enumerate(repos, start=1):
        t0 = time.time()
        try:
            start = _next_exp_num(repo)
            final = extended_hill_climb(repo, start)
            rec = {"task": repo.name, "kind": repo.parent.name,
                   "start": start, "final": final - 1,
                   "elapsed_sec": time.time() - t0, "status": "ok"}
        except Exception as exc:
            rec = {"task": repo.name, "error": str(exc),
                   "traceback": traceback.format_exc()[:1000],
                   "elapsed_sec": time.time() - t0, "status": "error"}
        with log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")
        print(f"  [{i}/{len(repos)}] {repo.name:55s} {rec.get('status'):8s} "
              f"{rec.get('elapsed_sec', 0):6.1f}s "
              f"{rec.get('start', '?')}->{rec.get('final', '?')}")


if __name__ == "__main__":
    main()
