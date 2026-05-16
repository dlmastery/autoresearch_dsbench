# DSBench AutoResearch — Engineering Documentation

> A chapter-by-chapter mapping of *Software Engineering at Google: Lessons Learned from Programming Over Time* (Winters, Manshreck, Wright, O'Reilly 2020) onto the DSBench autoresearch project.
> Last reviewed: 2026-05-16. Pinned to commit on `main`.

## Reading this docs/

This documentation is structured as **25 chapters across 4 parts plus four appendices**, mirroring the *Software Engineering at Google* (henceforth **SWE-book**) table of contents. Every chapter cites the SWE-book parallel in its opening section so a reader who knows the book recognises the mapping instantly.

The DSBench project (Jing et al. 2025 ICLR *DSBench: How Far Are Data Analysis Agents from Becoming Data Analysis Experts* arXiv:2409.07703) is treated as 112 independent Kaggle-style benchmarks (74 modeling + 38 analysis). We solve them with an LLM-driven, citation-disciplined Karpathy-style hill-climb wrapped in a 4-layer audit gate. This project is, to use the SWE-book's framing, **software engineering for ML experiment loops integrated over collaborator turns** — and that framing drives the chapter mapping.

### Project snapshot (cited throughout)

| Metric | Value |
|---|---|
| Tasks | **112** (74 modeling + 38 analysis) |
| Beat DSBench baseline | **82 / 112** (73 %) |
| Forensic-audit PASS | **112 / 112** |
| Skill-pack section coverage | **148 / 148** (100 %) |
| Lessons-Learned table rows | **26** |
| Sub-skills in `autoresearch-pack` | **44** |
| Experiments logged | **~14,000** |

## Reading order

You can read this docs/ end-to-end (~80,000 words) or use the four common entry points below.

1. **30-minute onboarding.** Read [Part I](part_1_thesis/01_what_is_autoresearch_engineering.md), [chapter 8](part_3_processes/08_style_guides_and_rules.md) on the project style guide, then [chapter 11](part_3_processes/11_testing_overview.md) on the 4-layer audit gate. That triple is the minimum context to read or review a commit.
2. **"Why is this so audit-heavy?"** Read [chapter 9](part_3_processes/09_code_review.md) (forensic committee), [chapter 11](part_3_processes/11_testing_overview.md) (testing pyramid), [chapter 20](part_4_tools/20_static_analysis.md) (validator), and any postmortem under [appendix A](appendix_a_postmortems/) — every audit hook was paid for by a real bug.
3. **"How do I add a backbone / task / skill?"** Read [chapter 8](part_3_processes/08_style_guides_and_rules.md), [chapter 15](part_3_processes/15_deprecation.md), [chapter 18](part_4_tools/18_build_systems.md), and [chapter 21](part_4_tools/21_dependency_management.md).
4. **"How does this compare to the SWE-book?"** Use the chapter map below.

## Chapter map — SWE-book chapter ↔ this repository

| Part | SWE-book chapter | DSBench parallel |
|---|---|---|
| I — Thesis | 1. *What Is Software Engineering?* | [01 What Is AutoResearch Engineering?](part_1_thesis/01_what_is_autoresearch_engineering.md) |
| II — Culture | 2. *How to Work Well on Teams* | [02 Working Well With Agents](part_2_culture/02_working_well_with_agents.md) |
| | 3. *Knowledge Sharing* | [03 Knowledge Sharing](part_2_culture/03_knowledge_sharing.md) |
| | 4. *Engineering for Equity* | [04 Engineering for Equity](part_2_culture/04_engineering_for_equity.md) |
| | 5. *How to Lead a Team* | [05 How to Lead an Agent Team](part_2_culture/05_how_to_lead_an_agent_team.md) |
| | 6. *Leading at Scale* | [06 Leading at Scale](part_2_culture/06_leading_at_scale.md) |
| | 7. *Measuring Engineering Productivity* | [07 Measuring Engineering Productivity](part_2_culture/07_measuring_engineering_productivity.md) |
| III — Processes | 8. *Style Guides and Rules* | [08 Style Guides and Rules](part_3_processes/08_style_guides_and_rules.md) |
| | 9. *Code Review* | [09 Code Review](part_3_processes/09_code_review.md) |
| | 10. *Documentation* | [10 Documentation](part_3_processes/10_documentation.md) |
| | 11. *Testing Overview* | [11 Testing Overview](part_3_processes/11_testing_overview.md) |
| | 12. *Unit Testing* | [12 Unit Testing](part_3_processes/12_unit_testing.md) |
| | 13. *Test Doubles* | [13 Test Doubles](part_3_processes/13_test_doubles.md) |
| | 14. *Larger Testing* | [14 Larger Testing](part_3_processes/14_larger_testing.md) |
| | 15. *Deprecation* | [15 Deprecation](part_3_processes/15_deprecation.md) |
| IV — Tools | 16. *Version Control and Branch Management* | [16 Version Control and Branches](part_4_tools/16_version_control_and_branches.md) |
| | 17. *Code Search* | [17 Code Search](part_4_tools/17_code_search.md) |
| | 18. *Build Systems and Build Philosophy* | [18 Build Systems](part_4_tools/18_build_systems.md) |
| | 19. *Critique: Google's Code Review Tool* | [19 Critique-Equivalent Code Review Tool](part_4_tools/19_critique_code_review_tool.md) |
| | 20. *Static Analysis* | [20 Static Analysis](part_4_tools/20_static_analysis.md) |
| | 21. *Dependency Management* | [21 Dependency Management](part_4_tools/21_dependency_management.md) |
| | 22. *Large-Scale Changes* | [22 Large-Scale Changes](part_4_tools/22_large_scale_changes.md) |
| | 23. *Continuous Integration* | [23 Continuous Integration](part_4_tools/23_continuous_integration.md) |
| | 24. *Continuous Delivery* | [24 Continuous Delivery](part_4_tools/24_continuous_delivery.md) |
| | 25. *Compute as a Service* | [25 Compute as a Service](part_4_tools/25_compute_as_a_service.md) |

### Appendices

- [Appendix A — Postmortems](appendix_a_postmortems/) — five real incidents in Five-Whys + Action-Items format.
- [Appendix B — Architectural Decision Records](appendix_b_adrs/) — fifteen ADRs in Michael Nygard format.
- [Appendix C — API Reference](appendix_c_api_reference/) — per-module documentation for the shared `framework/` library plus the CLI and glossary.
- [Appendix D — Diagrams](appendix_d_diagrams/) — Mermaid source for five canonical diagrams referenced throughout the chapters.

## Named principles canonised here

The SWE-book formalises a handful of principles that recur in every chapter (Hyrum's Law, the Beyoncé Rule, the Three Laws of Optimization). This documentation does the same for the DSBench project. The principles below are introduced in their home chapter and cited everywhere they apply.

| Principle | Home chapter | Statement |
|---|---|---|
| **Test-Set Embargo Rule** | [Ch. 11](part_3_processes/11_testing_overview.md) | If the test set is read once, it leaks once. The only legal reader is `framework/final_report.py`. |
| **Six-Field Annotation Rule** | [Ch. 10](part_3_processes/10_documentation.md) | Every experiment annotation carries six fields: diagnosis, citations, hypothesis, prediction, verdict, learning. No `_manual: true` ⇒ no commit. |
| **Four-Layer Gate Rule** | [Ch. 11](part_3_processes/11_testing_overview.md), [Ch. 23](part_4_tools/23_continuous_integration.md) | No commit changes experiment state without all four audit layers green: validator, forensic committee, 14-section explainability, skill-pack coverage. |
| **One-Knob Rule** | [Ch. 8](part_3_processes/08_style_guides_and_rules.md) | Every hill-climb experiment changes exactly one config knob and cites at least one paper. |
| **Per-Backbone 25-Experiment Mandate** | [Ch. 8](part_3_processes/08_style_guides_and_rules.md) | Every backbone gets a full 25-iteration exploration even if axes "look exhausted" earlier. |
| **Citation-Rigor Rule** | [Ch. 10](part_3_processes/10_documentation.md) | Every citation must carry Author1, Author2, ... YEAR VENUE 'Title' (arXiv:XXXX.XXXXX) + one-sentence relevance note. Parenthetical-only tags are insufficient. |
| **Checkpoint-After-Every-Experiment Rule** | [Ch. 16](part_4_tools/16_version_control_and_branches.md) | The next experiment's exact PowerShell command must be in the checkpoint *before* the previous experiment's results are read. |
| **No-Future-Sections Rule** | [Ch. 10](part_3_processes/10_documentation.md) | Documentation never describes state that hasn't been measured. Numbers come from running code, not estimation. |

## What is *not* in this docs/

- **No "SRE workbook" content.** This project is single-operator, batch, offline. We do not run SLOs, on-call rotations, or postmortems for production incidents. The five entries in Appendix A are *engineering* postmortems — they explain bugs in our code, not outages.
- **No marketing language.** Numbers are cited (BEAT 82/112, FORENSIC PASS 112/112, COVERAGE 148/148). When a number isn't measured, we say so.
- **No fanciful roadmap.** The roadmap belongs in [Ch. 22](part_4_tools/22_large_scale_changes.md) (large-scale-change tooling) and any individual chapter's "follow-up review" section. There is no separate roadmap document.

## How to cite this project

See [`appendix_c_api_reference/glossary.md`](appendix_c_api_reference/glossary.md) for the full citation list (~30 papers). The project itself is unpublished work by Evi Janti (`eranti@gmail.com`), MIT-licensed, mirrored at <https://github.com/dlmastery/autoresearch_dsbench>.
