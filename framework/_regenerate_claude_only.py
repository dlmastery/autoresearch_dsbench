"""Re-render every per-task CLAUDE.md from the updated CLAUDE_template.md.

Idempotent. Touches ONLY each task's CLAUDE.md — leaves seed_reasoning,
memory checkpoint, paper.md, README, autoresearch_results/*, and code
versions untouched.

Usage:
    "C:/Users/evija/anaconda3/python.exe" framework/_regenerate_claude_only.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from framework.generate_scaffolds import render_claude  # noqa: E402


def main() -> None:
    modeling = json.loads((ROOT / "registry" / "modeling_tasks.json").read_text(encoding="utf-8"))
    analysis = json.loads((ROOT / "registry" / "analysis_tasks.json").read_text(encoding="utf-8"))
    port = 8765
    n_written = 0
    n_missing = 0
    for task in modeling:
        task["kind"] = "modeling"
        repo = ROOT / "modeling" / task["slug"]
        if not repo.exists():
            n_missing += 1
            continue
        (repo / "CLAUDE.md").write_text(render_claude(task, port, repo), encoding="utf-8")
        n_written += 1
    for task in analysis:
        task["kind"] = "analysis"
        repo = ROOT / "analysis" / task["slug"]
        if not repo.exists():
            n_missing += 1
            continue
        (repo / "CLAUDE.md").write_text(render_claude(task, port, repo), encoding="utf-8")
        n_written += 1
    print(f"[regen] wrote {n_written} CLAUDE.md files ({n_missing} missing repos)")


if __name__ == "__main__":
    main()
