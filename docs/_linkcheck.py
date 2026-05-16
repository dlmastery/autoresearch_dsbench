"""Link-checker for docs/ Markdown files.

Reports broken internal links: file paths that don't resolve.
External links (http://, https://, mailto:) are not checked.
Anchor-only links (#section) are not checked.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LINK_RE = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)]+)\)")


def check_file(p: Path) -> list[tuple[int, str, str]]:
    broken: list[tuple[int, str, str]] = []
    try:
        text = p.read_text(encoding="utf-8")
    except Exception:
        return broken
    for line_no, line in enumerate(text.splitlines(), start=1):
        for m in LINK_RE.finditer(line):
            txt, target = m.group(1), m.group(2)
            if target.startswith(("http://", "https://", "mailto:", "ftp://", "#")):
                continue
            file_part = target.split("#", 1)[0]
            if not file_part:
                continue
            candidate = (p.parent / file_part).resolve()
            if not candidate.exists():
                broken.append((line_no, txt, target))
    return broken


def main() -> None:
    broken_total = 0
    files_with_broken = 0
    for p in ROOT.rglob("*.md"):
        broken = check_file(p)
        if broken:
            files_with_broken += 1
            rel = p.relative_to(ROOT)
            print(f"\n{rel}:")
            for ln, txt, tgt in broken:
                print(f"  L{ln}: [{txt}]({tgt})")
                broken_total += 1
    print(f"\n=== {broken_total} broken links across {files_with_broken} files ===")
    sys.exit(1 if broken_total else 0)


if __name__ == "__main__":
    main()
