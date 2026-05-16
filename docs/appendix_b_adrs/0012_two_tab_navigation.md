# ADR-0012: Cross-task = new-tab; per-task = inline drawer

## Status

Accepted (2026-05-15). Lessons 9 and 25 in `framework/CLAUDE_template.md`.

## Context

The cross-task leaderboard (`dashboard/index.html`) shows one row per task. The per-task dashboard (`modeling/<slug>/autoresearch_results/dashboard.html`) shows one row per experiment. Both have a "row click" action — but the right behaviour differs:

- **Cross-task row click** = "go to that task's full dashboard". This is a navigation jump; the user wants to leave the leaderboard and read the task's full ledger.
- **Per-task row click** = "show me the details of this experiment". This is a drill-down; the user wants to read the reasoning annotation and the per-fold metrics without leaving the experiment table.

Implementing both as the same action (e.g., always a modal, always navigation) confuses one of the two flows.

## Decision

**Two-tab contract:**

1. **Cross-task → per-task** opens in a **new browser tab**.

   ```html
   <a href="modeling/titanic/autoresearch_results/dashboard.html" target="_blank" rel="noopener">titanic</a>
   ```

   No modals, no in-place navigation, no JS `window.location.assign`. The cross-task leaderboard stays open in the original tab so the user can drill into multiple tasks side-by-side.

2. **Per-task row click** opens an **inline detail panel** (drawer) within the same dashboard.

   ```javascript
   row.addEventListener("click", (e) => {
     const drawer = row.querySelector(".detail-drawer");
     drawer.classList.toggle("open");
   });
   ```

   The drawer is a sibling `<div class="detail-drawer">` beneath the row; it expands to show the reasoning annotation, per-fold train/val metrics, and a link to the trade log. No tab is opened, no URL changes — the user can scroll back to the table immediately.

The asymmetry encodes a design intent: cross-task is a navigation surface, per-task is a drill-down surface.

## Consequences

**Easier:**

- Reviewers can open ten tasks at once and compare. No back-button thrash.
- Per-task drill-down is fast — no page reload to read an experiment's details.
- The pattern is enforced at the template level (`framework/dashboard_template.html` and `dashboard/index.html`).

**Harder:**

- A user expecting modal behaviour on the cross-task table is mildly surprised. Mitigated by the "About this task" affordance and a small `↗` icon next to each row indicating new-tab.
- The inline drawer requires careful CSS to handle ~325 experiment rows in the worst case. Mitigated by virtual-scrolling-light: only the visible rows have an inflated drawer; others are collapsed by default.

**Riskier:**

- Browsers can block `target="_blank"` opens if triggered by something other than a user click. The dashboards only use `target="_blank"` on `<a>` clicks, which browsers allow.

## Related

- [`0011_md_viewer_inline_render.md`](0011_md_viewer_inline_render.md)
- Skills `interactive-dashboard-design`, `dashboard-backbone-tabs`.
- `framework/dashboard_template.html`.
- `dashboard/index.html`.
