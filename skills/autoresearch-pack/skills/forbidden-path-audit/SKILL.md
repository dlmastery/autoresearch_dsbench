---
name: forbidden-path-audit
description: Forbidden-path access audit — a forensic agent (agent K) that grep-scans the runner / hill-climb codebase for any reference to a held-back data surface (e.g. `data/test/`, `data/eval/`, or — under the DARE-bench inversion — `data/train/`) and FAILS if found. Generalises the dsbench rule "test set is OFF-LIMITS until the final report run" to any benchmark whose held-back surface is named differently. Triggers on "forbidden path", "off-limits surface", "agent K", "held-back grep", "DARE-bench inversion", "eval-only mandate", "test path leak".
metadata:
  category: verification
  source: dsbench + dare-bench
  related: [forensic-audit-pipeline, data-integrity-rules, held-back-surface-discipline, train-val-test-invariants]
---

# Forbidden-Path Access Audit (forensic agent K — held-back grep)

## When to use

- Any autoresearch project where ONE data surface is held back from the hill-climbing loop and may only be touched by a final-report script.
- DSBench: `data/test/` is forbidden; `framework/final_report.py` is the only path that may read it.
- DARE-bench: `data/train/` is forbidden during the eval-only loop; `framework/final_eval.py` is the only path that may read it (the inversion).
- Generally: any benchmark whose protocol defines a single "evaluation-anchor" surface that the iterative loop must NOT see.

## The rule

> **Agent K — forbidden-path access enforcer (forensic audit committee, dare-bench inversion-aware)**
>
> Every champion is policed by a static-code grep over `run_autoresearch.py`, `hill_climb.py`, and every module under the project's runner / search package, for references to the held-back surface. The reference list is parameterised:
>
> | Benchmark mode | Held-back surface | Forbidden tokens (case-sensitive) | Single allowed accessor |
> |---|---|---|---|
> | DSBench (default) | `data/test/` | `X_test`, `y_test`, `splits['test']`, `data/test/`, `test_loader` | `framework/final_report.py` |
> | DARE-bench (inversion) | `data/train/` | `X_train`, `y_train`, `splits['train']`, `data/train/`, `train_loader` | `framework/final_eval.py` |
> | Any custom benchmark | `<held_back_surface>` | declared in `task_config.json:held_back_tokens` | declared in `task_config.json:final_accessor` |
>
> Agent K reads `task_config.json:held_back_surface` to pick the right token set; defaults to the DSBench token set if the key is absent. Any positive grep outside the declared accessor is a FAIL.
>
> The corresponding skill `held-back-surface-discipline` documents the protocol-level invariant; this skill documents the enforcement.

### Construction pattern

1. **Parameterise the held-back tokens** in `task_config.json`:
   ```json
   {
     "held_back_surface": "test",
     "held_back_tokens": ["X_test", "y_test", "splits['test']", "data/test/", "test_loader"],
     "final_accessor": "framework/final_report.py"
   }
   ```
   For DARE-bench eval-only tasks, the same key set inverts (`"held_back_surface": "train"`, tokens reference train, accessor is `final_eval.py`).
2. **Grep every runner file** for every forbidden token. Comments inside `framework/final_report.py` / `framework/final_eval.py` are exempt.
3. **Treat ANY positive grep as FAIL.** Even a commented-out reference is forbidden — the comment was once code, and may be re-uncommented.
4. **Wire into the audit committee.** Agent K runs first in `framework/forensic_audit.py`; a FAIL blocks all downstream agents (no point auditing leakage when the held-back surface is being read).
5. **Cross-check the section-coverage validator.** `framework/validator.py` performs the same grep as a quick sanity check; agent K is the authoritative enforcement.

### Why it matters — DSBench example

The DSBench protocol holds out `data/test/` for the SINGLE comparison run that reports the agent's score. Any hill-climbing code that reads the test set inflates the reported score, breaks the comparison's validity, and disqualifies the submission. Agent K + the validator together guarantee that the only path to `X_test` / `y_test` is `framework/final_report.py`, ONCE per task.

### Why it matters — DARE-bench inversion

DARE-bench inverts the protocol: the eval set is provided up-front, and the agent is forbidden from re-training on the train set during evaluation. The held-back surface is `data/train/`, and the same enforcement pattern applies with inverted tokens. The skill `held-back-surface-discipline` documents the protocol-level rule; agent K is the enforcement mechanism that generalises across both modes.

## Anti-patterns

- **Hard-coded `X_test` / `y_test` token list** — only catches DSBench's idioms; misses DARE-bench's train-side inversion and any custom benchmark. Parameterise.
- **Whitelisting `final_report.py` AND `extended_hill_climb.py`** — anything beyond the single declared accessor is suspect; require exactly one allowed reader.
- **Skipping comments in the grep** — commented-out `# X_test = ...` lines re-emerge as live code on the next refactor.
- **Running agent K only on the final winner** — every iter that touches the held-back surface poisons the loop; grep on every commit.
- **Not blocking the runner on a positive grep** — the audit must FAIL the experiment, not warn and proceed.

## Implementation checklist

1. `task_config.json` declares `held_back_surface`, `held_back_tokens`, `final_accessor`.
2. `framework/forensic_audit.py` includes an agent K that reads those keys and greps the runner package.
3. Agent K runs FIRST in the committee; a FAIL aborts subsequent agents and the experiment.
4. `framework/validator.py` shares the same grep logic as a fast pre-flight gate.
5. CI / commit hooks: any commit changing runner files runs agent K before push.
6. The single allowed accessor (`final_report.py` or `final_eval.py`) is invoked at most ONCE per task and writes its result to a frozen artefact (`final_report.json` / `final_eval.json`).

## References

- DSBench source: `C:/Users/evija/dsbench/framework/CLAUDE_template.md` section "Hard Rules → Data Integrity" and "Auditing & Forensics → Layer 1 / Layer 2".
- DARE-bench source: the eval-only mandate (held-back train surface; documented in `held-back-surface-discipline`).
- Conceptual lineage: Kapoor & Narayanan 2023 'Leakage and the Reproducibility Crisis in ML-based Science' Patterns (arXiv:2207.07048) — static-code grep as a defence against accidental leakage.
- Related: `forensic-audit-pipeline`, `data-integrity-rules`, `held-back-surface-discipline`, `train-val-test-invariants`.
