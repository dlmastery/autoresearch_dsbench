"""Drive 25-iter-per-backbone hill climbing across all 112 task repos."""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import traceback
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from framework.hill_climb import hill_climb_all  # noqa: E402
from framework.validator import audit_repo  # noqa: E402
from framework.final_report import report_repo  # noqa: E402


def all_repos() -> list[Path]:
    out: list[Path] = []
    for root in (ROOT / "modeling", ROOT / "analysis"):
        for child in sorted(root.iterdir()):
            if (child / "task_config.json").exists():
                out.append(child)
    return out


def process(repo: Path, do_final: bool = True) -> dict:
    t0 = time.time()
    audit_pre = audit_repo(repo)
    if not audit_pre["ok"]:
        return {"task": repo.name, "status": "audit_failed_pre", "report": audit_pre}
    try:
        hill = hill_climb_all(repo)
    except Exception as exc:
        return {"task": repo.name, "status": "hill_climb_error",
                "error": str(exc), "traceback": traceback.format_exc()}
    audit_post = audit_repo(repo)
    final: dict | None = None
    if do_final and (repo / "autoresearch_results" / "best_config.json").exists():
        try:
            final = report_repo(repo)
        except Exception as exc:
            final = {"error": str(exc), "traceback": traceback.format_exc()}
    return {
        "task": repo.name,
        "status": "ok" if audit_post["ok"] else "audit_failed_post",
        "elapsed_sec": time.time() - t0,
        "hill": hill,
        "audit": audit_post,
        "final": final,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--max", type=int, default=None,
                   help="limit number of repos processed")
    p.add_argument("--kind", choices=("modeling", "analysis", "both"), default="both")
    p.add_argument("--skip-final", action="store_true",
                   help="skip the test-set final report pass (still does hill climb)")
    p.add_argument("--log", default=str(ROOT / "registry" / "run_all_log.jsonl"))
    args = p.parse_args()

    repos = all_repos()
    if args.kind != "both":
        repos = [r for r in repos if r.parent.name == args.kind]
    if args.max:
        repos = repos[: args.max]
    print(f"[run_all] processing {len(repos)} repos")

    log_path = Path(args.log)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    summary: list[dict] = []
    for i, repo in enumerate(repos, start=1):
        rec = process(repo, do_final=not args.skip_final)
        summary.append(rec)
        with log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")
        elapsed = rec.get("elapsed_sec", 0)
        status = rec["status"]
        print(f"  [{i}/{len(repos)}] {repo.name:60s} {status:10s} {elapsed:6.1f}s")

    # roll-up
    out = ROOT / "registry" / "run_all_summary.json"
    out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    n_ok = sum(1 for r in summary if r["status"] == "ok")
    print(f"[run_all] done: {n_ok}/{len(summary)} ok — summary at {out}")


if __name__ == "__main__":
    main()
