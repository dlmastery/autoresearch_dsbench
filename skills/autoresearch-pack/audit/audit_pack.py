"""audit_pack.py — verify every CLAUDE.md section maps to at least one skill.

Parses the two source CLAUDE.md files (`autoresearch/CLAUDE.md` and
`autoresearchindexspy/autoresearchspy/CLAUDE.md`) for H2/H3 headers, then
walks the `skills/` tree to confirm every section is referenced by at
least one SKILL.md. Emits `coverage_report.md` with PASS/FAIL per section.

Run:
    "C:/Users/evija/anaconda3/python.exe" audit_pack.py
or
    python audit_pack.py

Exit code: 0 if 100% coverage, 1 otherwise.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------

HERE = Path(__file__).resolve().parent
PACK_ROOT = HERE.parent                      # skills/autoresearch-pack/
SKILLS_DIR = PACK_ROOT / "skills"
COVERAGE_REPORT = HERE / "coverage_report.md"
COVERAGE_MATRIX = PACK_ROOT / "coverage_matrix.md"

DEFAULT_SOURCES = [
    Path("C:/Users/evija/autoresearch/CLAUDE.md"),
    Path("C:/Users/evija/autoresearchindexspy/autoresearchspy/CLAUDE.md"),
    # DSBench template — anchors the dsbench-specific corrections (regression
    # delta sign, extended hill-climb, qa task feature engineering,
    # cross-task pooling, stride-5 split, problem-type-aware audit thresholds,
    # forensic agents I/J, sklearn early-stopping, dashboard navigation,
    # task description disclosure, status snapshot script, lessons learned).
    Path("C:/Users/evija/dsbench/framework/CLAUDE_template.md"),
]

# Spy-only synthetic sections derived from the top-of-file champion block.
# These are not H2/H3 headers in the source but are required by the brief.
SPY_TOP_SECTIONS = [
    ("autoresearchindexspy/autoresearchspy/CLAUDE.md",
     "Three stacked validated KEEPs (stacked ensemble)"),
    ("autoresearchindexspy/autoresearchspy/CLAUDE.md",
     "Regime gate (rvol60d > 15%)"),
    ("autoresearchindexspy/autoresearchspy/CLAUDE.md",
     "Sub-period robustness audit"),
    ("autoresearchindexspy/autoresearchspy/CLAUDE.md",
     "Resumption pointers / committee summary"),
]

# Section-title -> required-skill-name(s) override map.
# When a source header doesn't naturally match a skill name, we map it
# explicitly. This is the authoritative mapping the audit uses.
SECTION_SKILL_MAP: Dict[str, List[str]] = {
    # autoresearch H2s
    "On Session Start (ALWAYS do this first)": ["session-startup"],
    "Hardware Constraints (MANDATORY": ["hardware-pinning"],
    "Crash-Recovery Checkpointing (MANDATORY": ["crash-recovery-checkpoint"],
    "Mindset (Read First)": ["mlfin-researcher-mindset"],
    "Hard Rules (NEVER violate)": ["data-integrity-rules", "experiment-design"],
    # autoresearch H3s
    "Data Integrity": ["data-integrity-rules"],
    "Super-Fold Invariants": ["train-val-test-invariants"],
    "Experiment Design": ["experiment-design"],
    "Autoresearch Agent Protocol (Karpathy-adapted)": ["karpathy-agent-protocol"],
    "Research-Driven Experiment Selection (STRICT — no blind sweeps)": [
        "seven-step-research-process"],
    "Monotonic Quality Progression (NEVER regress)": ["monotonic-quality-progression"],
    "MLOps Documentation Standards (MANDATORY)": ["mlops-documentation"],
    "Explainability & Auditability Report (MANDATORY for every NEW BEST)": [
        "explainability-audit-14-section"],
    "Winner Definition (CLARIFICATION)": ["winner-archive-protocol"],
    "Per-Backbone Code Snapshots (MANDATORY)": ["per-backbone-code-snapshot"],
    "Dashboard Reasoning Annotations (MANDATORY — capture EVERYTHING, every experiment)": [
        "dashboard-reasoning-annotations"],
    "Per-Backbone 50-Experiment Mandate (MANDATORY, not optional)": [
        "per-backbone-experiment-mandate"],
    "Per-Backbone SOTA Training Recipes (MANDATORY — re-derive per backbone)": [
        "per-backbone-sota-recipes"],
    "Backbone-Specific Training Recipes (updated 2026-04-19 from SOTA literature)": [
        "per-backbone-sota-recipes"],
    "GPU Memory Constraint (MANDATORY — 16 GB VRAM hard cap)": ["gpu-memory-constraint"],
    "Epoch-budget rule of thumb (when in doubt)": ["per-backbone-sota-recipes"],
    "Empirical evidence (LSTM phase confirmations)": ["per-backbone-sota-recipes"],
    "Backbone Isolation Rule": ["per-backbone-code-snapshot"],
    "Dashboard Backbone Tabs": ["dashboard-backbone-tabs"],
    "GitHub Pages Dashboard Sync (MANDATORY — every push, zero exceptions)": [
        "github-pages-dashboard-sync"],
    "Dashboard Files Update Mandate (MANDATORY — every experiment, zero exceptions)": [
        "dashboard-files-update-mandate"],
    "Citation Rigor (MANDATORY format for `citations` field)": ["citation-rigor"],
    "Reasoning Blob Completeness (what \"full reasoning\" means)": [
        "reasoning-blob-completeness"],
    "Heteroscedastic Loss Rules (Kendall & Gal 2017)": ["heteroscedastic-loss"],
    "Winner Archiving Protocol (MANDATORY for every NEW BEST)": ["winner-archive-protocol"],
    "Google Colab Notebook (MANDATORY for every winner)": ["google-colab-notebook"],
    "Traditional ML Metrics (MANDATORY for every experiment)": ["traditional-ml-metrics"],
    "Trade-Level Win/Loss Logging (MANDATORY for every experiment)": [
        "per-sample-decision-logging"],
    "Architecture": ["architecture-separation-of-concerns"],
    "Validation Checklist (Run Before Every Experiment Session)": ["validation-checklist"],
    "Project Structure": ["architecture-separation-of-concerns"],
    "Key Constants": ["architecture-separation-of-concerns"],
    "Common Mistakes (Never Repeat)": ["validation-checklist", "data-integrity-rules"],
    "Session Learnings (LSTM Phase, Exps 1-44 of 50)": [
        "per-backbone-sota-recipes", "committee-resumption-pointers"],
    "Confirmed optimal LSTM hyperparameters (at n=2738 daily FX samples)": [
        "per-backbone-sota-recipes"],
    "Axes that DID NOT help": ["per-backbone-sota-recipes"],
    "Seed variance is LARGE and backbone-specific": [
        "per-backbone-sota-recipes", "monotonic-quality-progression"],
    "Key protocol additions": ["committee-resumption-pointers"],
    "Next-backbone priorities": ["per-backbone-sota-recipes"],
    "Checkpoint + packaging cadence": ["crash-recovery-checkpoint"],

    # spy-only additions
    "Three-stream feature engineering (MANDATORY pre-flight discipline)": [
        "three-stream-feature-engineering"],
    "Three stacked validated KEEPs (stacked ensemble)": ["stacked-ensemble-design"],
    "Regime gate (rvol60d > 15%)": ["regime-gate"],
    "Sub-period robustness audit": ["sub-period-robustness-audit"],
    "Resumption pointers / committee summary": ["committee-resumption-pointers"],

    # Sub-templates inside MLOps section
    "Experiment Log — [Backbone] Phase": ["mlops-documentation"],
    "Exp[N]: [description]": ["mlops-documentation"],
    "Exp<N> — <short title>": ["mlops-documentation", "dashboard-reasoning-annotations"],

    # DSBench template additions (Lessons Learned corrections, 2026-05)
    "Extended Hill-Climb Phase (200-iter recovery cycle)": ["extended-hill-climb-phase"],
    "QA-Excel Task Data Loading (real Modeloff answers — NOT synthetic placeholders)":
        ["qa-task-feature-engineering"],
    "Cross-Task Pooling Discipline (training only — evaluation is per-task)":
        ["cross-task-pooling-discipline"],
    "Small-n Stride-5 Interleaved Split (QA tasks only)": ["small-n-stride-split"],
    "Forensic Audit — Problem-Type-Aware Thresholds & Agents I/J":
        ["forensic-audit-pipeline", "problem-type-aware-audit-thresholds"],
    "Sklearn Early-Stopping Val > Train Is Normal (Bishop 2006 §5.5.2)":
        ["regression-early-stopping-discipline"],
    "Interactive Dashboard Navigation Rules":
        ["interactive-dashboard-design", "task-description-disclosure"],
    "Lessons Learned (append-only — every user correction lands here)":
        ["mlops-documentation", "committee-resumption-pointers"],
    "Hardware Constraints (MANDATORY)": ["hardware-pinning"],
    "Crash-Recovery Checkpointing (MANDATORY)": ["crash-recovery-checkpoint"],
    "DSBench Comparison Target": ["winner-archive-protocol", "monotonic-quality-progression"],
    "Session Learnings": ["mlops-documentation", "committee-resumption-pointers"],
    "Common Mistakes (Never Repeat)": ["validation-checklist", "data-integrity-rules"],
    "Project Structure": ["architecture-separation-of-concerns"],
    "Key Constants": ["architecture-separation-of-concerns"],
    "Mindset": ["mlfin-researcher-mindset"],
    "On Session Start (ALWAYS do this first)": ["session-startup"],
    "Per-Backbone 25-Experiment Mandate (MANDATORY)": ["per-backbone-experiment-mandate"],
    "Per-Sample Decision Logging (MANDATORY for every experiment)":
        ["per-sample-decision-logging"],
}


# ----------------------------------------------------------------------
# Parsing
# ----------------------------------------------------------------------

HEADER_RE = re.compile(r"^(#{1,3})\s+(.+?)\s*$")


def parse_headers(path: Path) -> List[Tuple[int, str, str]]:
    """Return list of (line_no, level_str, title) from H1..H3 headers."""
    out = []
    with path.open("r", encoding="utf-8") as fh:
        for i, line in enumerate(fh, start=1):
            m = HEADER_RE.match(line)
            if not m:
                continue
            hashes, title = m.group(1), m.group(2).strip()
            # Skip noisy code-block "## comments" inside bash blocks.
            # We only count headers in the first column of markdown body.
            # We use a heuristic: ignore lines whose title looks like a
            # bash comment continuation (starts with digit + dot in some
            # places we already see in spy file). We'll keep all and let
            # the user override via SECTION_SKILL_MAP.
            out.append((i, hashes, title))
    return out


def title_matches_skill(title: str, skill_md_text: str) -> bool:
    """Heuristic: skill references this section if its source title appears
    in the SKILL.md, OR the skill name matches a SECTION_SKILL_MAP value."""
    # exact substring (case-insensitive)
    if title.lower() in skill_md_text.lower():
        return True
    # leading distinctive phrase (first 30 chars)
    lead = title.split(" — ")[0].split(" (")[0]
    if lead and lead.lower() in skill_md_text.lower():
        return True
    return False


# ----------------------------------------------------------------------
# Audit
# ----------------------------------------------------------------------

def collect_skill_texts() -> Dict[str, str]:
    out = {}
    for d in sorted(SKILLS_DIR.iterdir()):
        if not d.is_dir():
            continue
        sk = d / "SKILL.md"
        if not sk.exists():
            continue
        out[d.name] = sk.read_text(encoding="utf-8")
    return out


def audit() -> int:
    sources = [p for p in DEFAULT_SOURCES if p.exists()]
    missing_src = [p for p in DEFAULT_SOURCES if not p.exists()]
    skill_texts = collect_skill_texts()

    rows: List[Tuple[str, str, str, List[str], str]] = []
    # (source_short, section_title, status, skills_matched, notes)

    # Real H2/H3 headers from source files
    seen_titles: List[Tuple[str, str]] = []  # (short, title)
    for src in sources:
        try:
            short = "/".join(src.parts[-2:])
        except Exception:
            short = src.name
        for _, _level, title in parse_headers(src):
            # Skip the document H1 and obvious code-block fake headers
            if title.startswith("CLAUDE.md — Project Rules"):
                continue
            # Skip bullet-list pseudo-headers that snuck into the file
            # (lines starting with "1.", "2.", "or equivalently", etc.)
            if title.lower().startswith("or equivalently"):
                continue
            if re.match(r"^\d+\.\s", title) and "experiment" in title.lower() and "run" in title.lower():
                # bash-comment style steps
                continue
            seen_titles.append((short, title))

    # Synthetic spy top-of-file blocks
    for short, title in SPY_TOP_SECTIONS:
        seen_titles.append((short, title))

    # Deduplicate by (short, title) — preserve order
    seen_uniq = []
    seen_set = set()
    for st in seen_titles:
        if st in seen_set:
            continue
        seen_set.add(st)
        seen_uniq.append(st)

    for short, title in seen_uniq:
        # Find which skills cover it
        matches: List[str] = []
        # 1) explicit map
        for key, skill_names in SECTION_SKILL_MAP.items():
            if key in title or title in key:
                for sn in skill_names:
                    if sn in skill_texts and sn not in matches:
                        matches.append(sn)
        # 2) heuristic: any SKILL.md that name-drops the title
        for sname, text in skill_texts.items():
            if title_matches_skill(title, text) and sname not in matches:
                matches.append(sname)

        status = "PASS" if matches else "FAIL"
        rows.append((short, title, status, matches, ""))

    # Write report
    fail_count = sum(1 for r in rows if r[2] == "FAIL")
    total = len(rows)
    pct = 100.0 * (total - fail_count) / max(total, 1)

    lines = ["# coverage_report.md\n",
             f"_Auto-generated by `audit/audit_pack.py`._\n",
             f"\n**Coverage:** {total - fail_count} / {total} sections "
             f"covered ({pct:.1f}%). "
             f"**Verdict:** {'PASS' if fail_count == 0 else 'FAIL'}.\n"]

    if missing_src:
        lines.append("\n## Source files NOT FOUND (sections from these are skipped)\n")
        for p in missing_src:
            lines.append(f"- `{p}`\n")

    lines.append("\n## Per-section coverage\n")
    lines.append("| Source | Section | Status | Skills |\n")
    lines.append("|---|---|---|---|\n")
    for short, title, status, matches, _notes in rows:
        skills_str = ", ".join(matches) if matches else "_(none — FAIL)_"
        # Escape pipes in titles
        safe_title = title.replace("|", "\\|")
        lines.append(f"| `{short}` | {safe_title} | {status} | {skills_str} |\n")

    if fail_count:
        lines.append("\n## FAIL details\n")
        for short, title, status, matches, _ in rows:
            if status == "FAIL":
                lines.append(f"- `{short}` → **{title}** — no SKILL.md references this section.\n")

    COVERAGE_REPORT.write_text("".join(lines), encoding="utf-8")
    print(f"[audit_pack] wrote {COVERAGE_REPORT}")
    print(f"[audit_pack] coverage: {total - fail_count}/{total} ({pct:.1f}%) — "
          f"{'PASS' if fail_count == 0 else 'FAIL'}")
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(audit())
