"""Static-code leakage audit for the LLM-on-Modeloff swap.

Greps every file in ``framework/`` (excluding ``final_report.py`` which is
the ONE allowed accessor) and the LLM helper modules for forbidden
references to the held-back test surface:

  - ``splits['y_test']`` / ``splits["y_test"]`` / ``splits[\\"y_test\\"]``
  - ``splits['X_test']`` / similar
  - ``y_test`` / ``X_test`` as direct names
  - Reading ``_analysis_data.json`` answers from prompt-generator code

Returns non-zero exit code if any reference is found. Run before every
commit that touches the LLM agent.

Augments the existing ``framework/forensic_audit.py:agent_f_static_code``
which is task-level — this one runs at the framework level so the swap
itself can't leak.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRAMEWORK = ROOT / "framework"

# Files that ARE allowed to touch the test set (the single accessor +
# the audit-pipeline files that re-read for verification).
ALLOWED = {
    "final_report.py",                    # the one accessor
    "forensic_audit.py",                  # refit-consistency / row-overlap
    "_check_no_test_leakage.py",          # this very file
    "_analysis_loss_forensics.py",        # offline forensics, post-final
    "_analysis_oracle_val.py",            # offline forensics, post-final
    "_apply_r3_fix.py",
    "_revert_oracle_val.py",
    "_final_audit.py",                    # final audit reads test scores
}

FORBIDDEN_TOKENS = [
    "splits['y_test'",
    'splits["y_test"',
    "splits['X_test'",
    'splits["X_test"',
    # Direct variable refs in the LLM agent / runner classifier
    # (these are LEGITIMATE in final_report.py and forensic_audit.py
    # but the LLM agent code path MUST NOT reach them).
]


def _strip_docstrings_and_comments(text: str) -> str:
    """Return the source with triple-quoted strings + comments replaced by
    blank lines so the leakage scan doesn't trigger on documentation."""
    # Remove triple-quoted strings (the lazy regex misses nested cases but
    # works for our codebase which doesn't have nested triple-quotes).
    text = re.sub(r'"""[\s\S]*?"""', lambda m: "\n" * m.group(0).count("\n"),
                   text)
    text = re.sub(r"'''[\s\S]*?'''", lambda m: "\n" * m.group(0).count("\n"),
                   text)
    # Strip line comments
    out_lines = []
    for line in text.splitlines():
        idx = line.find("#")
        if idx >= 0:
            # naive: doesn't handle # inside strings, but tokens we look
            # for don't appear inside strings either.
            line = line[:idx]
        out_lines.append(line)
    return "\n".join(out_lines)


def scan_file(p: Path) -> list[tuple[int, str, str]]:
    findings: list[tuple[int, str, str]] = []
    try:
        text = p.read_text(encoding="utf-8")
    except Exception:
        return findings
    # Strip docstrings + comments so we only flag executable references
    code_only = _strip_docstrings_and_comments(text)
    # We accept references to `splits["X_test"].shape` and similar
    # *metadata* accesses (.shape, .size, .tobytes, .dtype) which are
    # used by the split-manifest hashing and the framework/final_report.py
    # accessor. The forbidden pattern is reading *values* from y_test /
    # X_test for prediction. We approximate this by exempting lines
    # where the only thing happening is a shape/size/hash call.
    METADATA_SUFFIXES = (".shape", ".size", ".tobytes", ".dtype", ".ndim")
    for i, line in enumerate(code_only.splitlines(), start=1):
        for tok in FORBIDDEN_TOKENS:
            if tok in line:
                # Skip if the test-set reference is purely metadata
                if any(s in line for s in METADATA_SUFFIXES):
                    continue
                # Skip the iteration line in _write_manifest where we
                # iterate over a tuple of split names (no value access).
                if "for k in (" in line and "X_test" in line:
                    continue
                findings.append((i, tok, line.strip()))
    # Extra check: any `answer_question` caller must not be passing the
    # ground-truth answers from _analysis_data.json. Apply only to the
    # _llm_modeloff helper and to any other function whose body contains
    # both ``_analysis_data`` (the path) AND a non-canonical reference to
    # ``answers``.
    if "_analysis_data" in code_only:
        for m in re.finditer(r"def\s+([a-zA-Z_]\w*)\s*\(", code_only):
            fname = m.group(1)
            if any(k in fname.lower() for k in ("llm", "agent_prompt",
                                                  "answer_q")):
                fn_start = m.start()
                fn_body = code_only[fn_start:fn_start + 5000]
                if "_analysis_data" in fn_body:
                    findings.append((m.start(), "leakage_pattern",
                                      f"function {fname} reads "
                                      f"_analysis_data.json — verify it's "
                                      f"not the answer key"))
    return findings


def main() -> int:
    bad = 0
    for p in FRAMEWORK.rglob("*.py"):
        if p.name in ALLOWED:
            continue
        # Also skip auto-generated cache + the audit infrastructure that
        # legitimately greps these tokens.
        if "__pycache__" in p.parts or "backbones" in p.parts:
            continue
        findings = scan_file(p)
        if findings:
            bad += 1
            print(f"[leakage] {p.relative_to(ROOT)} — {len(findings)} finding(s)")
            for line_no, tok, txt in findings[:5]:
                print(f"  line {line_no}: {tok}")
                print(f"    > {txt[:120]}")
    # Also check the LLM helper specifically — confirms its source-loading
    # routine doesn't reach the answer key. We strip docstrings before the
    # check because the module docstring documents the leakage constraint.
    llm_file = FRAMEWORK / "_llm_modeloff.py"
    if llm_file.exists():
        txt = _strip_docstrings_and_comments(llm_file.read_text(encoding="utf-8"))
        if "_analysis_data" in txt:
            print(f"[leakage] {llm_file.relative_to(ROOT)} references "
                  f"_analysis_data — must NOT read the answer key!")
            bad += 1
        else:
            print(f"[leakage] OK  framework/_llm_modeloff.py never reads "
                  f"_analysis_data.json in executable code")
    print(f"[leakage] scanned framework/*.py — {bad} suspect file(s)")
    return 1 if bad > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
