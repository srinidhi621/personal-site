#!/usr/bin/env python3
"""
AI Writing Forensics (text-only, editor-friendly).

DEPRECATED: This script has been superseded by scripts/ai_forensics_unified.py.
Use the unified script for all new analyses. This script is kept for backward
compatibility and will be removed in a future cleanup.

Supports the rubric in `docs/agent-skills/ai-detection-2.md`.

Design goals:
- Output is meant to be pasted/read in a terminal session.
- No giant tables. No JSON blob. Every line should be actionable.
- Flags include exact quotes + file line numbers for fast edits.

Usage:
  python3 scripts/ai_writing_forensics.py --file content/writing/<post>.md --channel blog --intent inform --topic "..."
"""

from __future__ import annotations

import argparse
import re
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'_-]*")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def strip_frontmatter(raw: str) -> str:
    if raw.startswith("---\n"):
        return re.sub(r"^---.*?---\s*", "", raw, flags=re.S)
    if raw.startswith("+++\n"):
        return re.sub(r"^\+\+\+.*?\+\+\+\s*", "", raw, flags=re.S)
    return raw


def sentence_lengths(text: str) -> List[int]:
    flat = re.sub(r"\s+", " ", text).strip()
    sents = [s.strip() for s in SENTENCE_SPLIT_RE.split(flat) if s.strip()]
    return [len(WORD_RE.findall(s)) for s in sents]


def count_anchors(text: str) -> int:
    anchors = 0
    anchors += len(re.findall(r"\b\d+(?:\.\d+)?%?\b", text))
    anchors += len(re.findall(r"\b20\d{2}\b", text))
    anchors += len(re.findall(r"\b[A-Z]{2,}\b", text))
    return anchors


def count_phrase(text: str, phrase: str) -> int:
    # whole-word for single words; substring for multi-word phrases
    low = text.lower()
    p = phrase.lower()
    if " " in p:
        return low.count(p)
    return len(re.findall(rf"\b{re.escape(p)}\b", low))


def section_for_line(lines: List[str], lineno: int) -> str:
    # Find nearest preceding H2 heading.
    # lineno is 1-based.
    idx = max(0, lineno - 1)
    for i in range(idx, -1, -1):
        line = lines[i].rstrip("\n")
        if line.startswith("## "):
            return line[3:].strip() or "Untitled"
    return "Intro"


@dataclass(frozen=True)
class Flag:
    lineno: int
    section: str
    quote: str
    family: str
    strength: str  # low/medium/high
    why: str
    rewrite_direction: str


def extract_quote(lines: List[str], lineno: int) -> str:
    line = lines[lineno - 1].rstrip("\n").strip()
    return line if line else "(blank line)"


