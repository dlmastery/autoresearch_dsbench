"""Audit one or all task repos against the SECTION_MAPPING + artifact rules."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
FRAMEWORK = ROOT / "framework"


REQUIRED_FILES = [
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


def _required_sections() -> list[str]:
    """Parse the substring column from SECTION_MAPPING.md."""
    txt = (FRAMEWORK / "SECTION_MAPPING.md").read_text(encoding="utf-8")
    out: list[str] = []
    for line in txt.splitlines():
        if not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 4:
            continue
        loc = parts[3]
        if loc.startswith("`") and loc.endswith("`"):
            out.append(loc.strip("`"))
    return out


def audit_repo(repo: Path) -> dict:
    out: dict = {"repo": str(repo), "missing_files": [], "missing_sections": [],
                 "warnings": [], "ok": True}
    if not repo.exists():
        out["ok"] = False
        out["error"] = "repo does not exist"
        return out
    for rel in REQUIRED_FILES:
        if not (repo / rel).exists():
            out["missing_files"].append(rel)
            out["ok"] = False
    claude_path = repo / "CLAUDE.md"
    if claude_path.exists():
        claude = claude_path.read_text(encoding="utf-8")
        for section in _required_sections():
            if section not in claude:
                out["missing_sections"].append(section)
                out["ok"] = False
    # Sanity: test set must not be referenced by runner.py / hill_climb.py inside the task
    for f in ("run_autoresearch.py", "hill_climb.py"):
        p = repo / f
        if p.exists():
            txt = p.read_text(encoding="utf-8", errors="ignore")
            if "y_test" in txt or "X_test" in txt:
                out["warnings"].append(f"{f} references X_test/y_test — must be removed")
                out["ok"] = False
    # Experiment count target
    log = repo / "autoresearch_results" / "experiment_log.jsonl"
    if log.exists():
        n_exps = sum(1 for _ in log.read_text(encoding="utf-8").splitlines() if _.strip())
        out["n_experiments"] = n_exps
    return out


def audit_all(roots: Iterable[Path]) -> list[dict]:
    reports: list[dict] = []
    for r in roots:
        if not r.exists():
            continue
        for child in sorted(r.iterdir()):
            if child.is_dir() and (child / "CLAUDE.md").exists():
                reports.append(audit_repo(child))
    return reports


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--repo", default=None, help="audit one repo; omit to audit modeling/* + analysis/*")
    p.add_argument("--strict", action="store_true",
                   help="exit non-zero if ANY repo fails the audit")
    p.add_argument("--report", default=str(ROOT / "registry" / "audit_report.json"))
    args = p.parse_args()
    if args.repo:
        reports = [audit_repo(Path(args.repo).resolve())]
    else:
        reports = audit_all([ROOT / "modeling", ROOT / "analysis"])
    Path(args.report).parent.mkdir(parents=True, exist_ok=True)
    Path(args.report).write_text(json.dumps(reports, indent=2), encoding="utf-8")
    n_ok = sum(1 for r in reports if r["ok"])
    print(f"[validator] {n_ok}/{len(reports)} repos ok — report at {args.report}")
    if reports and not all(r["ok"] for r in reports):
        # Show first 5 failures
        for r in reports:
            if not r["ok"]:
                print(f"  [FAIL] {r['repo']}")
                if r["missing_files"]:
                    print(f"         missing files: {r['missing_files'][:3]}")
                if r["missing_sections"]:
                    print(f"         missing sections: {r['missing_sections'][:3]}")
                if r["warnings"]:
                    print(f"         warnings: {r['warnings'][:2]}")
        if args.strict:
            sys.exit(1)


if __name__ == "__main__":
    main()
