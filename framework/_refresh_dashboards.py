"""Re-render the per-task dashboard.html for every task using the rich
autoresearch-style template (framework/dashboard_template.html).

Substitutes per-task metadata loaded from task_config.json + the registry
(registry/modeling_tasks.json or registry/analysis_tasks.json) so the
"About this task" dropdown is populated with real values.
"""
from __future__ import annotations
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TPL = (ROOT / "framework" / "dashboard_template.html").read_text(encoding="utf-8")


# ----- problem-type-specific "What this task tests" copy -----
PROBLEM_TYPE_BLURB = {
    "classification_binary": (
        "Binary classification on tabular data (e.g. fraud detection, churn). "
        "Evaluated via ROC-AUC. SOTA backbones explored: GBMs "
        "(XGBoost / LightGBM / CatBoost), MLP, FT-Transformer."
    ),
    "classification_multiclass": (
        "Multiclass classification on tabular / structured data. "
        "Evaluated via macro-F1 + accuracy. SOTA backbones: GBMs "
        "(XGBoost / LightGBM / CatBoost), MLP, FT-Transformer."
    ),
    "regression": (
        "Tabular / NLP regression. Evaluated via RMSE (negated so higher = better). "
        "SOTA backbones: GBMs, MLP residual, PatchTSMixer for sequence-like inputs."
    ),
    "structured": (
        "Structured-prediction task (sequence / image / time-series). "
        "Evaluated via the task-specific metric. SOTA backbones: GBMs, MLP, "
        "specialised sequence/vision models where applicable."
    ),
    "qa_excel": (
        "Modeloff financial-modelling QA. Multiple-choice (A-I) and numeric "
        "answers over Excel files. Per autoresearch-style hill climb we use a "
        "learned answer-prior classifier (LogReg / KNN / NaiveBayes / global prior) — "
        "see `_DIAGNOSIS.md` for the ceiling analysis."
    ),
}


def _load_registry() -> dict:
    """Return {slug: registry_record} merged across modeling + analysis."""
    out: dict = {}
    for p in (ROOT / "registry" / "modeling_tasks.json",
              ROOT / "registry" / "analysis_tasks.json"):
        if not p.exists():
            continue
        for rec in json.loads(p.read_text(encoding="utf-8")):
            slug = rec.get("slug") or rec.get("name")
            if slug:
                out[slug] = rec
    return out


REGISTRY = _load_registry()


def _h(value) -> str:
    """HTML-escape a scalar value, returning '?' for None/blank."""
    if value is None or value == "":
        return "?"
    return html.escape(str(value))


def _metadata_rows(task: dict, reg: dict) -> str:
    """Build the per-task <table> rows for the dropdown."""
    rows: list[tuple[str, str]] = []
    kind = task.get("kind", "modeling")
    if kind == "modeling":
        rows = [
            ("name", task.get("name")),
            ("slug", task.get("slug")),
            ("kind", task.get("kind")),
            ("problem_type", task.get("problem_type")),
            ("task_type", task.get("task_type")),
            ("metric", task.get("metric")),
            ("year", reg.get("year")),
            ("dataset size (MB)", reg.get("size_mb")),
            ("iterations / backbone", task.get("iterations_per_backbone")),
        ]
    else:  # analysis
        rows = [
            ("name", task.get("name")),
            ("slug", task.get("slug")),
            ("challenge_id", reg.get("challenge_id")),
            ("year", reg.get("year")),
            ("n_questions", reg.get("n_questions")),
            ("n_answers", reg.get("n_answers")),
            ("problem_type", task.get("problem_type")),
            ("metric", task.get("metric")),
            ("iterations / backbone", task.get("iterations_per_backbone")),
        ]
    return "".join(
        f"<tr><td>{_h(k)}</td><td>{_h(v)}</td></tr>" for k, v in rows
    )


def _backbones_chips(task: dict) -> str:
    bbs = task.get("backbones") or []
    if not bbs:
        return '<span style="color:#8b949e">none recorded</span>'
    return "".join(f'<span class="bb-pill">{_h(b)}</span>' for b in bbs)


def _dsbench_baseline_line(task: dict) -> str:
    baseline = task.get("dsbench_baseline")
    metric = task.get("metric", "score")
    if baseline is None:
        return '<span style="color:#8b949e">no baseline recorded</span>'
    return f'<b>{_h(baseline)}</b> &nbsp;<span style="color:#8b949e">({_h(metric)})</span>'


def _url_label(reg: dict) -> str:
    url = reg.get("url", "")
    if "kaggle.com" in url:
        return "Kaggle competition"
    if "eloquens.com" in url:
        return "Eloquens / Modeloff challenge"
    return "task source"


def render_dashboard(task: dict, reg: dict) -> str:
    pt = task.get("problem_type", "")
    subs = {
        "{{task_name}}": _h(task.get("name", "")),
        "{{task_type}}": _h(task.get("task_type", "")),
        "{{problem_type}}": _h(pt),
        "{{iterations_per_backbone}}": _h(task.get("iterations_per_backbone", 25)),
        "{{kind}}": _h(task.get("kind", "modeling")),
        "{{slug}}": _h(task.get("slug", task.get("name", ""))),
        "{{task_url}}": _h(reg.get("url", "")) if reg.get("url") else "#",
        "{{task_url_label}}": _h(_url_label(reg)),
        "{{metadata_rows}}": _metadata_rows(task, reg),
        "{{backbones_chips}}": _backbones_chips(task),
        "{{task_description}}": html.escape(
            PROBLEM_TYPE_BLURB.get(pt, "Custom task — see CLAUDE.md.")
        ),
        "{{dsbench_baseline_line}}": _dsbench_baseline_line(task),
    }
    out = TPL
    for k, v in subs.items():
        out = out.replace(k, v)
    return out


def main() -> None:
    n = 0
    for root in (ROOT / "modeling", ROOT / "analysis"):
        if not root.exists():
            continue
        for child in sorted(root.iterdir()):
            cfg_p = child / "task_config.json"
            if not cfg_p.exists():
                continue
            cfg = json.loads(cfg_p.read_text(encoding="utf-8"))
            slug = cfg.get("slug") or cfg.get("name") or child.name
            reg = REGISTRY.get(slug, {})
            html_out = render_dashboard(cfg, reg)
            out_p = child / "autoresearch_results" / "dashboard.html"
            out_p.parent.mkdir(parents=True, exist_ok=True)
            out_p.write_text(html_out, encoding="utf-8")
            n += 1
    print(f"[refresh] rewrote {n} per-task dashboards with the rich template")


if __name__ == "__main__":
    main()