def gather_flags(lines: List[str]) -> List[Flag]:
    """
    Line-based flags: optimized for fast editing (jump to line number, rewrite).
    """
    patterns: List[Tuple[re.Pattern, str, str, str, str]] = [
        # (regex, family, strength, why, rewrite_direction)
        (
            re.compile(r"\[(?:placeholder|todo|tbd)\s*:", re.I),
            "Family G — Hard artifacts",
            "high",
            "Explicit placeholder in prose is a strong draft/AI-assist tell and breaks reader trust.",
            "Replace with a specific real incident/detail, or delete the line.",
        ),
        (
            re.compile(r"\bthis is a short list\b", re.I),
            "Family C — Template scaffolding",
            "medium",
            "Common thought-leadership boilerplate; reads generic unless followed by a concrete promise.",
            "Replace with a concrete promise: what changed, what broke, and what the reader will get.",
        ),
        (
            re.compile(r"\bthe pattern that held up\b", re.I),
            "Family C — Template scaffolding",
            "medium",
            "Slide-ready phrasing can sound influencer-y if not tied to a scar (what failed first, what changed).",
            "Rewrite as mechanism + scar: what you tried first, what failed, what held up and why.",
        ),
        (
            re.compile(r"\bnon-negotiable\b", re.I),
            "Family B/C — Influencer certainty",
            "medium",
            "Overconfident/absolute phrasing; can read LinkedIn-ish without a concrete forcing event.",
            "Rewrite as consequence: 'After [incident], we made these changes…' (show the forcing function).",
        ),
        (
            re.compile(r"\bwe converged on\b", re.I),
            "Family C — Case-study template",
            "low",
            "Reads like a polished case-study beat; better when you mention what you cut and why.",
            "Rewrite as decision scar: 'We started with X, cut Y, kept Z because…'.",
        ),
        (
            re.compile(r"\bthink of it as\b", re.I),
            "Family C — Portable maxim",
            "medium",
            "Aphorism framing; can sound generic unless anchored to an observed failure mode.",
            "Add one concrete failure mode or example right after the line.",
        ),
        (
            re.compile(r"\bthe goal is not\b.*\bit is\b", re.I),
            "Family C — Template cadence",
            "medium",
            "Classic blog cadence ('not X; it is Y'); fine once, but reads templated if repeated.",
            "Make it more direct and local: what users needed to do in practice; remove the philosophical framing.",
        ),
        (
            re.compile(r"\bmost of this will still apply\b", re.I),
            "Family C — Generic wrap-up",
            "medium",
            "Universal closer; risks sounding like a generic thought-leadership wrap-up.",
            "Rewrite as a concrete invariant: name 2–3 operational constraints that remain even if models improve.",
        ),
        (
            re.compile(r"\bstop doing\b|\bhere's what nobody tells you\b|\blet that sink in\b", re.I),
            "Family B — LinkedIn influencer dialect",
            "high",
            "Strong LinkedIn dialect markers.",
            "Remove the contrarian hook; replace with a specific observation or incident.",
        ),
        (
            re.compile(r"\b10x\b", re.I),
            "Family B — Influencer shorthand",
            "low",
            "Not always bad, but '10x' can trip influencer/AI vibes depending on tone.",
            "If it’s not essential, replace with a specific measurable improvement or remove.",
        ),
    ]

    flags: List[Flag] = []
    for lineno, line in enumerate(lines, start=1):
        raw = line.rstrip("\n")
        if not raw.strip():
            continue
        sec = section_for_line(lines, lineno)
        for rx, family, strength, why, rewrite in patterns:
            if rx.search(raw):
                quote = raw.strip()
                flags.append(
                    Flag(
                        lineno=lineno,
                        section=sec,
                        quote=quote,
                        family=family,
                        strength=strength,
                        why=why,
                        rewrite_direction=rewrite,
                    )
                )
                break

    # Deduplicate by (quote, line) and keep stable order.
    seen = set()
    uniq: List[Flag] = []
    for f in flags:
        key = (f.lineno, f.quote)
        if key in seen:
            continue
        seen.add(key)
        uniq.append(f)
    return uniq


def component_scores(text: str) -> Dict[str, int]:
    # Lexicon cluster
    lexicon_terms = [
        "delve",
        "unlock",
        "harness",
        "robust",
        "seamless",
        "at its core",
        "key takeaway",
        "important to note",
        "it's worth noting",
        "it’s worth noting",
    ]
    word_count = len(WORD_RE.findall(text))
    lex_hits = sum(count_phrase(text, t) for t in lexicon_terms)
    lex_density = (lex_hits / word_count) if word_count else 0.0
    if lex_density < 0.002:
        lex = 0
    elif lex_density < 0.006:
        lex = 8
    elif lex_density < 0.012:
        lex = 14
    else:
        lex = 20

    # Cadence uniformity (doc-level)
    lens = sentence_lengths(text)
    if lens:
        mean = statistics.mean(lens)
        std = statistics.pstdev(lens) if len(lens) > 1 else 0.0
        cv = (std / mean) if mean else 0.0
    else:
        cv = 0.0
    if cv >= 0.55:
        cadence = 0
    elif cv >= 0.40:
        cadence = 6
    elif cv >= 0.30:
        cadence = 12
    else:
        cadence = 15

    # Rhetorical template score
    rule3 = len(re.findall(r"\b\w+\b,\s+\b\w+\b,\s+and\s+\b\w+\b", text))
    notbut = len(re.findall(r"not\s+[^\n]{0,120}?\s+but\s+", text, flags=re.I))
    headings = len(re.findall(r"^##\s+", text, flags=re.M))
    placeholders = len(re.findall(r"\[(?:placeholder|todo|tbd)\s*:", text, flags=re.I))
    bullet_heavy = 0
    for block in re.split(r"\n\s*\n", text):
        bl = sum(1 for l in block.split("\n") if l.strip().startswith("- "))
        if bl >= 3:
            bullet_heavy += 1
    template_points = 0
    if headings >= 6:
        template_points += 1
    if rule3 >= 5:
        template_points += 1
    if notbut >= 2:
        template_points += 1
    if bullet_heavy >= 6:
        template_points += 1
    template = 0 if template_points == 0 else 7 if template_points <= 2 else 12 if template_points <= 4 else 15

    # Abstraction / anchors
    anchors = count_anchors(text)
    anchor_rate = (anchors / word_count) if word_count else 0.0
    if anchor_rate >= 0.020:
        abstraction = 0
    elif anchor_rate >= 0.010:
        abstraction = 10
    elif anchor_rate >= 0.005:
        abstraction = 18
    else:
        abstraction = 25

    # Thought texture (deterministic heuristic)
    lower = f" {text.lower()} "
    decision_scar_markers = sum(lower.count(w) for w in [" we tried ", " it failed ", " incident", " postmortem", " rollback", " audit", " cfo", " board review", " mid-demo "])
    texture = 8
    if decision_scar_markers >= 4:
        texture -= 2
    if anchor_rate >= 0.010:
        texture -= 1
    if placeholders:
        texture += 2
    texture = max(0, min(15, texture))

    # Contradictions / overreach (very conservative)
    universal_claims = len(re.findall(r"\b(always|never|everyone|no one)\b", text, flags=re.I))
    overreach = 0 if universal_claims < 6 else 3 if universal_claims < 12 else 5

    # Hard artifacts
    hard = 0 if placeholders == 0 else 3 if placeholders == 1 else 5

    return {
        "lexicon_cluster": lex,
        "cadence_uniformity": cadence,
        "rhetorical_template": template,
        "abstraction_low_anchor": abstraction,
        "thought_texture": texture,
        "contradictions_overreach": overreach,
        "hard_artifacts": hard,
        "word_count": word_count,
        "anchor_rate_x1000": int(anchor_rate * 1000),  # e.g. 13 means 0.013
    }


