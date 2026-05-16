"""Build clean per-task registry from DSBench raw data files."""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_MODELING = ROOT / "_modeling_data.json"
RAW_ANALYSIS = ROOT / "_analysis_data.json"
OUT_MODELING = ROOT / "registry" / "modeling_tasks.json"
OUT_ANALYSIS = ROOT / "registry" / "analysis_tasks.json"


def _slug(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9_-]+", "-", s.strip().lower())
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:80]


def _infer_task_type(name: str) -> str:
    n = name.lower()
    if any(k in n for k in ("nlp", "essay", "feedback", "text", "tweet", "sentence",
                            "phrase", "language", "quest", "patent", "lmsys",
                            "commonlit", "readability")):
        return "nlp"
    if any(k in n for k in ("covid", "forecasting", "demand", "time-series",
                            "ion-switching", "ventilator")):
        return "time_series"
    if any(k in n for k in ("game-of-life",)):
        return "structured"
    if any(k in n for k in ("titanic", "satisfaction", "safe-driver", "fraud",
                            "malware", "spaceship", "tabular", "playground",
                            "cat-in", "instant", "transaction-prediction",
                            "value-prediction", "click", "bike", "box-office",
                            "dont-overfit", "value")):
        return "tabular"
    return "tabular"


def _infer_problem_type(name: str) -> str:
    n = name.lower()
    if "regression" in n or "value-prediction" in n or "demand" in n or \
            "box-office" in n or "ventilator" in n or "essay-scoring" in n:
        return "regression"
    if "covid" in n:
        return "regression"
    if "ion-switching" in n:
        return "classification_multiclass"
    if "tweet-sentiment-extraction" in n or "patent" in n or \
            "feedback" in n or "commonlit" in n or "quest" in n or "lmsys" in n:
        return "regression"
    if "game-of-life" in n:
        return "structured"
    return "classification_binary"


def _parse_size_mb(size: str) -> float:
    m = re.match(r"([\d.]+)\s*([kKmMgG])?B", size.replace(",", ""))
    if not m:
        return 0.0
    val = float(m.group(1))
    unit = (m.group(2) or "").lower()
    return {"k": val / 1024, "m": val, "g": val * 1024}.get(unit, val)


def build_modeling() -> list[dict]:
    tasks: list[dict] = []
    for line in RAW_MODELING.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line:
            continue
        raw = json.loads(line)
        name = raw["name"]
        tasks.append({
            "id": f"m{len(tasks)+1:03d}",
            "name": name,
            "slug": _slug(name),
            "url": raw["url"],
            "size_mb": _parse_size_mb(raw["size"]),
            "year": raw["year"],
            "task_type": _infer_task_type(name),
            "problem_type": _infer_problem_type(name),
            "kind": "modeling",
        })
    return tasks


def build_analysis() -> list[dict]:
    tasks: list[dict] = []
    for line in RAW_ANALYSIS.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line:
            continue
        raw = json.loads(line)
        questions = raw.get("questions", [])
        answers = raw.get("answers", [])
        tasks.append({
            "id": f"a{len(tasks)+1:03d}",
            "challenge_id": raw["id"],
            "name": raw["name"],
            "slug": _slug(raw["name"]),
            "url": raw["url"],
            "n_questions": len(questions),
            "n_answers": len(answers),
            "year": raw["year"],
            "task_type": "financial_modeling_excel",
            "problem_type": "qa_excel",
            "kind": "analysis",
        })
    return tasks


def main() -> None:
    modeling = build_modeling()
    analysis = build_analysis()
    OUT_MODELING.parent.mkdir(parents=True, exist_ok=True)
    OUT_MODELING.write_text(json.dumps(modeling, indent=2), encoding="utf-8")
    OUT_ANALYSIS.write_text(json.dumps(analysis, indent=2), encoding="utf-8")
    print(f"[registry] wrote {len(modeling)} modeling tasks -> {OUT_MODELING}")
    print(f"[registry] wrote {len(analysis)} analysis tasks -> {OUT_ANALYSIS}")
    # type distribution
    from collections import Counter
    print("[modeling problem-type]", Counter(t["problem_type"] for t in modeling))
    print("[modeling task-type]", Counter(t["task_type"] for t in modeling))


if __name__ == "__main__":
    main()
