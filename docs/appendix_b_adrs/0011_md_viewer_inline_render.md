# ADR-0011: All `.md` links route through `dashboard/md_viewer.html`

## Status

Accepted (2026-05-15). Lesson 10 in `framework/CLAUDE_template.md`.

## Context

Per-task dashboards link to multiple Markdown artefacts: `experiment_summary.md`, `research_journal.md`, `paper.md`, `CLAUDE.md`, `forensic_audit.md`, `checkpoint.md`, `audit_report.md`. Chromium-family browsers (Chrome, Edge, Brave) default to **downloading** `.text/markdown` files instead of rendering them. Firefox renders them as preformatted text, which is also not what we want.

Direct links to `.md` files therefore produce a download dialog, not a readable page. Reviewers click a link expecting to read the document and get a save-as prompt instead.

## Decision

**Every `.md` link in any dashboard MUST route through `dashboard/md_viewer.html`:**

```
dashboard/md_viewer.html?path=<relative-or-absolute>
```

The viewer is a single-page HTML app that:

1. Reads the `path` query string.
2. Fetches the markdown via `fetch(path)`.
3. Renders it client-side via `marked.js` (CommonMark) into a styled `<article>`.
4. Adds syntax highlighting for code blocks via `highlight.js`.
5. Inlines mermaid diagrams via `mermaid.js`.

The viewer is checked into both `dashboard/md_viewer.html` (for the cross-task dashboard) and `submissions/md_viewer.html` (for the submission archive's local browser).

`framework/_refresh_dashboards.py` rewrites every `.md` link in the per-task dashboard template to use the viewer:

```html
<!-- WRONG -->
<a href="autoresearch_results/research_journal.md">Journal</a>

<!-- RIGHT -->
<a href="../../dashboard/md_viewer.html?path=modeling/titanic/autoresearch_results/research_journal.md">Journal</a>
```

The skill `interactive-dashboard-design` documents the rule.

## Consequences

**Easier:**

- Reviewers click and read. No download-dialog friction.
- Mermaid diagrams in `.md` artefacts render inline. Code blocks are syntax-highlighted.
- The viewer is a single file — easy to fork, easy to vendor.

**Harder:**

- All `.md` links must be routed via the viewer. The `_final_audit.py` end-to-end check counts viewer-references in `framework/dashboard_template.html` and `dashboard/task_detail.html` (Lesson 22).
- Local development: opening a per-task dashboard via `file://` fails to fetch the markdown (CORS). The dev workflow uses `python -m http.server 8501 --directory <repo>` per the `framework/CLAUDE_template.md` "Session Start" step.

**Riskier:**

- A future browser may default to rendering `.md` natively, making the viewer obsolete. The pattern still works (the viewer is a no-op layer), so no immediate action needed. We re-evaluate annually.

## Related

- [`0012_two_tab_navigation.md`](0012_two_tab_navigation.md)
- Skills `interactive-dashboard-design`, `dashboard-files-update-mandate`.
- `dashboard/md_viewer.html`.
- `framework/_refresh_dashboards.py`.