def classify(score: int) -> str:
    if score <= 29:
        return "Likely Human"
    if score <= 59:
        return "Ambiguous/Hybrid"
    if score <= 79:
        return "Probably AI-Assisted"
    return "Likely AI-Generated"


def primary_dialect(flags: List[Flag], scores: Dict[str, int], *, channel: str) -> str:
    if any("LinkedIn influencer" in f.family for f in flags):
        return "LinkedIn-Template"
    if scores["rhetorical_template"] >= 12 and scores["abstraction_low_anchor"] >= 10:
        return "Corporate-Generic"
    if channel.lower() in {"marketing", "landing-page"} and scores["rhetorical_template"] >= 12:
        return "Marketing-Polish"
    return "None"


def format_flags(flags: List[Flag], limit: int) -> List[Flag]:
    # Prioritize: high first, then medium, then low; stable order within severity by line number.
    sev = {"high": 0, "medium": 1, "low": 2}
    ordered = sorted(flags, key=lambda f: (sev.get(f.strength, 9), f.lineno))
    return ordered[:limit]


def group_by_section(flags: Iterable[Flag]) -> Dict[str, List[Flag]]:
    out: Dict[str, List[Flag]] = {}
    for f in flags:
        out.setdefault(f.section, []).append(f)
    # stable within section
    for sec in out:
        out[sec] = sorted(out[sec], key=lambda f: f.lineno)
    return out


