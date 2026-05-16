# Contributing to DSBench AutoResearch

> Thanks for considering a contribution. The project is single-operator but the discipline applies to anyone who edits the code or the protocol.

## Before you start

1. Read [`../part_1_thesis/01_what_is_autoresearch_engineering.md`](../part_1_thesis/01_what_is_autoresearch_engineering.md) — 5-minute orientation.
2. Read [`../part_1_thesis/01_what_is_autoresearch_engineering.md`](../part_1_thesis/01_what_is_autoresearch_engineering.md) — what we built and why.
3. Read [`../appendix_b_adrs/`](../appendix_b_adrs/) — the 15 decisions that shape the codebase.
4. Set up locally per [`../part_4_tools/18_build_systems.md`](../part_4_tools/18_build_systems.md).

## How to propose a change

| Change type | Path |
|---|---|
| New protocol rule | Add a row to `framework/CLAUDE_template.md` Lessons-Learned + a new or extended skill in `skills/autoresearch-pack/` + an ADR. See [`../part_3_processes/15_deprecation.md`](../part_3_processes/15_deprecation.md). |
| Bug fix in framework | Open the file, fix the bug, add a unit test under `framework/_test_*.py`, run the 4-layer audit. See [`../part_4_tools/23_continuous_integration.md`](../part_4_tools/23_continuous_integration.md). |
| New backbone | Add the dispatch case to `framework.runner._fit_predict`, add per-backbone proposals to `framework.hill_climb`, add a recipe to `framework/sota_catalog.yaml`. |
| New task | See [`../part_3_processes/15_deprecation.md`](../part_3_processes/15_deprecation.md). |
| New ADR | Copy the template from [`../appendix_b_adrs/`](../appendix_b_adrs/). |
| New postmortem | Copy the template from [`../appendix_a_postmortems/`](../appendix_a_postmortems/). |
| Documentation | Edit the relevant page. See [`style_guide.md`](style_guide.md). |

## Pre-commit checklist

Full 4-layer audit gate. See [`../part_4_tools/23_continuous_integration.md`](../part_4_tools/23_continuous_integration.md):

1. `framework/validator.py` — 112/112 ok.
2. `framework/forensic_audit.py` — 112/112 PASS.
3. `framework/build_submission.py` — refreshed.
4. `skills/autoresearch-pack/audit/audit_pack.py` — 100% coverage.
5. `framework/_final_audit.py` — green.

The 9-step "Single-command end-to-end refresh" in `framework/CLAUDE_template.md` is the canonical ritual.

## Commit message format

Subject line ≤ 70 chars. Imperative ("add", "fix", "extend"). Optional `<area>:` prefix.

```
docs: Google SRE-workbook-quality docs/ folder

- ~50 markdown files across architecture / ADR / runbooks / postmortems / reference / SLOs / onboarding / contributing
- 5 mermaid diagrams under architecture/diagrams/
- audit: validator 112/112, forensic 112/112 PASS, skills 156/156

Co-Authored-By: Claude
```

PowerShell heredocs are flaky; write multi-line messages to `.commit_msg.txt` and pass `-F`.

## Code style

- Python 3.10+ type hints. `from __future__ import annotations`.
- f-strings, not `%` formatting.
- Pathlib, not `os.path`.
- No global mutable state in the framework.
- Imports: stdlib → third-party → local.
- See [`style_guide.md`](style_guide.md).

## Citations matter

Every paper reference in code comments, ADRs, postmortems, and reasoning annotations follows:

```
Author1, Author2, Author3 YEAR VENUE 'Paper Title' (arXiv:XXXX.XXXXX) — one-sentence relevance.
```

Parenthetical-only tags (`(Bishop 2006)`) are insufficient.

## Code of conduct

Be precise. Be honest about uncertainty. Don't ship a number you can't reproduce.

## Where to ask

Single-operator project. Direct questions to `eranti@gmail.com`.

## Related

- [`style_guide.md`](style_guide.md)
- [`pr_template.md`](pr_template.md)
- [`issue_template.md`](issue_template.md)
