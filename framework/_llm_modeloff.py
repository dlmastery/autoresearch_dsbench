"""LLM (or heuristic) Modeloff-source answerer for ``_excel_agent``.

This module is the runtime entry-point for ``backend=llm_modeloff``. It
implements two paths:

  Path A — Anthropic API. Active when ``ANTHROPIC_API_KEY`` is in the env.
    Sends the per-question source text (intro + question wording + workbook
    summary if available) to Claude, asks for a single-letter / numeric
    answer, parses the response.

  Path B — Offline structural-LLM heuristic. Active when no API key is set.
    Parses the multiple-choice options from the question file, scores each
    option against the question stem (and the workbook markdown if present)
    using token-overlap + heuristic financial-modelling cues, returns the
    best option letter. Falls back to the pool-mode (per-task training mode)
    when no MC options can be parsed.

Predictions are ALWAYS returned via the global ``LabelEncoder`` so the
runner's int-coded ``y_va`` arithmetic remains valid. Never reads
``_analysis_data.json:answers`` or ``splits['y_test']`` — only the source
material under ``analysis/<slug>/source/`` and the train pool labels (which
are train-pool only, not the test set).

Citations (per CLAUDE.md Citation Rigor):
  - Wei, Wang, Schuurmans, Bosma, Ichter, Xia, Chi, Le, Zhou 2022 NeurIPS
    'Chain-of-Thought Prompting Elicits Reasoning in Large Language Models'
    (arXiv:2201.11903) — motivates Path A's "think step by step then answer"
    template.
  - Brown, Mann, Ryder, Subbiah, Kaplan, Dhariwal, Neelakantan, Shyam,
    Sastry, Askell et al. 2020 NeurIPS 'Language Models are Few-Shot
    Learners' (arXiv:2005.14165) — supports the few-shot / single-shot
    template families in ``hill_climb.py:_excel_agent_proposals``.
  - Kojima, Gu, Reid, Matsuo, Iwasawa 2022 NeurIPS 'Large Language Models
    are Zero-Shot Reasoners' (arXiv:2205.11916) — backs the zero-shot
    "Let's think step by step" prefix.
  - Manning, Raghavan, Schütze 2008 Cambridge 'Introduction to Information
    Retrieval' Ch. 6 — TF-IDF / token-overlap is the heuristic backbone for
    Path B's scoring rule when no LLM is available.
"""
from __future__ import annotations

import functools
import os
import re
import time
from collections import Counter
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
SOURCE_CACHE: dict[str, dict] = {}


def has_api_key() -> bool:
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


# ---------------------------------------------------------------------------
# Source loading — reads ONLY analysis/<slug>/source/, NEVER answers
# ---------------------------------------------------------------------------
def _read_text_safe(p: Path) -> str:
    if not p.exists():
        return ""
    for enc in ("utf-8", "utf-8-sig", "latin-1", "cp1252"):
        try:
            return p.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    return p.read_bytes().decode("utf-8", errors="replace")


def load_source_for_slug(slug: str) -> dict:
    """Load intro + per-question files + (optional) excel markdown for a slug.

    Returns dict with keys ``intro``, ``questions`` (map question_name → text),
    ``excel`` (combined markdown), ``available`` (bool — at least intro+one Q).
    Cached on slug.
    """
    if slug in SOURCE_CACHE:
        return SOURCE_CACHE[slug]
    src = ROOT / "analysis" / slug / "source"
    intro = _read_text_safe(src / "introduction.md")
    qs: dict[str, str] = {}
    if src.exists():
        for f in src.iterdir():
            m = re.match(r"^question_(\d+)\.md$", f.name)
            if m:
                qs[f"question{m.group(1)}"] = _read_text_safe(f)
    excel_parts: list[str] = []
    if src.exists():
        for f in sorted(src.glob("excel_*.md")):
            excel_parts.append(_read_text_safe(f))
    out = {
        "intro": intro,
        "questions": qs,
        "excel": "\n\n".join(excel_parts),
        "available": bool(intro and qs),
    }
    SOURCE_CACHE[slug] = out
    return out


# ---------------------------------------------------------------------------
# Multiple-choice option parsing — handles all observed Modeloff layouts
# ---------------------------------------------------------------------------
_OPT_LINE_RE = re.compile(r"(?:^|\s)([A-Ia-i])[\.\)]\s+([^\n]+)")
_OPT_LINE_RE_ALT = re.compile(r"(?:^|\s)([A-Ia-i])\s+([^A-Ia-i\n][^\n]*)")
_OPT_ANYWHERE_RE = re.compile(
    r"(?<![A-Za-z])([A-Ia-i])[\.\)]\s+([\S][^A-Ia-i\n]*[^\s])"
)


