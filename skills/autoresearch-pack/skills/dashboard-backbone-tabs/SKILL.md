---
name: dashboard-backbone-tabs
description: Dashboard backbone tab bar — render an ALL/per-backbone tab strip above the experiment list to filter by architecture family. Triggers on "backbone tabs", "dashboard tabs", "filter by backbone", "tab strip".
metadata:
  category: dashboard
  source: autoresearch
  related: [interactive-dashboard-design, dashboard-reasoning-annotations, dashboard-files-update-mandate]
---

# Dashboard Backbone Tabs

## When to use

- Designing the dashboard layout for a project with multiple backbones.
- Adding a new backbone — wire it into the tab bar.
- Users want to focus on one architecture family at a time without re-filtering.

## The rule

> ### Dashboard Backbone Tabs
>
> Dashboard (`dashboard.html`) renders a backbone tab bar above the experiment list. Default view shows "ALL". Tabs filter the scrollable experiment list to just that backbone's experiments. Click to switch.

### Practical layout (derived from the autoresearch dashboard)

- Tab strip sits **above** the experiment table and **below** the global metrics (champion composite, total experiments).
- Tabs in order: `ALL | mlp | lstm | patchtst | patchtsmixer | xgboost | lightgbm | catboost | <new>`.
- Active tab is visually distinct (bold + colored background).
- Click toggles filter; click again on "ALL" clears.
- The filter is purely client-side JS on the JSONL — no server round-trip.

## Anti-patterns

- **Hard-coded backbone list in HTML.** New backbones get forgotten. Derive the tab list from `experiment_log.jsonl` distinct values.
- **Tab default = first backbone alphabetically.** Default should be `ALL` so the user sees the lineage.
- **Tab filter that hides reasoning panel** — keep the reasoning panel visible regardless of filter.
- **No URL anchor for active tab.** Bookmarks and shared links should preserve the filter (`#tab=lstm`).
- **Backbone counts not shown.** Render `lstm (44)` so users see exploration depth at a glance.

## Implementation checklist

1. Derive backbone list from `experiment_log.jsonl` distinct `backbone` values.
2. Tab strip with `ALL` first, then backbones in insertion order.
3. JavaScript filter on the experiment table rows.
4. URL hash sync (`#tab=patchtst`).
5. Counts in parentheses next to each tab.

## References

- Source: `autoresearch/CLAUDE.md` section "Dashboard Backbone Tabs"
- Source: `autoresearchindexspy/autoresearchspy/CLAUDE.md` section "Dashboard Backbone Tabs"
- Related: `interactive-dashboard-design`, `dashboard-reasoning-annotations`, `dashboard-files-update-mandate`.
