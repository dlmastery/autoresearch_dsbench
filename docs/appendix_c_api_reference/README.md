# Appendix C — API Reference

> Per-module documentation for the shared `framework/` library, the CLI, and the glossary.

This appendix is the reference manual. Each page describes one module: its purpose, public functions, side effects, CLI invocation, and related chapters.

## Module pages

| Module | Page | Purpose |
|---|---|---|
| `framework.runner` | [`framework_runner.md`](framework_runner.md) | Single-experiment runner. Logs only. |
| `framework.hill_climb` | [`framework_hill_climb.md`](framework_hill_climb.md) | Base 25-iter × 5-backbone loop. |
| `framework.extended_hill_climb` | [`framework_extended_hill_climb.md`](framework_extended_hill_climb.md) | 200-iter recovery cycle across 15 backbone families. |
| `framework.forensic_audit` | [`framework_forensic_audit.md`](framework_forensic_audit.md) | 10-agent forensic committee. |
| `framework.final_report` | [`framework_final_report.md`](framework_final_report.md) | One-shot test-set refit. Only legal reader of the test set. |
| `framework.build_submission` | [`framework_build_submission.md`](framework_build_submission.md) | 14-file per-task submission archive builder. |
| `framework.validator` | [`framework_validator.md`](framework_validator.md) | Section-coverage validator + X_test grep. Layer 1. |
| `framework._status` | [`framework_status.md`](framework_status.md) | Cohort scoreboard. |
| `framework.generate_scaffolds` | [`framework_generate_scaffolds.md`](framework_generate_scaffolds.md) | Per-task scaffold generator. |
| `framework._refresh_dashboards` | [`framework_refresh_dashboards.md`](framework_refresh_dashboards.md) | Single-command dashboard refresh. |
| `framework._final_audit` | [`framework_final_audit.md`](framework_final_audit.md) | Four-layer audit-gate aggregator. |

## CLI and glossary

- [`cli_reference.md`](cli_reference.md) — every CLI command in the project.
- [`glossary.md`](glossary.md) — project-specific terms and the full citation list.

## Notes on conventions

- Every module page documents *public* functions only. Helpers prefixed with `_` are implementation detail and may change between commits.
- Side effects are documented exhaustively. A function that writes to disk says so.
- Wall-clock times are measured on the reference hardware (Intel 14th-gen HX laptop, 16 GB GPU). Times on other hardware may differ.
- Citations follow the Citation-Rigor Rule: Author, YEAR, VENUE, *Title*, arXiv ID, one-sentence relevance.

## Related

- [Ch. 18 — Build Systems](../part_4_tools/18_build_systems.md): the build pipeline that uses these modules.
- [Ch. 23 — Continuous Integration](../part_4_tools/23_continuous_integration.md): the audit gate that runs them in sequence.
- [`framework/CLAUDE_template.md`](../../framework/CLAUDE_template.md): the project's style guide.
