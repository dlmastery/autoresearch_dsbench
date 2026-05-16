"""Per-task forensic root-cause report for the 29 analysis tasks that miss
DSBench. For each missing task, decompose WHY we lost:

  R1 — answer absent from pool      (structurally unrecoverable)
  R2 — answer present but rare      (wrong-mode trap; oracle ceiling)
  R3 — multi-modal split            (tie in pool; predictor commits to wrong tie)
  R4 — predicted vs actual mismatch (predicted X, actual Y, gap = ?)
  R5 — val/test distribution drift  (val champion failed on test)

Writes:
  analysis/_LOSS_FORENSICS.md   (per-task narrative + summary table)
  analysis/_LOSS_FORENSICS.json (machine-readable per-task records)
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from framework.runner import (  # noqa: E402
    TaskConfig,
    load_or_make_data,
    _build_qa_global,
    _fit_predict,
)


def classify_loss(task_pool_letters: list[int], val_letters: list[int],
                  test_letters: list[int], pred_test: list[int]) -> dict:
    pool_set = set(task_pool_letters)
    test_in_pool = [t in pool_set for t in test_letters]
    pool_counter = Counter(task_pool_letters)
    test_counter = Counter(test_letters)
    pool_mode = pool_counter.most_common(1)[0][0] if pool_counter else -1
    test_mode = test_counter.most_common(1)[0][0] if test_counter else -1

    # Per-test-row classification
    rows = []
    for t, p, in_pool in zip(test_letters, pred_test, test_in_pool):
        if not in_pool:
            r = "R1_absent_from_pool"
        elif t == p:
            r = "R0_correct"
        elif pool_counter.get(t, 0) <= 1:
            r = "R2_rare_in_pool"
        elif len(pool_counter) > 1 and pool_counter[t] == pool_counter[pool_mode]:
            r = "R3_pool_tied_mode"
        else:
            r = "R4_mode_trap"
        rows.append({"actual": int(t), "predicted": int(p), "in_pool": bool(in_pool),
                     "pool_count_for_actual": int(pool_counter.get(t, 0)),
                     "pool_count_for_predicted": int(pool_counter.get(p, 0)),
                     "root_cause": r})

    # Headline reason for this task = most-common per-row reason
    reasons = Counter([r["root_cause"] for r in rows])
    headline = reasons.most_common(1)[0][0]

    return {
        "headline_reason": headline,
        "per_test_row_reasons": rows,
        "pool_size": len(task_pool_letters),
        "pool_letters_histogram": {int(k): int(v) for k, v in pool_counter.items()},
        "test_letters_histogram": {int(k): int(v) for k, v in test_counter.items()},
        "pool_mode": int(pool_mode),
        "test_mode": int(test_mode),
        "test_in_pool_count": int(sum(test_in_pool)),
        "test_total": len(test_letters),
        "test_accuracy_if_we_picked_pool_mode": float(
            sum(t == pool_mode for t in test_letters) / max(1, len(test_letters))
        ),
        "test_accuracy_if_we_picked_test_mode_oracle": float(
            sum(t == test_mode for t in test_letters) / max(1, len(test_letters))
        ),
    }


def process_task(repo: Path) -> dict:
    cfg = TaskConfig.load(repo)
    if cfg.problem_type != "qa_excel":
        return {"task": repo.name, "status": "skipped_not_qa"}
    fr = repo / "autoresearch_results" / "final_report.json"
    if not fr.exists():
        return {"task": repo.name, "status": "no_final_report"}
    final = json.loads(fr.read_text(encoding="utf-8"))
    if final.get("beats_dsbench"):
        return {"task": repo.name, "status": "won", "delta": final.get("delta_vs_dsbench")}
    bc = json.loads((repo / "autoresearch_results" / "best_config.json").read_text(encoding="utf-8"))

    splits = load_or_make_data(repo, cfg)
    # Refit champion to get the test predictions (NOTE: we read y_test here
    # solely to author the forensic report — this is the same operation
    # framework/final_report.py already does once per task).
    X_fit = np.concatenate([splits["X_train"], splits["X_val"]], axis=0)
    y_fit = np.concatenate([splits["y_train"], splits["y_val"]], axis=0)
    pred_te, _ = _fit_predict(bc["backbone"], bc.get("params", {}),
                              X_fit, y_fit, splits["X_test"], cfg.problem_type)

    task_pool = list(splits["y_train"]) + list(splits["y_val"])
    cls = classify_loss(task_pool, list(splits["y_val"]), list(splits["y_test"]),
                        [int(p) for p in pred_te])

    return {
        "task": repo.name,
        "status": "miss",
        "champion_backbone": bc.get("backbone"),
        "champion_params": bc.get("params", {}),
        "test_score": final.get("test_score"),
        "delta_vs_dsbench": final.get("delta_vs_dsbench"),
        **cls,
    }


def main():
    out_dir = ROOT / "analysis"
    decisions = []
    for child in sorted((ROOT / "analysis").iterdir()):
        if not (child / "task_config.json").exists():
            continue
        try:
            d = process_task(child)
        except Exception as exc:
            d = {"task": child.name, "status": "error", "error": str(exc)}
        decisions.append(d)

    (out_dir / "_LOSS_FORENSICS.json").write_text(json.dumps(decisions, indent=2), encoding="utf-8")

    misses = [d for d in decisions if d.get("status") == "miss"]
    wins = [d for d in decisions if d.get("status") == "won"]

    # Render markdown
    lines = []
    lines.append("# Per-task Loss Forensics — Analysis (29 misses)\n")
    lines.append(f"_Generated by `framework/_analysis_loss_forensics.py`. "
                 f"Final state: {len(wins)} wins, {len(misses)} misses across "
                 f"{len(decisions)} analysis tasks._\n")
    lines.append("## Root-cause taxonomy\n")
    lines.append("- **R0_correct** — predicted right (never the headline for a miss row)")
    lines.append("- **R1_absent_from_pool** — test letter never appears in train+val")
    lines.append("  → STRUCTURALLY UNRECOVERABLE without real Excel parsing")
    lines.append("- **R2_rare_in_pool** — test letter appears ≤ 1× in pool")
    lines.append("  → recoverable in principle but Bayes-optimal pool predictor "
                 "would never commit to it")
    lines.append("- **R3_pool_tied_mode** — test letter is tied with the modal letter "
                 "in the pool")
    lines.append("  → recoverable with the right tiebreaker (per-position prior, "
                 "challenge metadata, etc.)")
    lines.append("- **R4_mode_trap** — pool has a clear mode and our predictor "
                 "picked it; test answer is a non-modal in-pool letter")
    lines.append("  → recoverable only with per-question semantic understanding\n")

    # Headline summary
    by_headline = Counter(d["headline_reason"] for d in misses)
    lines.append("## Summary by headline reason\n")
    lines.append("| reason | count | recoverability |")
    lines.append("|---|---|---|")
    recoverable = {
        "R0_correct": "n/a",
        "R1_absent_from_pool": "no — structurally unrecoverable without real Excel",
        "R2_rare_in_pool": "no — Bayes-optimal pool predictor cannot commit to a rare letter",
        "R3_pool_tied_mode": "maybe — needs a tiebreaker not currently in the predictor",
        "R4_mode_trap": "no — requires semantic Q&A (GPT-4 + Excel parsing)",
    }
    for r, n in by_headline.most_common():
        lines.append(f"| `{r}` | {n} | {recoverable.get(r, 'unknown')} |")
    lines.append("")

    # Per-task narrative
    lines.append("## Per-task narrative (29 misses, sorted by recoverability then "
                 "by oracle-uplift)\n")
    miss_sorted = sorted(misses, key=lambda d: (
        d["headline_reason"] != "R3_pool_tied_mode",
        -d["test_accuracy_if_we_picked_test_mode_oracle"],
    ))
    for d in miss_sorted:
        lines.append(f"### {d['task']}\n")
        lines.append(f"- champion: `{d['champion_backbone']}` "
                     f"params=`{json.dumps(d['champion_params'])}`")
        lines.append(f"- test score: **{d['test_score']:.4f}** "
                     f"(Δ vs DSBench = {d['delta_vs_dsbench']:+.4f})")
        lines.append(f"- headline reason: **{d['headline_reason']}**")
        lines.append(f"- pool histogram: {d['pool_letters_histogram']}")
        lines.append(f"- test histogram: {d['test_letters_histogram']}")
        lines.append(f"- if we'd picked pool-mode: "
                     f"test_acc = {d['test_accuracy_if_we_picked_pool_mode']:.3f}")
        lines.append(f"- oracle-test-mode ceiling: "
                     f"test_acc = {d['test_accuracy_if_we_picked_test_mode_oracle']:.3f}")
        lines.append(f"- per-row reasons: " +
                     ", ".join([r["root_cause"] for r in d["per_test_row_reasons"]]))
        lines.append("")

    (out_dir / "_LOSS_FORENSICS.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"[loss-forensics] wrote {out_dir / '_LOSS_FORENSICS.md'} "
          f"({len(misses)} misses, {len(wins)} wins)")
    print()
    print("Headline reasons across the 29 misses:")
    for r, n in by_headline.most_common():
        print(f"  {n:3d}  {r}")


if __name__ == "__main__":
    main()
