---
name: interactive-dashboard-design
description: Interactive dashboard design — multi-column sort, regex filter, drill-down panels, reasoning-annotation detail view, per-fold tables, backbone tabs, sticky champion summary. Self-contained HTML/JS reading the JSONL/JSON. Triggers on "dashboard design", "interactive dashboard", "multi-column sort", "drill-down", "rich dashboard", "regex filter".
metadata:
  category: dashboard
  source: composite
  related: [dashboard-backbone-tabs, dashboard-reasoning-annotations, dashboard-files-update-mandate]
---

# Interactive Dashboard Design (rich, self-contained)

## When to use

- Designing the dashboard for a new autoresearch project.
- Upgrading a thin "table of experiments" dashboard to a research-grade tool.
- Hand-off to a team that needs to navigate hundreds of experiments fast.

## The rule

The autoresearch dashboards (FX + SPY) demonstrate a self-contained, JSONL-driven, vanilla-HTML/JS pattern. The interactive surface must include all of the following:

### Required UI sections (top to bottom)

1. **Sticky champion summary** — at the top of the page, always visible: global champion composite, test Sharpe, val Sharpe, backbone, exp number, link to winner archive.
2. **Backbone tab bar** — see `dashboard-backbone-tabs` skill (ALL | per-backbone tabs with counts).
3. **Multi-column sortable experiment table** with columns: `exp_num | backbone | description | composite | test_sharpe | val_sharpe | n_pos_folds | status | timestamp`. Click any header to sort asc/desc; second click reverses.
4. **Regex / substring filter box** — filter rows by description, citations, or config.
5. **Drill-down detail panel** — click a row to open: the reasoning annotation (all 7 fields), per-fold val and test Sharpe table, per-fold classification metrics (Precision/Recall/F1/F2/MCC), per-fold uncertainty (aleatoric/epistemic/confidence), trade-log link.
6. **Per-fold tables** — separate train / val / test tabs (default = test) with the 7-fold breakdown.
7. **Reasoning detail view** — the 7 fields (`diagnosis`, `citations`, `hypothesis`, `prediction`, `verdict`, `learning`, `_manual`) rendered with markdown formatting; citations clickable to arxiv.org.
8. **Champion lineage strip** (optional but recommended) — a small horizontal chain showing the sequence of champions over time.
9. **Audit links** — for each champion, link to the 14-section audit report and the Colab notebook.

### Data sources (all client-side fetched)

- `experiment_log.jsonl` — append-only per-experiment metrics.
- `best_config.json` — global champion.
- `reasoning_annotations.json` — per-experiment 7-field annotations.
- Optional: `experiment_summary.md`, `research_journal.md`, `medium_article.md`.

### Engineering invariants

- **Static HTML + vanilla JS** (no build step, no React/Vue) so the dashboard works directly off the file system and from GitHub Pages.
- **Idempotent renders** — refresh shows the latest state without server.
- **URL hash state** — active tab, sort column, filter string are preserved on reload (`#tab=lstm&sort=composite_desc&q=residual`).
- **No server dependency** — anyone can `open file://` and have a working dashboard.

### Navigation rules (cross-task ↔ per-task)

- **Cross-task dashboard row click → per-task dashboard in a NEW BROWSER TAB.** Not a modal, not a new window, not in-place navigation. Implementation: `<a href="…" target="_blank" rel="noopener">`.
- **Per-task experiment row click → inline detail panel** in the same dashboard (not a new tab). Implementation: vanilla-JS click handler that toggles a `<div class="detail-drawer">` sibling beneath the row.
- These two rules are different on purpose: the cross-task → per-task hop is a "go investigate" navigation (preserve the leaderboard for back-reference); the per-task → experiment-detail hop is a "drill in without losing place" navigation.

### Markdown artefact link rule

All markdown artefacts (`summary.md`, `journal.md`, `paper.md`, `CLAUDE.md`, `forensic_audit.md`, `checkpoint.md`) MUST route through an in-browser markdown viewer:

```html
<a href="md_viewer.html?path=research_journal.md" target="_blank" rel="noopener">Research Journal</a>
```

NOT a direct link like `<a href="research_journal.md">`. Reason: Chromium-family browsers DOWNLOAD `.md` files instead of rendering them — the direct link produces a "file saved" notification instead of a viewable page. `md_viewer.html` is a one-file dashboard component that reads `?path=…`, fetches the file, and renders via marked.js / CommonMark client-side.

### Task-description disclosure (about-block)

Per-task dashboards MUST include a collapsible "About this task" `<details open>` block near the top, BEFORE the sticky champion summary. See the dedicated skill `task-description-disclosure` for the full schema (source URL, metadata grid, backbones explored, problem-type description, DSBench baseline + delta, link to CLAUDE.md via md_viewer, link to skill pack).

### Train / val / test exposure in the detail panel

The per-experiment detail panel renders metrics with the following exposure rules:

- **Train metrics:** always shown for every experiment.
- **Val metrics:** always shown for every experiment.
- **Test metrics:** ONLY shown for the global champion experiment, sourced from `autoresearch_results/final_report.json`. NEVER show per-experiment test scores — the test set is touched ONCE per task per the autoresearch protocol (see `data-integrity-rules`).

## Anti-patterns

- **Server-side rendering** (Flask/Django dashboard). Adds a deploy surface; the JSONL/HTML model is enough.
- **Build-step dependencies** (npm install + webpack). Future maintainers can't open the dashboard standalone.
- **Default view is "ALL" but sorted by timestamp.** The user wants the champion at the top — sort by composite desc.
- **Reasoning panel below the fold.** It's the institutional-memory artifact; keep it close to the row click.
- **Filter without regex** — substring-only filter on a 500-experiment log is too coarse.

## Implementation checklist

1. Single file `dashboard.html` < 2000 lines including embedded CSS + JS.
2. Fetch JSONL/JSON via `fetch()` relative paths; render on `DOMContentLoaded`.
3. Sticky champion summary at top of `<body>`.
4. Backbone tab bar derived from JSONL distinct backbones.
5. Sortable table with click-header handlers.
6. Regex filter input wired with a debounce.
7. Row click opens a detail drawer; ESC or X closes.
8. URL hash sync for tab + sort + filter.
9. Mobile-responsive single-column collapse for small screens.

## References

- Source: `autoresearch/CLAUDE.md` section "Dashboard Reasoning Annotations" (panel content).
- Source: `autoresearch/CLAUDE.md` section "Dashboard Backbone Tabs" (tab strip).
- Source: `autoresearch/CLAUDE.md` section "Architecture" (dashboard decoupled from runner).
- Source: `autoresearchindexspy/autoresearchspy/CLAUDE.md` champion summary block (sticky summary motivation).
- Related: `dashboard-backbone-tabs`, `dashboard-reasoning-annotations`, `dashboard-files-update-mandate`, `github-pages-dashboard-sync`.
