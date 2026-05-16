# Appendix D — Diagrams

> Five canonical Mermaid diagrams referenced throughout the chapters. Each diagram is also embedded inline in its primary chapter.

This appendix is the standalone home of the project's five Mermaid diagrams. Each `.mmd` file is GitHub-Mermaid-renderable (open the file directly to view) and is also embedded inline in the chapter that describes the structure it illustrates.

## Diagrams

### 1. [`repo_topology.mmd`](repo_topology.mmd)

The top-level dataflow across `framework/`, `modeling/`, `analysis/`, `skills/`, `submissions/`, `dashboard/`, and `registry/`. The diagram is the canonical answer to "where does this script's output go". The arrows are directed; the consumer of each artefact is on the arrow's target end.

**Read alongside:** [Ch. 18 — Build Systems](../part_4_tools/18_build_systems.md) (the build-graph chapter) and [Ch. 1 — What Is AutoResearch Engineering?](../part_1_thesis/01_what_is_autoresearch_engineering.md) (the elevator pitch).

### 2. [`per_experiment_lifecycle.mmd`](per_experiment_lifecycle.mmd)

The sequence-diagram form of one experiment: Claude pre-writes the 4-field annotation, `hill_climb.py` invokes `runner.run_one`, the runner pins to P-cores, loads cached data, fits on TRAIN, scores on VAL, computes the composite, appends to the log, updates `best_config.json` if a champion. Then Claude post-writes verdict + learning and checkpoints.

**Read alongside:** [Ch. 14 — Larger Testing](../part_3_processes/14_larger_testing.md) (the experiment as the unit of larger testing), [Ch. 25 — Compute as a Service](../part_4_tools/25_compute_as_a_service.md) (the P-core pinning detail).

### 3. [`four_layer_audit_gate.mmd`](four_layer_audit_gate.mmd)

The control flow of the four-layer audit gate: Layer 1 (validator section coverage + X_test grep) → Layer 2 (10-agent forensic committee) → Layer 3 (14-section explainability) → Layer 4 (skill-pack coverage). A FAIL at any layer routes back to "fix"; only after every layer is green does the commit reach GREEN.

**Read alongside:** [Ch. 11 — Testing Overview](../part_3_processes/11_testing_overview.md) (the pyramid framing), [Ch. 23 — Continuous Integration](../part_4_tools/23_continuous_integration.md) (the gate as CI).

### 4. [`per_task_split.mmd`](per_task_split.mmd)

The 70 / 15 / 15 split with a "TEST OFF-LIMITS" stamp on the test slice. The diagram makes the Test-Set Embargo Rule visible: train + val feed `runner.run_one` and `hill_climb.py`; test feeds *only* `final_report.py`, exactly once per task.

**Read alongside:** [Ch. 11 — Testing Overview](../part_3_processes/11_testing_overview.md) (the Test-Set Embargo), [Ch. 4 — Engineering for Equity](../part_2_culture/04_engineering_for_equity.md) (the split as a fairness choice), [ADR 0002](../appendix_b_adrs/0002_train_val_only_for_hill_climb.md) and [ADR 0007](../appendix_b_adrs/0007_stride5_interleaved_split_for_qa.md).

### 5. [`ten_agent_forensic_committee.mmd`](ten_agent_forensic_committee.mmd)

The committee structure: agents A (split-hash), B (target leakage), C (row overlap), D (distribution shift), E (anomaly), F (static-code), G (temporal order), H (seed stability), I (refit consistency), J (backbone diversity) feed into agent Z, which aggregates into a PASS / FAIL / PASS_WITH_WARN verdict written to `forensic_audit.md`, `forensic_audit.json`, and `registry/forensic_summary.json`.

**Read alongside:** [Ch. 9 — Code Review](../part_3_processes/09_code_review.md) (the committee as code review), [Ch. 19 — Critique-Equivalent Code Review Tool](../part_4_tools/19_critique_code_review_tool.md) (`forensic_audit.md` as our Critique), [ADR 0004](../appendix_b_adrs/0004_10_agent_forensic_committee.md).

## How to view

GitHub renders `.mmd` files natively. To view locally:

- Open the file in any editor that supports Mermaid (VS Code with Mermaid plugin, Obsidian, Typora).
- Or paste the file's contents into <https://mermaid.live>.
- Or render via `mmdc` (mermaid CLI) into PNG / SVG.

## Diagram authoring conventions

- All Mermaid blocks open with `mermaid` (lowercase) for GitHub native rendering.
- Node IDs are uppercase short codes; node labels include line breaks via `<br/>` for legibility.
- Solid arrows are data flow; dashed arrows are control flow.
- The TEST node in `per_task_split.mmd` carries the red-bordered "TEST OFF-LIMITS" styling to make the Test-Set Embargo immediately visible.
- The committee diagram clusters agents by concern (Split / Feature / Model / Code) before they feed agent Z.
