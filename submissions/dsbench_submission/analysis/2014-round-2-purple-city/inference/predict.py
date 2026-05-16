"""Standalone inference for 2014-round-2-purple-city champion.

Usage:
    python predict.py

The model is re-trained from scratch on the train split because the
synthetic-data harness ships only the *config* of the champion (no
checkpoint), since synthetic data is regenerated deterministically on each
runner start (seed=42). For real-data submissions replace this with a
pickled model_checkpoint.pkl + sklearn / xgboost loader.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]  # repo root
sys.path.insert(0, str(ROOT))
from framework.runner import TaskConfig, load_or_make_data, _fit_predict


def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    cfg = TaskConfig.load(repo)
    champion = json.loads((repo / "autoresearch_results" / "best_config.json").read_text(encoding="utf-8"))
    splits = load_or_make_data(repo, cfg)
    pred_val, proba_val = _fit_predict(
        champion["backbone"], champion.get("params", {}),
        splits["X_train"], splits["y_train"],
        splits["X_val"], cfg.problem_type,
    )
    print("backbone:   " + str(champion["backbone"]))
    print("composite:  " + f"{champion['composite']:.4f}")
    print("val score:  " + f"{champion['val_score']:.4f}")
    try:
        first = pred_val[:10].tolist()
    except AttributeError:
        first = list(pred_val)[:10]
    print("first 10 predictions: " + str(first))


if __name__ == "__main__":
    main()
