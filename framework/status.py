"""Quick status check across all task repos."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    rows = []
    for root in (ROOT / "modeling", ROOT / "analysis"):
        for child in sorted(root.iterdir()):
            if not (child / "task_config.json").exists():
                continue
            log = child / "autoresearch_results" / "experiment_log.jsonl"
            n = sum(1 for _ in log.read_text(encoding="utf-8").splitlines() if _.strip()) if log.exists() else 0
            best = -float("inf")
            bb = ""
            bc = child / "autoresearch_results" / "best_config.json"
            if bc.exists():
                try:
                    cfg = json.loads(bc.read_text(encoding="utf-8"))
                    best = cfg.get("composite", best)
                    bb = cfg.get("backbone", "")
                except Exception:
                    pass
            final = child / "autoresearch_results" / "final_report.json"
            test_score = ""
            beats = ""
            if final.exists():
                try:
                    f = json.loads(final.read_text(encoding="utf-8"))
                    test_score = f"{f.get('test_score', 0):.4f}"
                    beats = "BEAT" if f.get("beats_dsbench") else "miss"
                except Exception:
                    pass
            rows.append({"task": child.name, "kind": root.name, "n_exp": n,
                         "champion_bb": bb,
                         "champion_composite": f"{best:.4f}" if best != -float('inf') else '',
                         "test": test_score, "vs_dsbench": beats})
    # ascii table
    print(f"{'task':45s} {'kind':10s} {'n_exp':>6s} {'champ_bb':>15s} {'comp':>8s} {'test':>8s} {'dsb':>5s}")
    print("-" * 110)
    n_total = len(rows)
    n_started = sum(1 for r in rows if r["n_exp"] > 0)
    n_complete = sum(1 for r in rows if r["n_exp"] >= 125)
    n_test = sum(1 for r in rows if r["test"])
    n_beat = sum(1 for r in rows if r["vs_dsbench"] == "BEAT")
    for r in rows:
        if r["n_exp"] > 0:
            print(f"{r['task'][:45]:45s} {r['kind']:10s} {r['n_exp']:>6d} {r['champion_bb']:>15s} "
                  f"{r['champion_composite']:>8s} {r['test']:>8s} {r['vs_dsbench']:>5s}")
    print("-" * 110)
    print(f"total={n_total} started={n_started} complete>=125={n_complete} "
          f"final_test={n_test} beat_dsbench={n_beat}")


if __name__ == "__main__":
    main()
