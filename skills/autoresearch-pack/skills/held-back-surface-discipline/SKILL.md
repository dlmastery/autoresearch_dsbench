---
name: held-back-surface-discipline
description: Held-back-surface discipline — generalises the autoresearch "test set is OFF-LIMITS until final_report" rule to any benchmark whose held-back surface is named differently. DSBench holds back `data/test/` (eval-after-search); DARE-bench inverts and holds back `data/train/` (eval-only mandate). The pattern is "one declared accessor, one frozen output artefact, one final touch." Triggers on "held-back surface", "eval-only", "DARE-bench inversion", "data/<surface>/-is-forbidden", "single-touch surface", "frozen accessor".
metadata:
  category: protocol
  source: dsbench + dare-bench
  related: [data-integrity-rules, train-val-test-invariants, forbidden-path-audit, forensic-audit-pipeline]
---

# Held-Back-Surface Discipline (one declared accessor, one frozen artefact)

## When to use

- Designing a new autoresearch benchmark that mandates a held-back evaluation surface.
- Adapting the dsbench protocol to a benchmark whose held-back surface is the TRAINING side (DARE-bench inversion).
- Auditing whether a project's runner code paths respect the held-back surface.

## The rule

> **The autoresearch loop's `data/test/`-is-forbidden rule generalises to `data/<held-back-surface>/`-is-forbidden.**
>
> Every autoresearch benchmark declares (in `task_config.json`):
>
> 1. **Which surface is held back** — `held_back_surface` in `{"test", "train", "eval", …}`.
> 2. **What tokens reference it** — `held_back_tokens` list (e.g. `["X_test", "y_test", "data/test/"]` for DSBench; `["X_train", "y_train", "data/train/"]` for DARE-bench).
> 3. **The single allowed accessor** — `final_accessor` (e.g. `framework/final_report.py` for DSBench; `framework/final_eval.py` for DARE-bench).
> 4. **The frozen output artefact** — `final_artefact` (e.g. `autoresearch_results/final_report.json`).
> 5. **The single-touch rule** — the accessor is invoked EXACTLY ONCE per task, AT THE END, and writes a frozen artefact. The hill-climb / search loop must not invoke it.
>
> The audit enforcement is `forbidden-path-audit` (forensic agent K). The protocol-level rule is THIS skill.

### Mode catalogue

| Benchmark mode | Held-back surface | Final accessor | Frozen output | Why |
|---|---|---|---|---|
| **DSBench (eval-after-search)** | `data/test/` | `framework/final_report.py` | `autoresearch_results/final_report.json` | The agent hill-climbs on train+val; the test set is the unbiased estimate of the agent's final quality, used exactly once for the DSBench comparison. |
| **DARE-bench (eval-only)** | `data/train/` | `framework/final_eval.py` | `autoresearch_results/final_eval.json` | The agent is given a pre-trained model and must evaluate it on a fixed eval surface; touching the train set during evaluation defeats the purpose of the benchmark. |
| **NeurIPS-style competition** | `private_test/` | `framework/submit.py` | `submission.jsonl` | The private test is server-side; the agent never sees it locally, but the protocol still names it. |
| **Walk-forward time-series** | `data/future/` (the next walk-forward step) | `framework/step_forward.py` | `walk_forward_log.jsonl` | Each step's "future" is held back from the model fitted on the prior steps. |

### Invariants (apply to every mode)

1. **One declared accessor.** Multiple accessors invite drift; one is the audit anchor.
2. **One frozen artefact.** The accessor's output is read-only post-creation; re-running the accessor on the same task is allowed but must produce the same artefact (deterministic seed, frozen config).
3. **Search loop blind.** The hill-climb / search loop has no code path to the held-back surface — verified by `forbidden-path-audit`.
4. **Final touch is logged.** The accessor logs to `experiment_log.jsonl` with a distinguishing `kind: "final"` flag so the dashboard can render the held-back-surface score in a separate row from the search-loop iterations.
5. **No back-channel.** No artefact derived from the held-back surface (statistics, summaries, even sample counts beyond what's published in `task_config.json`) leaks back into the search loop.

### Concrete DSBench pattern

```python
# task_config.json
{
  "held_back_surface": "test",
  "held_back_tokens": ["X_test", "y_test", "splits['X_test']", "splits['y_test']", "data/test/", "test_loader"],
  "final_accessor": "framework/final_report.py",
  "final_artefact": "autoresearch_results/final_report.json"
}
```

The hill-climb loop touches `train + val` only. After 125-325 iters complete, `framework/final_report.py` runs ONCE, refits the champion (per the `winner-archive-protocol` refit rule), scores `data/test/`, writes `final_report.json` with the DSBench comparison.

### Concrete DARE-bench inversion

```python
# task_config.json
{
  "held_back_surface": "train",
  "held_back_tokens": ["X_train", "y_train", "splits['X_train']", "splits['y_train']", "data/train/", "train_loader"],
  "final_accessor": "framework/final_eval.py",
  "final_artefact": "autoresearch_results/final_eval.json"
}
```

The eval-only loop reads `data/eval/` and the pre-trained model checkpoint; the training data is forbidden until `framework/final_eval.py` performs the official reference-fit check.

## Anti-patterns

- **Hard-coding "test" everywhere** — the discipline must be parameterised by `held_back_surface`. A dsbench-only codebase will fail when re-pointed at dare-bench.
- **Two accessors** ("we have `final_report.py` AND `quick_test_check.py`") — pick one; `quick_test_check.py` is the leak.
- **Logging the held-back-surface score during the search loop** — the score may not enter the loop's decision function, even as a passive observation.
- **Caching a summary statistic of the held-back surface** (mean, std, class counts beyond what's in `task_config.json`) and using it during the search loop — back-channel leakage.
- **Re-running the accessor on every iter "to see how the loop is doing"** — single-touch means one. If you re-run, you've broken the invariant.
- **Not declaring the held-back surface in `task_config.json`** — the audit can't enforce a surface it doesn't know about.

## Implementation checklist

1. Every `task_config.json` declares `held_back_surface`, `held_back_tokens`, `final_accessor`, `final_artefact`.
2. The accessor is the ONLY file that imports / references the held-back surface; verified by `forbidden-path-audit`.
3. The accessor is invoked exactly once per task; the dashboard / status script flags multi-touch.
4. The frozen artefact is checksummed; re-runs must reproduce the checksum.
5. The search loop's logging schema includes `kind: "search"` (vs `kind: "final"` for the accessor) so the dashboard can separate them.
6. The protocol doc (CLAUDE.md) explicitly names the held-back surface in the "Hard Rules → Data Integrity" section.

## References

- DSBench source: `framework/CLAUDE_template.md` "Hard Rules → Data Integrity" — the original `data/test/`-is-forbidden rule.
- DARE-bench source: the eval-only mandate (the inversion).
- Kapoor & Narayanan 2023 Patterns 'Leakage and the Reproducibility Crisis in ML-based Science' (arXiv:2207.07048) — taxonomy of test-set leakage.
- Recht, Roelofs, Schmidt, Shankar 2019 ICML 'Do ImageNet Classifiers Generalize to ImageNet?' (arXiv:1902.10811) — the cost of a leaky held-back surface.
- Related: `data-integrity-rules`, `train-val-test-invariants`, `forbidden-path-audit`, `forensic-audit-pipeline`.