def parse_options(question_text: str) -> dict[str, str]:
    """Extract a {letter: text} mapping from the question file.

    Handles three layouts observed in the Modeloff dump:
      1. ``A. <text>\\nB. <text>``  (one-option-per-line, dot)
      2. ``a) <text>\\nb) <text>``  (lowercase + paren)
      3. ``A 31 Dec 2044 D 30 Sep 2045 G ...``  (3-columns-per-row layout
         used in some 2017 finals; whitespace-separated, no dot)
    """
    # Layout 1+2: one option per line with dot or paren separator
    out: dict[str, str] = {}
    for m in _OPT_LINE_RE.finditer(question_text):
        letter, txt = m.group(1).upper(), m.group(2).strip().rstrip(".")
        if 1 <= len(txt) <= 200 and letter not in out:
            out[letter] = txt
    if len(out) >= 2:
        return out
    # Layout 3 — multi-column without dot: try splitting on letter boundaries
    out.clear()
    # Strategy: replace each " A " (capital letter surrounded by spaces, or
    # at start of line) with a marker, then split on the marker.
    txt = question_text
    # Normalise newlines
    txt = re.sub(r"[\r\n]+", " ", txt)
    # Find letter markers " X " where X in A-I
    marks = []
    for m in re.finditer(r"(?:^|\s)([A-I])\s+", txt):
        marks.append((m.start(), m.end(), m.group(1)))
    if len(marks) >= 4:
        for i, (s, e, letter) in enumerate(marks):
            end = marks[i + 1][0] if i + 1 < len(marks) else len(txt)
            piece = txt[e:end].strip()
            if piece and letter not in out:
                out[letter] = piece[:200]
        if len(out) >= 4:
            return out
    return {}


def parse_question_stem(question_text: str) -> str:
    """Return everything before the first option as the question stem."""
    # Strip the leading "Question N" header
    stem = re.sub(r"^\s*Question\s+\d+\s*", "", question_text, count=1,
                   flags=re.IGNORECASE)
    # Stop at the first option marker
    m = re.search(r"(?:^|\n)\s*[A-Ia-i][\.\)]\s+", stem)
    if m:
        stem = stem[:m.start()]
    else:
        # Layout 3: stop at the first " A " marker following whitespace
        m2 = re.search(r"(?:^|\s)A\s+\S", stem)
        if m2:
            stem = stem[:m2.start()]
    return stem.strip()


# ---------------------------------------------------------------------------
# Path A — Anthropic API
# ---------------------------------------------------------------------------
_CLIENT = None


def _get_client():
    global _CLIENT
    if _CLIENT is not None:
        return _CLIENT
    try:
        import anthropic
    except ImportError:
        return None
    try:
        _CLIENT = anthropic.Anthropic()
    except Exception:
        _CLIENT = None
    return _CLIENT


def call_anthropic(question_text: str, source_excerpt: str,
                   options: dict[str, str],
                   model: str = "claude-opus-4-7",
                   style: str = "single_shot") -> str:
    """Call Claude for a single-letter / short-text answer.

    style ∈ {single_shot, cot, few_shot, source_rich, source_minimal}.
    Returns "" on any error (caller falls back to heuristic).
    """
    client = _get_client()
    if client is None:
        return ""
    opt_str = "\n".join(f"  {k}. {v}" for k, v in sorted(options.items()))
    expected = ", ".join(sorted(options.keys())) if options else "a number or short string"
    # Compose the prompt per style
    if style == "single_shot":
        prefix = ("You are a top-tier financial modeller. Answer the Modeloff "
                  "question by selecting one of the options. Reply with ONLY "
                  "the answer letter, no explanation.")
    elif style == "cot":
        prefix = ("You are a top-tier financial modeller. Think step by step "
                  "(Kojima et al. 2022), then answer with exactly one letter "
                  "from the options below. Put your final answer on the LAST "
                  "line in the form: ANSWER: X")
    elif style == "few_shot":
        prefix = ("You are a top-tier financial modeller. Examples:\n"
                  "Q: For a 3-month bond at 5% APR, what is the period rate?\n"
                  "Options: A. 1.25% B. 1.227% C. 5%\n"
                  "ANSWER: B\n\n"
                  "Now solve this question. Reply with ANSWER: X on the last line.")
    elif style == "source_minimal":
        prefix = ("You are a top-tier financial modeller. Use ONLY the "
                  "question and options below. Reply with ONLY the answer letter.")
        source_excerpt = ""  # zero out
    else:  # source_rich
        prefix = ("You are a top-tier financial modeller with access to the full "
                  "case-study background. Reply with ONLY the answer letter.")
    src_block = f"Background:\n{source_excerpt}\n\n" if source_excerpt else ""
    content = f"""{prefix}

{src_block}Question:
{question_text}

Options:
{opt_str}

Valid replies: {expected}"""
    try:
        msg = client.messages.create(
            model=model,
            max_tokens=512,
            messages=[{"role": "user", "content": content}],
        )
        out = msg.content[0].text.strip()
        # Parse final letter
        # Look for "ANSWER: X" first
        m = re.search(r"ANSWER\s*[:=]?\s*([A-Ia-i])\b", out)
        if m:
            return m.group(1).upper()
        # Otherwise grab the first / last standalone letter
        toks = re.findall(r"\b([A-Ia-i])\b", out)
        if toks:
            return toks[-1].upper()
        return out.strip()[:1].upper() if out else ""
    except Exception:
        return ""


