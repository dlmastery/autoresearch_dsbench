# Chapter 3 — Knowledge Sharing

> *Parallel to:* SWE-book Chapter 3 *"Knowledge Sharing"* (Winters, Manshreck, Wright 2020).

**Thesis.** A project's knowledge is everything it knows about its own failures. Knowledge that lives only in one collaborator's head is one stack-overflow refresh away from being lost. The DSBench project's knowledge lives in three machine-readable surfaces: per-task `CLAUDE.md` files (the *operational* protocol), the `autoresearch-pack` skill bundle (the *industry-shareable* protocol), and Appendix A / Appendix B of this docs/ (the *narrative* protocol). All three are append-only.

## 3.1 The two failure modes of knowledge

The SWE-book chapter 3 starts by naming two ways knowledge dies in a software team:

1. **Tribal knowledge:** the answer is in one engineer's head; they leave the team and the answer is gone.
2. **Stale documentation:** the answer is in the docs but the docs lag the code, so nobody trusts the docs.

Autoresearch has a third failure mode the SWE-book doesn't address:

3. **Per-session amnesia:** the collaborator's working memory dies at session end. Everything the collaborator learned in the last session is gone unless it was written down.

The mitigations for all three failure modes are the same: **make the knowledge text, make the text machine-checkable, and make the check fail loudly when the knowledge is missing**.

## 3.2 The three knowledge surfaces

### 3.2.1 Per-task CLAUDE.md (operational)

The 112 per-task `CLAUDE.md` files are clones of `framework/CLAUDE_template.md` with task-specific parameter substitutions (slug, problem-type, kind, metric, backbones, baseline). Every file:

- Has the same 36+ required sections (see `framework/SECTION_MAPPING.md`).
- Is verified by `framework/validator.py` to contain those sections.
- Carries a task-specific Lessons-Learned table that the generator can append to without disrupting the audit.
- Names the protocol the human-Claude pair will follow for this task.

The CLAUDE.md is the *runtime* knowledge — what the collaborator reads on session start to know what to do. It is not industry-shareable verbatim because it carries financial-project artefacts (Sharpe ratios, regime gates) that don't apply to a CV task.

### 3.2.2 The `autoresearch-pack` skill bundle (industry-shareable)

`skills/autoresearch-pack/` decomposes the monolithic CLAUDE.md into **44 atomic, self-contained skills** plus one composite umbrella skill plus an audit script. Each skill has YAML frontmatter (trigger phrases, related skills), preserves the verbatim text from the source CLAUDE.md, and is independently loadable into a Claude Code session via the Skill tool.

The pack is designed for two audiences:

- **Claude Code users** — install by copying to `.claude/skills/`. Each skill auto-detects when it's relevant via trigger phrases.
- **Non-Claude-Code humans** — every SKILL.md is a self-contained Markdown protocol document. A teammate can read the directory as a protocol manual.

Coverage: **148/148 H2/H3 sections** across the three source files (`autoresearch/CLAUDE.md` — the FX project; `autoresearchindexspy/.../CLAUDE.md` — the SPY adaptation; `dsbench/framework/CLAUDE_template.md` — this project) map to ≥ 1 SKILL.md. Verified by `skills/autoresearch-pack/audit/audit_pack.py`. The audit is Layer 4 of the audit gate ([Ch. 11](../part_3_processes/11_testing_overview.md)).

The skills span 5 categories:

| Category | Count | Examples |
|---|---|---|
| protocol | 10 | `session-startup`, `crash-recovery-checkpoint`, `karpathy-agent-protocol`, `seven-step-research-process`. |
| engineering | 7 | `per-backbone-sota-recipes`, `gpu-memory-constraint`, `heteroscedastic-loss`, `three-stream-feature-engineering`, `stacked-ensemble-design`. |
| documentation | 8 | `mlops-documentation`, `citation-rigor`, `reasoning-blob-completeness`, `winner-archive-protocol`, `google-colab-notebook`, `committee-resumption-pointers`. |
| verification | 9 | `explainability-audit-14-section`, `traditional-ml-metrics`, `per-sample-decision-logging`, `validation-checklist`, `forensic-audit-pipeline`, `sub-period-robustness-audit`, `problem-type-aware-audit-thresholds`. |
| dashboard | 5 | `dashboard-reasoning-annotations`, `dashboard-backbone-tabs`, `dashboard-files-update-mandate`, `github-pages-dashboard-sync`, `interactive-dashboard-design`. |
| corrections (from DSBench Lessons) | 5 | `metric-sign-convention`, `extended-hill-climb-phase`, `regression-early-stopping-discipline`, `qa-task-feature-engineering`, `small-n-stride-split`, `cross-task-pooling-discipline`, `task-description-disclosure`. |

(Counts sum to 44 distinct sub-skills; some skills extend earlier ones.)

### 3.2.3 Appendix A / Appendix B (narrative)

The five postmortems in [Appendix A](../appendix_a_postmortems/) and the fifteen ADRs in [Appendix B](../appendix_b_adrs/) are the *narrative* knowledge surface. They give the why behind the what. A new team member who reads [postmortem 0001](../appendix_a_postmortems/0001_regression_delta_sign_bug.md) understands not just that we negate RMSE inside `_score`, but *why we had to*, and what it cost us to learn.

The ADRs are in Michael Nygard format (context, decision, consequences). The postmortems are in Five Whys + Action Items format. Both formats are append-only — never edit an ADR or postmortem after it's been committed; supersede it with a new one.

## 3.3 Why three surfaces, not one

The temptation is to keep all the knowledge in one giant `CLAUDE.md` and be done. We have tried this; it does not scale. The three-surface split exists because the three surfaces serve different readers at different times:

| Surface | Reader | When | Latency budget |
|---|---|---|---|
| CLAUDE.md | Claude Code at session start | Every session | ~ 1 minute (must fit in context) |
| Skill pack | Claude Code mid-session, when a sub-protocol becomes relevant | Per relevant trigger | ~ 1 second (one skill at a time) |
| Appendix A/B | Human or Claude doing a deep-dive | Once per debug session or design review | ~ 10 minutes |

Putting all three surfaces into one document would either (a) blow the context budget at session start, or (b) be too coarse to load on a trigger. The three-surface split is the same pattern the SWE-book describes for Google's documentation: the README is short, the design doc is long, the codelab is interactive.

## 3.4 The Citation-Rigor Rule

The SWE-book chapter 3 emphasises that good documentation cites primary sources. Our equivalent is canonised as the **Citation-Rigor Rule**:

> Every reasoning annotation includes at least one citation in the canonical format `Author1, Author2, ... YEAR VENUE 'Paper Title' (arXiv:XXXX.XXXXX) — one-sentence relevance note`. Parenthetical-only tags such as `(Keskar2017)` are insufficient. The `citation-rigor` skill polices the format.

The rule has teeth: it is the contract between the experiment ledger (which records *what* changed) and the rationale (which records *why*). Without it, the log becomes a grid search transcript and stops being autoresearch.

Examples used across the codebase:

- Chen, Guestrin 2016 KDD *XGBoost: A Scalable Tree Boosting System* arXiv:1603.02754 — anchors the gradient-boosted-tree axis.
- Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS *LightGBM: A Highly Efficient Gradient Boosting Decision Tree* arXiv:1711.05101 — leaf-wise GOSS sampling.
- Loshchilov, Hutter 2019 ICLR *Decoupled Weight Decay Regularization* arXiv:1711.05101 — AdamW anchor for the MLP / FT-Transformer backbones.
- Bishop 2006 *Pattern Recognition and Machine Learning* PRML §1.3, §5.5.2 — exchangeability and early-stopping discipline.
- Kohavi 1995 IJCAI *A Study of Cross-Validation and Bootstrap* — k-fold discipline; the seed-variance protocol cites this.
- Wolpert 1992 Neural Networks *Stacked Generalization* — motivates the `prior_ensemble` backend in the qa_excel pipeline.
- Friedman 2001 *Greedy Function Approximation: A Gradient Boosting Machine* — stochastic gradient boosting; the depth × lr trade-off cite.
- Guo, Pleiss, Sun, Weinberger 2017 ICML *On Calibration of Modern Neural Networks* arXiv:1706.04599 — temperature scaling for the excel-agent softmax.

The full citation list lives in [`appendix_c_api_reference/glossary.md`](../appendix_c_api_reference/glossary.md).

## 3.5 The committee-resumption pointer

A specific SWE-book pattern that the project adopts: every long-running document carries an explicit *resumption pointer* — a "if you read only one paragraph, read this" callout near the top. The per-task `CLAUDE.md` resumption pointer says:

> Beat DSBench: \<count\>/\<total\>. Forensic PASS: \<count\>/\<total\>. Champion of champions: \<task\> · \<backbone\> · composite \<value\>. Resume in one command: `python framework/_status.py`. Cross-task dashboard: <http://localhost:8765/dashboard/index.html>.

The pointer is intentionally not auto-substituted in the template — placeholders are LITERAL, so the file never claims state it hasn't measured. The substitution happens during `_refresh_dashboards.py` after a real measurement run. The `committee-resumption-pointers` skill codifies the pattern.

This is the same pattern the SWE-book recommends for design docs ("if you only read one paragraph, here's what this proposes"). We just enforce it through a template substitution rather than relying on the author to write it.

## 3.6 What knowledge we deliberately do *not* share

Three categories of knowledge stay out of the public skill pack:

1. **Per-task champions.** The current best config for `titanic` is not industry knowledge; it's the output of running the protocol on that task. Champions live in `autoresearch_results/best_config.json` per task and in `registry/final_rollup.json` globally.
2. **The user's actual identity.** The pack credits Evi Janti / `eranti@gmail.com` as author of the protocol; it does not embed the human's session transcripts or personal context.
3. **The DSBench dataset itself.** The 38 Modeloff PDFs and the 74 Kaggle CSVs are not redistributed by this project; we link to the upstream `LiqiangJing/DSBench` repository instead.

## 3.7 The "Knowledge Sharing" health metric

How do we know knowledge is being shared and not lost? Four checks:

1. **Skill-pack coverage:** every CLAUDE.md H2/H3 maps to ≥ 1 SKILL.md. Target 100 %. Current: 148 / 148.
2. **Lessons-Learned row count growth:** rows are added when corrections happen; if a session has corrections but no new row, the lesson is being lost. Current: 26 rows.
3. **Appendix A postmortem cadence:** every significant bug gets a postmortem; if a bug is fixed silently, the knowledge is being lost. Current: 5 postmortems.
4. **Citation count growth:** every new paper that influences an experiment is added to the glossary. If experiments cite without the glossary growing, the knowledge surface is being amputated.

The checks run as Layer 4 of the audit gate ([Ch. 23](../part_4_tools/23_continuous_integration.md)).

## 3.8 Related

- [Ch. 8 — Style Guides and Rules](../part_3_processes/08_style_guides_and_rules.md): the CLAUDE.md as the project style guide.
- [Ch. 10 — Documentation](../part_3_processes/10_documentation.md): the Six-Field Annotation Rule.
- [Appendix C — API Reference](../appendix_c_api_reference/): the per-module reference docs.
- [`skills/autoresearch-pack/README.md`](../../skills/autoresearch-pack/README.md): the skill-pack installation guide.