def main() -> int:
    import warnings
    warnings.warn(
        "ai_writing_forensics.py is deprecated. Use ai_forensics_unified.py instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    print("WARNING: This script is deprecated. Use scripts/ai_forensics_unified.py instead.\n",
          file=__import__("sys").stderr)

    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Path to markdown/text file to analyze")
    parser.add_argument("--channel", default="blog")
    parser.add_argument("--author-profile", default="unknown")
    parser.add_argument("--intent", default="inform")
    parser.add_argument("--topic", default="")
    parser.add_argument("--max-flags", type=int, default=15, help="Max items in Top Red Flags")
    args = parser.parse_args()

    path = Path(args.file)
    raw = path.read_text(encoding="utf-8")
    body = strip_frontmatter(raw)
    lines = body.replace("\r\n", "\n").split("\n")

    scores = component_scores(body)
    total = min(
        100,
        scores["lexicon_cluster"]
        + scores["cadence_uniformity"]
        + scores["rhetorical_template"]
        + scores["abstraction_low_anchor"]
        + scores["thought_texture"]
        + scores["contradictions_overreach"]
        + scores["hard_artifacts"],
    )
    classification = classify(total)

    flags = gather_flags(lines)
    dialect = primary_dialect(flags, scores, channel=args.channel)

    # 1) Executive Summary
    print("1) Executive Summary")
    print(f"- Score: {total}/100 ({classification})")
    print(f"- Dialect: {dialect}")
    print(f"- Context: channel={args.channel}, intent={args.intent}, author_profile={args.author_profile}, topic={args.topic or '(none)'}")
    print("- Main drivers:")
    if scores["hard_artifacts"]:
        print("  - Hard artifacts present (placeholders, TODOs): fix these first.")
    if scores["rhetorical_template"] >= 12:
        print("  - Template scaffolding is strong (framework/list/maxim cadence).")
    if scores["abstraction_low_anchor"] >= 10:
        ar = scores["anchor_rate_x1000"] / 1000.0
        print(f"  - Anchors are present but uneven (anchor_rate≈{ar:.4f}); add decision scars where claims are abstract.")
    if scores["lexicon_cluster"] == 0:
        print("  - Good: no meaningful clustering of classic AI/corporate safe-words.")
    if scores["cadence_uniformity"] == 0:
        print("  - Good: sentence rhythm is varied (not AI-smooth monotone).")
    print("")

    # 2) Overall Assessment
    print("2) Overall Assessment")
    print("- Component totals (deterministic):")
    print(f"  - lexicon_cluster: {scores['lexicon_cluster']}")
    print(f"  - cadence_uniformity: {scores['cadence_uniformity']}")
    print(f"  - rhetorical_template: {scores['rhetorical_template']}")
    print(f"  - abstraction_low_anchor: {scores['abstraction_low_anchor']}")
    print(f"  - thought_texture: {scores['thought_texture']}")
    print(f"  - contradictions_overreach: {scores['contradictions_overreach']}")
    print(f"  - hard_artifacts: {scores['hard_artifacts']}")
    print("- What NOT to over-edit:")
    if scores["lexicon_cluster"] == 0:
        print("  - Don’t waste time swapping vocabulary just to avoid 'AI words'; that’s not the issue here.")
    if scores["cadence_uniformity"] == 0:
        print("  - Don’t force more rhythm variance; the cadence is already human-consistent.")
    print("")

    # 3) Top Red Flags (Evidence Quotes)
    print("3) Top Red Flags (Evidence Quotes)")
    top = format_flags(flags, limit=args.max_flags)
    if not top:
        print("- No high-signal lines matched the built-in patterns. (This does NOT mean the draft is 'proven human'.)")
    else:
        for f in top:
            print(f"- Line {f.lineno} [{f.strength}] ({f.family})")
            print(f"  - Quote: {f.quote}")
            print(f"  - Why: {f.why}")
            print(f"  - Rewrite: {f.rewrite_direction}")
    print("")

    # 4) Deep Forensic Findings
    print("4) Deep Forensic Findings")
    print("- Template scaffolding")
    if scores["rhetorical_template"] >= 12:
        print("  - Many sections are structured as: principle → bullet list → maxim. That reads 'portable' (talk-track) unless you add scars.")
        print("  - Fix pattern: after each framework, add one forcing event (incident, audit, exec review) and what changed.")
    else:
        print("  - Not a major issue.")
    print("- LinkedIn influencer leakage")
    if dialect == "LinkedIn-Template":
        print("  - Detected strong LinkedIn dialect markers; remove contrarian hooks and moral-platitudes.")
    else:
        print("  - No strong LinkedIn markers; main risk is 'polished template prose', not platform slang.")
    print("- Anchors & scars")
    ar = scores["anchor_rate_x1000"] / 1000.0
    print(f"  - anchor_rate≈{ar:.4f}. Where you state 'this matters' or 'non-negotiable', add: the incident, the symptom, the fix.")
    print("")

    # 5) Actionable Rewrite Guidance (section-wise)
    print("5) Actionable Rewrite Guidance (section-wise)")
    if not flags:
        print("- No section-wise guidance generated (no flags matched).")
        return 0

    by_sec = group_by_section(top)
    for sec, sec_flags in by_sec.items():
        print(f"\n## {sec}")
        print("- Fix these lines first (fastest trust gain):")
        for f in sec_flags[:6]:
            # Provide a short before→after template for common cases.
            before = f.quote
            if f.family.startswith("Family G"):
                after = "[placeholder: replace with a concrete incident (what changed, symptom, how you caught it, what you changed)]"
            elif "non-negotiable" in before.lower():
                after = "After [incident], we changed [X] because [Y]. (Brief mechanism, not a maxim.)"
            elif "pattern that held up" in before.lower():
                after = "What held up after [failure] was [mechanism]. We chose it because [constraint]."
            elif "most of this will still apply" in before.lower():
                after = "Even if models improve, [invariant 1], [invariant 2], and [invariant 3] still bite in production."
            elif "this is a short list" in before.lower():
                after = "Here are the lessons that changed how we built/operated the system: [X], [Y], [Z]."
            else:
                after = "[placeholder: rewrite more directly; add one concrete anchor or tradeoff]"

            print(f"  - Line {f.lineno}: {before}")
            print(f"    - Why: {f.family} ({f.strength})")
            print(f"    - Before → After: {before} → {after}")
    print("")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

