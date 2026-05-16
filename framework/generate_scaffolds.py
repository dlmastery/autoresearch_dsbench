"""Generate per-task autoresearch repos.

For each row of registry/modeling_tasks.json and registry/analysis_tasks.json,
create a self-contained directory under dsbench/modeling/<slug>/ or
dsbench/analysis/<slug>/ that mirrors the autoresearch repo layout. The
CLAUDE.md is rendered from `framework/CLAUDE_template.md` with task-specific
parameters substituted in; the validator (framework/validator.py) verifies
every section listed in framework/SECTION_MAPPING.md survives the substitution.
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FRAMEWORK = ROOT / "framework"
TEMPLATE = (FRAMEWORK / "CLAUDE_template.md").read_text(encoding="utf-8")
DASHBOARD_TPL = (FRAMEWORK / "dashboard_template.html").read_text(encoding="utf-8")
SOTA = (FRAMEWORK / "sota_catalog.yaml").read_text(encoding="utf-8")


PROBLEM_TO_BACKBONES = {
    "classification_binary":
        ["xgboost", "lightgbm", "catboost", "mlp", "ft_transformer"],
    "classification_multiclass":
        ["xgboost", "lightgbm", "catboost", "mlp", "ft_transformer"],
    "regression":
        ["xgboost", "lightgbm", "catboost", "mlp", "ft_transformer"],
    "structured":
        ["mlp", "ft_transformer", "xgboost"],
    "qa_excel":
        ["excel_agent"],
}
PROBLEM_TO_METRIC = {
    "classification_binary": "roc_auc",
    "classification_multiclass": "macro_f1",
    "regression": "rmse",
    "structured": "accuracy",
    "qa_excel": "exact_match_accuracy",
}
DSBENCH_BASELINE = {
    "classification_binary": 0.50,
    "classification_multiclass": 0.34,
    "regression": -1.0,    # placeholder; actual depends on task
    "structured": 0.50,
    "qa_excel": 0.3412,    # DSBench paper: best agent 34.12% on data analysis
}


def render_claude(task: dict, port: int, repo_dir: Path) -> str:
    backbones = PROBLEM_TO_BACKBONES.get(task["problem_type"], ["xgboost"])
    subs = {
        "{{task_name}}": task["name"],
        "{{task_slug}}": task["slug"],
        "{{kind}}": task["kind"],
        "{{problem_type}}": task["problem_type"],
        "{{task_type}}": task["task_type"],
        "{{metric}}": PROBLEM_TO_METRIC.get(task["problem_type"], "accuracy"),
        "{{iterations_per_backbone}}": "25",
        "{{backbone_order}}": " → ".join(backbones),
        "{{primary_backbone}}": backbones[0],
        "{{dashboard_port}}": str(port),
        "{{repo_dir}}": str(repo_dir).replace("\\", "/"),
    }
    out = TEMPLATE
    for k, v in subs.items():
        out = out.replace(k, v)
    return out


def render_dashboard(task: dict) -> str:
    subs = {
        "{{task_name}}": task["name"],
        "{{task_type}}": task["task_type"],
        "{{problem_type}}": task["problem_type"],
        "{{iterations_per_backbone}}": "25",
    }
    out = DASHBOARD_TPL
    for k, v in subs.items():
        out = out.replace(k, v)
    return out


def seed_reasoning(task: dict) -> dict:
    bb = PROBLEM_TO_BACKBONES.get(task["problem_type"], ["xgboost"])[0]
    return {
        "task": task["slug"],
        "problem_type": task["problem_type"],
        "primary_backbone": bb,
        "first_experiment": {
            "backbone": bb,
            "diagnosis": (
                f"Fresh autoresearch run on {task['name']} — no champion exists. "
                f"Anchor the {bb}-phase 25-iter cycle with the sota_catalog default config so the "
                f"subsequent iterations can perturb individual axes (depth/lr/regularisation/seeds) "
                f"from a known-good starting point. Per autoresearch CLAUDE.md research-driven "
                f"selection, exploration must start with the SOTA literature default before "
                f"venturing into bold changes."
            ),
            "citations": (
                "Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' "
                "(arXiv:1603.02754) — establishes the 2nd-order Newton boosting default tabular SOTA; "
                "Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — "
                "neural-baseline AdamW recipe."
            ),
            "hypothesis": (
                f"The default sota_catalog config for {bb} should land in the middle of the Kaggle "
                f"distribution for tasks of this size/type. The composite metric "
                f"(min(val,train) - 0.05*|gap|) penalises overfit baselines; if the gap is wide, the "
                f"next iter will tighten regularisation."
            ),
            "prediction": (
                f"Composite in [0.55, 0.85] for classification_binary; for regression the score is "
                f"negated RMSE so target around [-1.5, -0.3]."
            ),
        },
    }


def build_repo_files(task: dict, repo: Path, port: int) -> None:
    repo.mkdir(parents=True, exist_ok=True)
    (repo / "memory").mkdir(exist_ok=True)
    (repo / "data").mkdir(exist_ok=True)
    (repo / "autoresearch_results").mkdir(exist_ok=True)
    (repo / "autoresearch_results" / "trade_logs").mkdir(exist_ok=True)
    (repo / "autoresearch_results" / "winners").mkdir(exist_ok=True)
    (repo / "code_versions").mkdir(exist_ok=True)
    (repo / ".data_cache").mkdir(exist_ok=True)

    (repo / "CLAUDE.md").write_text(render_claude(task, port, repo), encoding="utf-8")

    tc = {
        "name": task["name"],
        "slug": task["slug"],
        "kind": task["kind"],
        "problem_type": task["problem_type"],
        "task_type": task["task_type"],
        "metric": PROBLEM_TO_METRIC.get(task["problem_type"], "accuracy"),
        "iterations_per_backbone": 25,
        "backbones": PROBLEM_TO_BACKBONES.get(task["problem_type"], ["xgboost"]),
        "dsbench_baseline": DSBENCH_BASELINE.get(task["problem_type"], 0.5),
    }
    (repo / "task_config.json").write_text(json.dumps(tc, indent=2), encoding="utf-8")
    (repo / "seed_reasoning.json").write_text(json.dumps(seed_reasoning(task), indent=2), encoding="utf-8")

    # README
    readme = (
        f"# {task['name']} · DSBench autoresearch\n\n"
        f"**Kind:** {task['kind']} · **Problem:** {task['problem_type']} · "
        f"**Task type:** {task['task_type']}\n\n"
        f"DSBench source: {task.get('url', 'n/a')}\n\n"
        f"## Quick start\n\n"
        f"```powershell\n"
        f"# Run a single hill-climb backbone (25 iters)\n"
        f"& \"C:/Users/evija/anaconda3/python.exe\" -m framework.hill_climb --repo \"{repo}\" --backbone xgboost\n\n"
        f"# Run the full multi-backbone loop\n"
        f"& \"C:/Users/evija/anaconda3/python.exe\" -m framework.hill_climb --repo \"{repo}\"\n\n"
        f"# Audit this repo against autoresearch SECTION_MAPPING\n"
        f"& \"C:/Users/evija/anaconda3/python.exe\" -m framework.validator --repo \"{repo}\"\n"
        f"```\n\n"
        f"## DSBench comparison target\n\n"
        f"The DSBench paper reports the best agent achieving 34.12% on data-analysis tasks and "
        f"34.74% Relative Performance Gap on data-modeling. The final score for this task is "
        f"written to `autoresearch_results/final_report.json` after one test-set pass.\n\n"
        f"## Architecture\n\n"
        f"Generated from `framework/CLAUDE_template.md` (parameterised clone of "
        f"`autoresearch/CLAUDE.md`). See `CLAUDE.md` for the full 36-section protocol applied to "
        f"this task.\n"
    )
    (repo / "README.md").write_text(readme, encoding="utf-8")

    # paper_abstract
    abstract = (
        f"# Abstract — autoresearch on {task['name']}\n\n"
        f"We apply the autoresearch protocol (Karpathy 2024, dlmastery/autoresearch 2026) to the "
        f"DSBench `{task['name']}` benchmark ({task['problem_type']} on {task['task_type']} data). "
        f"The protocol drives 25 hill-climbing iterations per SOTA backbone "
        f"({', '.join(PROBLEM_TO_BACKBONES.get(task['problem_type'], ['xgboost']))}), each cited to "
        f"the relevant 2024-2026 arXiv paper, with train/val-only selection (test set held back "
        f"for the final DSBench comparison report). The champion composite metric is "
        f"`min(val, train) - 0.05*|val - train|` to penalise overfit. The target is to meet or "
        f"beat the DSBench paper's best-agent baselines on the test set.\n"
    )
    (repo / "paper_abstract.md").write_text(abstract, encoding="utf-8")

    # paper.md skeleton (sections will be filled by the loop as experiments accrue)
    paper = (
        f"# AutoResearch on {task['name']} — Paper\n\n"
        f"## 1. Introduction\n\nDSBench `{task['name']}` is a {task['problem_type']} benchmark on "
        f"{task['task_type']} data; see {task.get('url', '')}. We apply the autoresearch loop with "
        f"per-backbone 25-iter hill climbing, arXiv-cited reasoning per experiment, and a frozen "
        f"test split touched only by `framework/final_report.py`.\n\n"
        f"## 2. Method\n\n2.1 **Composite metric:** `min(val_score, train_score) - 0.05 * abs(val_score - train_score)`. "
        f"This penalises overfit by 5 cents per absolute gap unit.\n\n"
        f"2.2 **Backbone catalog:** "
        f"{', '.join(PROBLEM_TO_BACKBONES.get(task['problem_type'], ['xgboost']))}. Each backbone "
        f"starts from `framework/sota_catalog.yaml` defaults and is hill-climbed for 25 iters with "
        f"arXiv-cited perturbations (see `autoresearch_results/research_journal.md`).\n\n"
        f"2.3 **Train/val/test split:** 70/15/15 with seed 42, recorded in "
        f"`data/split_manifest.json`. Hashes are verified at every runner start.\n\n"
        f"## 3. Hill-Climb Trajectory\n\nSee `autoresearch_results/experiment_summary.md` for the "
        f"per-experiment table and `autoresearch_results/research_journal.md` for diagnosis / "
        f"hypothesis / verdict narratives.\n\n"
        f"## 4. Final DSBench Comparison\n\nSee `autoresearch_results/final_report.json` after "
        f"`framework/final_report.py` runs the one-and-only test-set pass.\n\n"
        f"## References\n\nSee `autoresearch_results/reasoning_annotations.json` for the full "
        f"per-experiment citation table.\n"
    )
    (repo / "paper.md").write_text(paper, encoding="utf-8")

    # memory checkpoint — initial state
    ckpt = (
        f"# Project autoresearch checkpoint — {task['name']}\n\n"
        f"## Current champion\n\n"
        f"None — repo just initialised. Next experiment is **Exp1** "
        f"({PROBLEM_TO_BACKBONES.get(task['problem_type'], ['xgboost'])[0]} iter 1/25).\n\n"
        f"## Next experiment command\n\n"
        f"```powershell\n"
        f"& \"C:/Users/evija/anaconda3/python.exe\" -m framework.hill_climb --repo \"{repo}\"\n"
        f"```\n\n"
        f"## Experiment history\n\n_(empty)_\n"
    )
    (repo / "memory" / "project_autoresearch_checkpoint.md").write_text(ckpt, encoding="utf-8")

    # autoresearch_results scaffolding
    (repo / "autoresearch_results" / "experiment_log.jsonl").write_text("", encoding="utf-8")
    (repo / "autoresearch_results" / "reasoning_annotations.json").write_text("{}", encoding="utf-8")
    (repo / "autoresearch_results" / "experiment_summary.md").write_text(
        f"# Experiment Summary — {task['name']}\n\n_(populated by `framework/hill_climb.py`)_\n",
        encoding="utf-8",
    )
    (repo / "autoresearch_results" / "research_journal.md").write_text(
        f"# Research Journal — {task['name']}\n\n_(populated by `framework/hill_climb.py`)_\n",
        encoding="utf-8",
    )
    (repo / "autoresearch_results" / "dashboard.html").write_text(render_dashboard(task), encoding="utf-8")

    # Stub data/splits.py — generic ML split with seed=42 (synthetic by default).
    (repo / "data" / "splits.py").write_text(
        '"""Stub splits.py — runner generates 70/15/15 with seed=42 the first time it runs."""\n'
        'TRAIN_FRAC, VAL_FRAC, TEST_FRAC, SEED = 0.70, 0.15, 0.15, 42\n',
        encoding="utf-8",
    )
    (repo / "data" / "features.py").write_text(
        '"""Stub features.py — synthetic features are generated by framework/runner.py."""\n',
        encoding="utf-8",
    )

    # run_autoresearch.py — thin wrapper to framework.runner
    (repo / "run_autoresearch.py").write_text(
        "import os, sys, json\n"
        "from pathlib import Path\n"
        "ROOT = Path(__file__).resolve()\n"
        "sys.path.insert(0, str(ROOT.parents[2]))\n"  # dsbench/
        "from framework.runner import main\n\n"
        "if __name__ == '__main__':\n"
        "    # Inject --repo if not provided so user can call: run_autoresearch.py --backbone xgboost --description ...\n"
        "    if '--repo' not in sys.argv:\n"
        "        sys.argv += ['--repo', str(Path(__file__).resolve().parent)]\n"
        "    main()\n",
        encoding="utf-8",
    )
    (repo / "hill_climb.py").write_text(
        "import sys\n"
        "from pathlib import Path\n"
        "ROOT = Path(__file__).resolve()\n"
        "sys.path.insert(0, str(ROOT.parents[2]))\n"
        "from framework.hill_climb import main\n\n"
        "if __name__ == '__main__':\n"
        "    if '--repo' not in sys.argv:\n"
        "        sys.argv += ['--repo', str(Path(__file__).resolve().parent)]\n"
        "    main()\n",
        encoding="utf-8",
    )
    (repo / "third_party_audit.py").write_text(
        "import sys\n"
        "from pathlib import Path\n"
        "ROOT = Path(__file__).resolve()\n"
        "sys.path.insert(0, str(ROOT.parents[2]))\n"
        "from framework.validator import main\n\n"
        "if __name__ == '__main__':\n"
        "    if '--repo' not in sys.argv:\n"
        "        sys.argv += ['--repo', str(Path(__file__).resolve().parent)]\n"
        "    main()\n",
        encoding="utf-8",
    )


def main() -> None:
    modeling = json.loads((ROOT / "registry" / "modeling_tasks.json").read_text(encoding="utf-8"))
    analysis = json.loads((ROOT / "registry" / "analysis_tasks.json").read_text(encoding="utf-8"))
    port = 8765
    n = 0
    for task in modeling:
        task["kind"] = "modeling"
        repo = ROOT / "modeling" / task["slug"]
        build_repo_files(task, repo, port=port)
        n += 1
    for task in analysis:
        task["kind"] = "analysis"
        repo = ROOT / "analysis" / task["slug"]
        build_repo_files(task, repo, port=port)
        n += 1
    print(f"[generator] wrote {n} task repos ({len(modeling)} modeling + {len(analysis)} analysis)")


if __name__ == "__main__":
    main()