# ---------------------------------------------------------------------------
# Path B — Offline structural-LLM heuristic
# ---------------------------------------------------------------------------
_STOPWORDS = frozenset(
    "the a an of for to in on at by with from as is it be are was were "
    "this that these those which what when where how why or and not no "
    "but if then so will would should could may might can do does did "
    "i you we they he she him her them us our your their its his hers "
    "modeloff question option answer mark marks per".split()
)


def _tokens(text: str) -> list[str]:
    return [t for t in re.findall(r"[A-Za-z0-9$%.,/-]+", text.lower())
            if t and t not in _STOPWORDS and len(t) > 1]


def _numeric_terms(text: str) -> list[str]:
    return re.findall(r"-?\d+(?:[.,]\d+)*%?", text)


def heuristic_answer(question_text: str, intro: str, excel_md: str,
                     train_pool_letters: list[str] | None = None) -> tuple[str, dict[str, float]]:
    """Pure-Python answerer using token-overlap scoring over the source.

    Returns (best_letter, per_option_scores).

    The scoring rule:
      score(option) = w1 * overlap(option_tokens, source_tokens)
                    + w2 * overlap(option_numerics, source_numerics)
                    + w3 * train_pool_letter_prior(letter)
                    + w4 * length_penalty(option)

    Falls back to the train-pool mode letter when no options can be parsed.
    """
    options = parse_options(question_text)
    if not options:
        # No MC options found — fall back to pool mode
        if train_pool_letters:
            c = Counter(train_pool_letters)
            return c.most_common(1)[0][0], {}
        return "A", {}
    stem = parse_question_stem(question_text)
    # Source corpus = stem + intro + excel
    src_tokens = set(_tokens(stem) + _tokens(intro) + _tokens(excel_md))
    src_numbers = set(_numeric_terms(stem) + _numeric_terms(intro) + _numeric_terms(excel_md))
    # Train-pool letter prior
    pool_counter = Counter(train_pool_letters) if train_pool_letters else Counter()
    pool_n = max(1, sum(pool_counter.values()))
    scores: dict[str, float] = {}
    for letter, opt_text in options.items():
        opt_tokens = set(_tokens(opt_text))
        opt_numbers = set(_numeric_terms(opt_text))
        # Components
        overlap_tok = len(opt_tokens & src_tokens) / max(1, len(opt_tokens))
        overlap_num = (len(opt_numbers & src_numbers) / max(1, len(opt_numbers))
                       if opt_numbers else 0.0)
        prior = pool_counter.get(letter, 0) / pool_n
        # Length penalty: extremely short options (1-2 chars) get no credit
        len_pen = min(1.0, len(opt_text) / 10.0)
        score = (0.45 * overlap_tok + 0.30 * overlap_num
                  + 0.15 * prior + 0.10 * len_pen)
        scores[letter] = score
    best = max(scores, key=scores.get)
    return best, scores


# ---------------------------------------------------------------------------
# Top-level answer entry point
# ---------------------------------------------------------------------------
def answer_question(slug: str, question_name: str,
                    train_pool_letters: list[str] | None = None,
                    *, prefer_api: bool = True,
                    api_style: str = "single_shot",
                    source_excerpt_chars: int = 8000) -> dict:
    """Return {answer, options, scores, path, slug, question_name}.

    answer is a single uppercase letter (A-I) or "" if the question can't be
    answered (no options + no pool fallback). Callers downstream encode it
    through the LabelEncoder.
    """
    src = load_source_for_slug(slug)
    qtext = src["questions"].get(question_name, "")
    intro = src["intro"]
    excel = src["excel"]
    if not qtext:
        # Source missing for this question — fall back to pool mode
        if train_pool_letters:
            c = Counter(train_pool_letters)
            return {"answer": c.most_common(1)[0][0], "path": "pool_fallback_no_source",
                    "options": {}, "scores": {}, "slug": slug,
                    "question_name": question_name}
        return {"answer": "A", "path": "pool_fallback_no_source",
                "options": {}, "scores": {}, "slug": slug,
                "question_name": question_name}
    options = parse_options(qtext)
    # Try API if available + preferred
    if prefer_api and has_api_key() and options:
        excerpt = (intro + "\n\n" + excel)[:source_excerpt_chars]
        ans = call_anthropic(qtext, excerpt, options, style=api_style)
        if ans and ans in options:
            return {"answer": ans, "path": f"api_{api_style}",
                    "options": options, "scores": {},
                    "slug": slug, "question_name": question_name}
        # Fall through to heuristic on failure / malformed reply
    best, scores = heuristic_answer(qtext, intro, excel, train_pool_letters)
    return {"answer": best, "path": "heuristic", "options": options,
            "scores": scores, "slug": slug, "question_name": question_name}


def get_question_name(info: dict, i: int) -> str:
    """Recover the question name (e.g. "question6") for index i in a task."""
    if 0 <= i < len(info["questions"]):
        return info["questions"][i]
    return ""
