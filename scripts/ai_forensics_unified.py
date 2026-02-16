#!/usr/bin/env python3
"""
AI Writing Forensics — Unified Engine.

Canonical CLI for AI-writing detection and humanization guidance.
Implements the rubric in docs/agent-skills/ai-writing-forensics.md.
Reads patterns and weights from scripts/ai_forensics_rules.json.

Supersedes:
  - scripts/ai_writing_forensics.py
  - scripts/ai_forensics_deep.py
  - scripts/ai_forensics_linefinder.py

Usage:
  python3 scripts/ai_forensics_unified.py --file content/writing/<post>.md
  python3 scripts/ai_forensics_unified.py --file <path> --channel blog --intent inform --topic "AI eng"
  python3 scripts/ai_forensics_unified.py --file <path> --json
  python3 scripts/ai_forensics_unified.py --file <path> --verbose
"""

from __future__ import annotations

import argparse
import json
import math
import re
import statistics
import sys
from collections import Counter
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ──────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────

WORD_RE = re.compile(r"[A-Za-z][A-Za-z'_-]*")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
RULES_PATH = Path(__file__).parent / "ai_forensics_rules.json"


# ──────────────────────────────────────────────
# Data classes
# ──────────────────────────────────────────────

@dataclass
class Flag:
    lineno: int
    section: str
    quote: str
    family: str
    strength: str       # low / medium / high
    why: str
    rewrite_direction: str


@dataclass
class FamilyScore:
    name: str
    key: str
    raw: float          # raw computed value (0..1 or absolute)
    score: int          # final points contributed (0..max_weight)
    max_weight: int
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Report:
    file_path: str
    word_count: int
    sentence_count: int
    paragraph_count: int
    family_scores: List[FamilyScore]
    cluster_boosts: List[Tuple[str, int]]
    base_score: int
    boost_total: int
    final_score: int
    classification: str
    dialect: str
    flags: List[Flag]
    short_text_warning: bool = False


# ──────────────────────────────────────────────
# Text helpers
# ──────────────────────────────────────────────

def load_rules(path: Path = RULES_PATH) -> Dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def strip_frontmatter(raw: str) -> str:
    if raw.startswith("---\n"):
        return re.sub(r"^---.*?---\s*", "", raw, flags=re.S)
    if raw.startswith("+++\n"):
        return re.sub(r"^\+\+\+.*?\+\+\+\s*", "", raw, flags=re.S)
    return raw


def get_words(text: str) -> List[str]:
    return WORD_RE.findall(text)


def get_words_lower(text: str) -> List[str]:
    return [w.lower() for w in WORD_RE.findall(text)]


def get_sentences(text: str) -> List[str]:
    flat = re.sub(r"\s+", " ", text).strip()
    return [s.strip() for s in SENTENCE_SPLIT_RE.split(flat) if s.strip()]


def get_paragraphs(text: str) -> List[str]:
    """Split into paragraphs on blank lines, filtering empties and headings."""
    raw_paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    prose = []
    for p in raw_paras:
        first_line = p.split("\n")[0]
        if re.match(r"^(#{1,6}\s|>\s|\s*[-*]\s|\s*\d+\.\s)", first_line):
            continue
        prose.append(p)
    return prose


def sentence_word_counts(text: str) -> List[int]:
    sents = get_sentences(text)
    return [len(get_words(s)) for s in sents]


def section_for_line(lines: List[str], lineno: int) -> str:
    idx = max(0, lineno - 1)
    for i in range(idx, -1, -1):
        stripped = lines[i].rstrip("\n")
        if stripped.startswith("## "):
            return stripped[3:].strip() or "Untitled"
    return "Intro"


def count_phrase(text_lower: str, phrase: str) -> int:
    p = phrase.lower()
    if " " in p:
        return text_lower.count(p)
    return len(re.findall(rf"\b{re.escape(p)}\b", text_lower))


def split_into_sections(lines: List[str]) -> List[Tuple[str, str]]:
    """Return list of (section_name, section_text) based on ## headings."""
    sections: List[Tuple[str, str]] = []
    current_name = "Intro"
    current_lines: List[str] = []
    for line in lines:
        stripped = line.rstrip("\n")
        if stripped.startswith("## "):
            if current_lines:
                sections.append((current_name, "\n".join(current_lines)))
            current_name = stripped[3:].strip() or "Untitled"
            current_lines = []
        else:
            current_lines.append(line)
    if current_lines:
        sections.append((current_name, "\n".join(current_lines)))
    return sections


# ──────────────────────────────────────────────
# Family A: Lexicon / phrase clusters
# ──────────────────────────────────────────────

def score_lexicon(text: str, rules: Dict[str, Any]) -> FamilyScore:
    max_w = rules["weights"]["lexicon_phrase_clusters"]
    lex_rules = rules["lexicon"]
    text_lower = f" {text.lower()} "
    words = get_words(text)
    word_count = len(words)

    all_terms: List[str] = []
    for group in ["verbs", "nouns", "adjectives", "fillers", "modern_ai_terms"]:
        all_terms.extend(lex_rules.get(group, []))

    hits = sum(count_phrase(text_lower, t) for t in all_terms)
    density = hits / word_count if word_count else 0.0

    thresholds = lex_rules["thresholds"]
    if density < thresholds["low"]:
        pts = 0
    elif density < thresholds["medium"]:
        pts = int(max_w * 0.3)
    elif density < thresholds["high"]:
        pts = int(max_w * 0.7)
    else:
        pts = max_w

    return FamilyScore(
        name="Lexicon / phrase clusters",
        key="lexicon_phrase_clusters",
        raw=density,
        score=pts,
        max_weight=max_w,
        details={"hits": hits, "density": round(density, 5), "word_count": word_count},
    )


# ──────────────────────────────────────────────
# Family B: Cadence / mechanical framing
# ──────────────────────────────────────────────

def score_cadence(text: str, rules: Dict[str, Any]) -> FamilyScore:
    max_w = rules["weights"]["cadence_mechanical_framing"]
    cad = rules["cadence"]
    total_pts = 0.0
    details: Dict[str, Any] = {}

    # --- Sentence length CV ---
    lens = sentence_word_counts(text)
    if len(lens) > 1:
        mean = statistics.mean(lens)
        std = statistics.pstdev(lens)
        cv = std / mean if mean else 0.0
    else:
        cv = 0.5  # neutral for single-sentence
    details["sentence_length_cv"] = round(cv, 3)

    cv_thresholds = cad["sentence_length_cv"]
    if cv >= cv_thresholds["healthy_min"]:
        cv_pts = 0
    elif cv >= cv_thresholds["moderate"]:
        cv_pts = 1
    elif cv >= cv_thresholds["suspicious"]:
        cv_pts = 3
    else:
        cv_pts = 5
    total_pts += cv_pts

    # --- Sentence starter variety ---
    sents = get_sentences(text)
    starters: Counter[str] = Counter()
    for s in sents:
        ws = get_words_lower(s)
        if ws:
            starters[ws[0]] += 1
    variety = len(starters) / len(sents) if sents else 1.0
    details["starter_variety"] = round(variety, 3)

    sv_thresholds = cad["sentence_starter_variety"]
    if variety >= sv_thresholds["healthy_min"]:
        sv_pts = 0
    elif variety >= sv_thresholds["low"]:
        sv_pts = 1
    else:
        sv_pts = 3
    total_pts += sv_pts

    # --- One-sentence paragraph ratio ---
    paras = get_paragraphs(text)
    one_sent = sum(1 for p in paras if len(get_sentences(p)) == 1)
    osp_ratio = one_sent / len(paras) if paras else 0.0
    details["one_sentence_para_ratio"] = round(osp_ratio, 3)
    details["total_paragraphs"] = len(paras)

    osp_thresholds = cad["one_sentence_para"]
    if osp_ratio <= osp_thresholds["safe_max"]:
        osp_pts = 0
    elif osp_ratio <= osp_thresholds["moderate"]:
        osp_pts = 1
    elif osp_ratio <= osp_thresholds["suspicious"]:
        osp_pts = 3
    elif osp_ratio <= 0.60:
        osp_pts = 5
    else:
        osp_pts = 7  # extreme broetry
    total_pts += osp_pts

    # --- Punctuation fingerprint ---
    word_count = len(get_words(text))
    per_1k = 1000 / word_count if word_count else 1.0

    em_dash_count = text.count("\u2014") + text.count("--")
    em_dash_per_1k = em_dash_count * per_1k
    details["em_dash_count"] = em_dash_count
    details["em_dash_per_1k"] = round(em_dash_per_1k, 2)

    semicolons = text.count(";")
    questions = text.count("?")
    parens = text.count("(")
    details["semicolons"] = semicolons
    details["questions"] = questions
    details["parentheses"] = parens

    em_thresholds = cad["em_dash"]
    if em_dash_per_1k <= em_thresholds["per_1000_words_safe"]:
        em_pts = 0
    elif em_dash_per_1k <= em_thresholds["per_1000_words_moderate"]:
        em_pts = 1
    elif em_dash_per_1k <= em_thresholds["per_1000_words_high"]:
        em_pts = 2
    elif em_dash_per_1k <= 12:
        em_pts = 4
    else:
        em_pts = 5  # extreme em-dash density
    total_pts += em_pts

    # --- Clause depth variance ---
    sub_conjs = cad.get("subordinating_conjunctions", [])
    clause_depths: List[int] = []
    for s in sents:
        depth = s.count(",")
        s_lower = s.lower()
        for sc in sub_conjs:
            depth += len(re.findall(rf"\b{re.escape(sc)}\b", s_lower))
        clause_depths.append(depth)
    if len(clause_depths) > 1:
        clause_cv = statistics.pstdev(clause_depths) / (statistics.mean(clause_depths) + 0.001)
    else:
        clause_cv = 0.5
    details["clause_depth_cv"] = round(clause_cv, 3)
    if clause_cv < 0.3:
        total_pts += 2  # very uniform clause depth

    # Scale total_pts to max weight
    raw_max = 5 + 3 + 7 + 5 + 2  # 22 possible raw points
    score = min(max_w, int(round(total_pts / raw_max * max_w)))

    return FamilyScore(
        name="Cadence / mechanical framing",
        key="cadence_mechanical_framing",
        raw=total_pts / raw_max,
        score=score,
        max_weight=max_w,
        details=details,
    )


# ──────────────────────────────────────────────
# Family C: Structural symmetry / scaffolding
# ──────────────────────────────────────────────

def score_structural(text: str, lines: List[str], rules: Dict[str, Any]) -> FamilyScore:
    max_w = rules["weights"]["structural_symmetry"]
    struct = rules["structural"]
    total_pts = 0.0
    details: Dict[str, Any] = {}

    # Rule-of-three
    r3_count = len(re.findall(r"\b\w+\b,\s+\b\w+\b,\s+and\s+\b\w+\b", text))
    details["rule_of_three_count"] = r3_count
    if r3_count >= struct["rule_of_three"]["suspicious_count"]:
        total_pts += 3

    # Negative parallelism
    neg_par_count = 0
    for pat in struct["negative_parallelism"]["patterns"]:
        neg_par_count += len(re.findall(pat, text, re.I))
    details["negative_parallelism_count"] = neg_par_count
    neg_thresh = struct["negative_parallelism"]["suspicious_count"]
    if neg_par_count >= neg_thresh + 2:
        total_pts += 4
    elif neg_par_count >= neg_thresh:
        total_pts += 2
    elif neg_par_count >= 1:
        total_pts += 1

    # Symmetric contrasts
    sym_count = 0
    for pat in struct["symmetric_contrast"]["patterns"]:
        sym_count += len(re.findall(pat, text, re.I))
    details["symmetric_contrast_count"] = sym_count
    sym_thresh = struct["symmetric_contrast"]["suspicious_count"]
    if sym_count >= sym_thresh + 3:
        total_pts += 4
    elif sym_count >= sym_thresh:
        total_pts += 2
    elif sym_count >= 2:
        total_pts += 1

    # Anaphora
    anaphora_cfg = struct["anaphora"]
    sents = get_sentences(text)
    anaphora_found = 0
    if len(sents) >= anaphora_cfg["min_consecutive"]:
        for i in range(len(sents) - anaphora_cfg["min_consecutive"] + 1):
            window = sents[i:i + anaphora_cfg["min_consecutive"]]
            prefixes = []
            for s in window:
                ws = get_words_lower(s)
                if len(ws) >= anaphora_cfg["min_phrase_words"]:
                    prefixes.append(" ".join(ws[:anaphora_cfg["min_phrase_words"]]))
                else:
                    prefixes.append("")
            if prefixes[0] and all(p == prefixes[0] for p in prefixes):
                anaphora_found += 1
    details["anaphora_instances"] = anaphora_found
    if anaphora_found >= 2:
        total_pts += 2
    elif anaphora_found >= 1:
        total_pts += 1

    # Heading structure regularity
    headings = [l.rstrip("\n") for l in lines if l.rstrip("\n").startswith("## ")]
    details["heading_count"] = len(headings)
    if len(headings) >= struct["heading_regularity"]["min_headings"]:
        depths = [len(re.match(r"^#+", h).group()) for h in headings]
        if len(set(depths)) == 1:
            total_pts += 1

    # Bullet-heavy blocks
    bullet_blocks = 0
    for block in re.split(r"\n\s*\n", text):
        bl = sum(1 for ln in block.split("\n") if ln.strip().startswith("- "))
        if bl >= 3:
            bullet_blocks += 1
    details["bullet_heavy_blocks"] = bullet_blocks
    if bullet_blocks >= 6:
        total_pts += 3
    elif bullet_blocks >= 3:
        total_pts += 2
    elif bullet_blocks >= 1:
        total_pts += 1

    # Parallel line structures (consecutive lines with same syntactic pattern)
    non_empty = [l.rstrip("\n") for l in lines if l.strip() and not l.strip().startswith("#")]
    parallel_groups = 0
    for i in range(len(non_empty) - 2):
        # Check for gerund-start or noun-start parallelism in consecutive lines
        starters = []
        for j in range(i, min(i + 4, len(non_empty))):
            w = get_words_lower(non_empty[j])
            if w:
                starters.append(w[0])
        # 3+ consecutive lines starting with same POS-like pattern (gerunds, etc.)
        if len(starters) >= 3:
            if starters[0].endswith("ing") and all(s.endswith("ing") for s in starters[:3]):
                parallel_groups += 1
    details["parallel_line_groups"] = parallel_groups
    if parallel_groups >= 2:
        total_pts += 2
    elif parallel_groups >= 1:
        total_pts += 1

    # Title-case non-heading lines (AI draft formatting tell)
    title_case_lines = 0
    for l in lines:
        stripped = l.rstrip("\n").strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("-") or stripped.startswith(">"):
            continue
        words_l = stripped.split()
        if 3 <= len(words_l) <= 10:
            skip = {"a", "an", "the", "in", "on", "at", "to", "for", "of", "and", "or", "but", "is", "are", "was"}
            caps = sum(1 for w in words_l if w[0].isupper() and w.lower() not in skip)
            if caps / len(words_l) >= 0.7 and not stripped.endswith("."):
                title_case_lines += 1
    details["title_case_prose_lines"] = title_case_lines
    if title_case_lines >= 3:
        total_pts += 3
    elif title_case_lines >= 1:
        total_pts += 1

    raw_max = 3 + 4 + 4 + 2 + 1 + 3 + 2 + 3  # 22
    score = min(max_w, int(round(total_pts / raw_max * max_w)))

    return FamilyScore(
        name="Structural symmetry / scaffolding",
        key="structural_symmetry",
        raw=total_pts / raw_max,
        score=score,
        max_weight=max_w,
        details=details,
    )


# ──────────────────────────────────────────────
# Family D: Specificity quality
# ──────────────────────────────────────────────

def score_specificity(text: str, lines: List[str], rules: Dict[str, Any]) -> FamilyScore:
    max_w = rules["weights"]["specificity_quality"]
    spec = rules["specificity"]
    details: Dict[str, Any] = {}
    word_count = len(get_words(text))

    # Strong anchors
    strong = 0
    for pat in spec["strong_anchor_patterns"]:
        strong += len(re.findall(pat, text))
    details["strong_anchors"] = strong

    # Weak anchors (for context, not scored positively)
    weak = 0
    for pat in spec["weak_anchor_patterns"]:
        weak += len(re.findall(pat, text))
    details["weak_anchors"] = weak

    # Vague quantifiers
    text_lower = text.lower()
    vague = sum(len(re.findall(rf"\b{re.escape(v)}\b", text_lower)) for v in spec["vague_quantifiers"])
    details["vague_quantifiers"] = vague

    # Universal claims
    universal = sum(len(re.findall(rf"\b{re.escape(u)}\b", text_lower)) for u in spec["universal_claims"])
    details["universal_claims"] = universal

    # Anchor rate
    anchor_rate = strong / word_count if word_count else 0.0
    details["anchor_rate"] = round(anchor_rate, 5)

    ar_cfg = spec["anchor_rate"]
    if anchor_rate >= ar_cfg["strong"]:
        ar_pts = 0
    elif anchor_rate >= ar_cfg["moderate"]:
        ar_pts = 3
    elif anchor_rate >= ar_cfg["low"]:
        ar_pts = 6
    elif anchor_rate > 0:
        ar_pts = 9
    else:
        ar_pts = 11  # zero anchors is a very strong AI signal

    # Information density variance across paragraphs
    paras = get_paragraphs(text)
    para_densities: List[float] = []
    for p in paras:
        pw = len(get_words(p))
        if pw < 5:
            continue
        pa = 0
        for pat in spec["strong_anchor_patterns"]:
            pa += len(re.findall(pat, p))
        para_densities.append(pa / pw)

    if len(para_densities) > 1:
        density_std = statistics.pstdev(para_densities)
    else:
        density_std = 0.0
    details["info_density_std"] = round(density_std, 5)

    # Low variance = AI-like (uniform distribution)
    if density_std < 0.005:
        idv_pts = 4
    elif density_std < 0.010:
        idv_pts = 2
    else:
        idv_pts = 0

    # Vague/universal penalty (raised thresholds to avoid penalizing conversational writing)
    vague_rate = (vague + universal) / word_count if word_count else 0.0
    details["vague_rate"] = round(vague_rate, 5)
    if vague_rate > 0.025:
        vague_pts = 3
    elif vague_rate > 0.015:
        vague_pts = 1
    else:
        vague_pts = 0

    total_pts = ar_pts + idv_pts + vague_pts
    raw_max = 11 + 4 + 3  # 18
    score = min(max_w, int(round(total_pts / raw_max * max_w)))

    return FamilyScore(
        name="Specificity quality",
        key="specificity_quality",
        raw=total_pts / raw_max,
        score=score,
        max_weight=max_w,
        details=details,
    )


# ──────────────────────────────────────────────
# Family E: Vocabulary richness
# ──────────────────────────────────────────────

def score_vocabulary(text: str, rules: Dict[str, Any]) -> FamilyScore:
    max_w = rules["weights"]["vocabulary_richness"]
    voc = rules["vocabulary"]
    details: Dict[str, Any] = {}
    words_lower = get_words_lower(text)
    word_count = len(words_lower)

    # Windowed TTR
    win = voc["ttr"]["window_size"]
    if word_count >= win:
        ttrs: List[float] = []
        for i in range(0, word_count - win + 1, win // 2):
            window = words_lower[i:i + win]
            ttrs.append(len(set(window)) / len(window))
        avg_ttr = statistics.mean(ttrs) if ttrs else 0.7
    else:
        # Too short for windowed — use global TTR
        avg_ttr = len(set(words_lower)) / word_count if word_count else 0.7
    details["avg_windowed_ttr"] = round(avg_ttr, 4)

    ttr_cfg = voc["ttr"]
    if avg_ttr >= ttr_cfg["healthy_min"]:
        ttr_pts = 0
    elif avg_ttr >= ttr_cfg["moderate"]:
        ttr_pts = 1
    elif avg_ttr >= ttr_cfg["low"]:
        ttr_pts = 2
    else:
        ttr_pts = 3

    # Hapax legomena
    freq = Counter(words_lower)
    hapax_count = sum(1 for c in freq.values() if c == 1)
    unique_count = len(freq)
    hapax_ratio = hapax_count / unique_count if unique_count else 0.0
    details["hapax_ratio"] = round(hapax_ratio, 4)
    details["hapax_count"] = hapax_count
    details["unique_words"] = unique_count

    hapax_cfg = voc["hapax"]
    if hapax_ratio >= hapax_cfg["healthy_min"]:
        hapax_pts = 0
    elif hapax_ratio >= hapax_cfg["moderate"]:
        hapax_pts = 1
    elif hapax_ratio >= hapax_cfg["low"]:
        hapax_pts = 2
    else:
        hapax_pts = 3

    # Referential density (pronoun rate)
    ref_cfg = voc["referential"]
    pronouns = set(ref_cfg["pronouns"])
    pronoun_count = sum(1 for w in words_lower if w in pronouns)
    pronoun_rate = pronoun_count / word_count if word_count else 0.0
    details["pronoun_rate"] = round(pronoun_rate, 4)

    if pronoun_rate >= ref_cfg["pronoun_rate_healthy_min"]:
        ref_pts = 0
    elif pronoun_rate >= ref_cfg["pronoun_rate_low"]:
        ref_pts = 1
    else:
        ref_pts = 2

    total_pts = ttr_pts + hapax_pts + ref_pts
    raw_max = 3 + 3 + 2  # 8
    score = min(max_w, int(round(total_pts / raw_max * max_w)))

    return FamilyScore(
        name="Vocabulary richness",
        key="vocabulary_richness",
        raw=total_pts / raw_max,
        score=score,
        max_weight=max_w,
        details=details,
    )


# ──────────────────────────────────────────────
# Family F: Ownership / thought texture
# ──────────────────────────────────────────────

def score_ownership(text: str, lines: List[str], rules: Dict[str, Any]) -> FamilyScore:
    max_w = rules["weights"]["ownership_texture"]
    own = rules["ownership"]
    details: Dict[str, Any] = {}
    text_lower = f" {text.lower()} "
    word_count = len(get_words(text))

    # Decision scars
    scar_count = sum(count_phrase(text_lower, m) for m in own["decision_scar_markers"])
    details["decision_scar_count"] = scar_count

    # Ownership markers
    ownership_count = sum(count_phrase(text_lower, m) for m in own["ownership_markers"])
    details["ownership_marker_count"] = ownership_count

    # Tradeoff markers
    tradeoff_count = sum(count_phrase(text_lower, m) for m in own["tradeoff_markers"])
    details["tradeoff_count"] = tradeoff_count

    total_markers = scar_count + ownership_count + tradeoff_count
    marker_rate = total_markers / word_count if word_count else 0.0
    details["total_texture_markers"] = total_markers
    details["texture_marker_rate"] = round(marker_rate, 5)

    # Score inversely: more markers = lower (better) score
    # Also consider raw count for short texts where rate can be misleading
    if total_markers >= 8 or marker_rate >= 0.006:
        texture_pts = 0
    elif total_markers >= 4 or marker_rate >= 0.003:
        texture_pts = 2
    elif total_markers >= 2 or marker_rate >= 0.001:
        texture_pts = 4
    else:
        texture_pts = 6

    # Hedging asymmetry
    sections = split_into_sections(lines)
    section_hedge_rates: List[float] = []
    for sec_name, sec_text in sections:
        sw = len(get_words(sec_text))
        if sw < 20:
            continue
        sec_lower = sec_text.lower()
        hedge_hits = sum(
            len(re.findall(rf"\b{re.escape(h)}\b", sec_lower))
            for h in own["hedging_words"]
        )
        section_hedge_rates.append(hedge_hits / sw)

    if len(section_hedge_rates) > 1:
        hedge_var = statistics.pstdev(section_hedge_rates)
    else:
        hedge_var = 0.01  # neutral
    details["hedging_variance"] = round(hedge_var, 5)
    details["section_hedge_rates"] = [round(r, 4) for r in section_hedge_rates]

    # Low variance = AI-like uniform hedging
    if hedge_var < 0.003:
        hedge_pts = 3
    elif hedge_var < 0.008:
        hedge_pts = 1
    else:
        hedge_pts = 0

    total_pts = texture_pts + hedge_pts
    raw_max = 6 + 3  # 9
    score = min(max_w, int(round(total_pts / raw_max * max_w)))

    return FamilyScore(
        name="Ownership / thought texture",
        key="ownership_texture",
        raw=total_pts / raw_max,
        score=score,
        max_weight=max_w,
        details=details,
    )


# ──────────────────────────────────────────────
# Family G: Formatting artifacts
# ──────────────────────────────────────────────

def score_formatting(text: str, rules: Dict[str, Any]) -> FamilyScore:
    max_w = rules["weights"]["formatting_artifacts"]
    fmt = rules["formatting"]
    total_pts = 0
    details: Dict[str, Any] = {}

    # Em-dashes (already counted in cadence, but scored differently here for formatting)
    em_chars = fmt.get("em_dash_chars", ["\u2014", "--"])
    em_count = sum(text.count(c) for c in em_chars)
    details["em_dash_count"] = em_count
    if em_count > 8:
        total_pts += 3
    elif em_count > 4:
        total_pts += 2
    elif em_count > 2:
        total_pts += 1

    # Smart quote mixing
    smart_pairs = fmt.get("smart_quote_pairs", [])
    has_smart = any(text.count(p[0]) > 0 or text.count(p[1]) > 0 for p in smart_pairs)
    has_straight = '"' in text
    details["smart_quotes"] = has_smart
    details["straight_quotes"] = has_straight
    if has_smart and has_straight:
        total_pts += 2  # inconsistent mixing
    elif has_smart and not has_straight:
        total_pts += 1  # smart-only is a mild signal

    # Title-case headings (expect sentence case for this site)
    headings = re.findall(r"^#{1,6}\s+(.+)$", text, re.M)
    title_case_count = 0
    for h in headings:
        words_h = h.split()
        if len(words_h) >= 3:
            # Check if most non-trivial words are capitalized
            caps = sum(1 for w in words_h if w[0].isupper() and w.lower() not in {"a", "an", "the", "in", "on", "at", "to", "for", "of", "and", "or", "but"})
            if caps / len(words_h) > 0.7:
                title_case_count += 1
    details["title_case_headings"] = title_case_count
    if title_case_count >= 3:
        total_pts += 2
    elif title_case_count >= 1:
        total_pts += 1

    # Emoji bullets
    emoji_pattern = fmt.get("emoji_bullet_pattern", "")
    if emoji_pattern:
        emoji_bullets = len(re.findall(emoji_pattern, text, re.M))
        details["emoji_bullets"] = emoji_bullets
        if emoji_bullets >= 3:
            total_pts += 2
        elif emoji_bullets >= 1:
            total_pts += 1
    else:
        details["emoji_bullets"] = 0

    # Stock photo artifacts
    stock_patterns = fmt.get("stock_photo_patterns", [])
    stock_hits = 0
    for sp in stock_patterns:
        stock_hits += len(re.findall(re.escape(sp), text, re.I))
    details["stock_photo_hits"] = stock_hits
    if stock_hits > 0:
        total_pts += 2

    raw_max = 3 + 2 + 2 + 2 + 2  # 11
    score = min(max_w, int(round(total_pts / raw_max * max_w)))

    return FamilyScore(
        name="Formatting artifacts",
        key="formatting_artifacts",
        raw=total_pts / raw_max,
        score=score,
        max_weight=max_w,
        details=details,
    )


# ──────────────────────────────────────────────
# Family H: Hard artifacts
# ──────────────────────────────────────────────

def score_hard_artifacts(text: str, rules: Dict[str, Any]) -> FamilyScore:
    max_w = rules["weights"]["hard_artifacts"]
    hard = rules["hard_artifacts"]
    total_pts = 0
    details: Dict[str, Any] = {}

    # Placeholders
    placeholder_count = 0
    for pat in hard["placeholder_patterns"]:
        placeholder_count += len(re.findall(pat, text, re.I))
    details["placeholders"] = placeholder_count
    if placeholder_count >= 2:
        total_pts += 3
    elif placeholder_count >= 1:
        total_pts += 2

    # AI self-reference
    text_lower = text.lower()
    ai_ref_count = 0
    for phrase in hard["ai_self_reference"]:
        ai_ref_count += text_lower.count(phrase.lower())
    details["ai_self_references"] = ai_ref_count
    if ai_ref_count > 0:
        total_pts += 3

    # Register flips (simplified: check co-occurrence of academic + casual)
    reg = hard.get("register_flip_markers", {})
    academic_hits = sum(text_lower.count(p.lower()) for p in reg.get("academic", []))
    casual_hits = sum(text_lower.count(p.lower()) for p in reg.get("casual", []))
    details["academic_register_hits"] = academic_hits
    details["casual_register_hits"] = casual_hits
    if academic_hits > 0 and casual_hits > 0:
        total_pts += 2

    # Stock photo lines (already counted in G, but hard artifacts too)
    stock_patterns = rules["formatting"].get("stock_photo_patterns", [])
    stock_hits = sum(len(re.findall(re.escape(sp), text, re.I)) for sp in stock_patterns)
    details["stock_photo_artifacts"] = stock_hits
    if stock_hits > 0:
        total_pts += 2

    raw_max = 3 + 3 + 2 + 2  # 10
    score = min(max_w, int(round(total_pts / raw_max * max_w)))

    return FamilyScore(
        name="Hard artifacts",
        key="hard_artifacts",
        raw=total_pts / raw_max,
        score=score,
        max_weight=max_w,
        details=details,
    )


# ──────────────────────────────────────────────
# Line-level flags
# ──────────────────────────────────────────────

def gather_flags(lines: List[str], rules: Dict[str, Any]) -> List[Flag]:
    flag_defs = rules.get("line_flags", [])
    flags: List[Flag] = []
    for lineno, line in enumerate(lines, start=1):
        raw_line = line.rstrip("\n")
        if not raw_line.strip():
            continue
        sec = section_for_line(lines, lineno)
        for fd in flag_defs:
            try:
                rx = re.compile(fd["pattern"], re.I)
            except re.error:
                continue
            if rx.search(raw_line):
                flags.append(Flag(
                    lineno=lineno,
                    section=sec,
                    quote=raw_line.strip(),
                    family=f"Family {fd['family']}",
                    strength=fd["strength"],
                    why=fd["why"],
                    rewrite_direction=fd["rewrite"],
                ))
                break  # one flag per line (highest-priority match)
    # Deduplicate
    seen: set = set()
    unique: List[Flag] = []
    for f in flags:
        key = (f.lineno, f.quote)
        if key not in seen:
            seen.add(key)
            unique.append(f)
    return unique


# ──────────────────────────────────────────────
# Derived evidence flags (to satisfy evidence-first reporting)
# ──────────────────────────────────────────────

def _is_prose_line(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    # Skip headings and common markdown scaffolding
    if s.startswith("#") or s.startswith(">") or s.startswith("```"):
        return False
    if re.match(r"^(\*|-|\d+\.)\s+", s):
        return False
    return True


def _find_line_matches(lines: List[str], patterns: List[str]) -> List[Tuple[int, str, int]]:
    """
    Return [(lineno, line, hit_count)] for lines that match any pattern.
    Uses case-insensitive regex search, counts total matches across patterns.
    """
    compiled: List[re.Pattern[str]] = []
    for p in patterns:
        try:
            compiled.append(re.compile(p, re.I))
        except re.error:
            continue
    hits: List[Tuple[int, str, int]] = []
    for i, line in enumerate(lines, start=1):
        raw = line.rstrip("\n")
        if not raw.strip():
            continue
        c = 0
        for rx in compiled:
            c += len(rx.findall(raw))
        if c > 0:
            hits.append((i, raw.strip(), c))
    return hits


def derive_evidence_flags(
    lines: List[str],
    text: str,
    rules: Dict[str, Any],
    family_scores: List[FamilyScore],
    max_per_family: int = 4,
) -> List[Flag]:
    """
    Generate additional line-level flags based on the rule registry and
    the computed family scores, so a high overall score always comes with
    evidence quotes + locations + rewrite directions.
    """
    flags: List[Flag] = []
    score_map = {fs.key: fs for fs in family_scores}

    # Family A: lexicon / phrase clusters — show densest lines with safe-words/fillers
    lex = rules.get("lexicon", {})
    lex_terms: List[str] = []
    for group in ["verbs", "nouns", "adjectives", "fillers", "modern_ai_terms"]:
        lex_terms.extend(lex.get(group, []))
    if lex_terms:
        # Build regex patterns for each term (word-boundary for single words)
        pats = []
        for t in lex_terms:
            t = t.strip()
            if not t:
                continue
            if " " in t:
                pats.append(re.escape(t))
            else:
                pats.append(rf"\b{re.escape(t)}\b")
        hits = _find_line_matches(lines, pats)
        hits.sort(key=lambda x: (-x[2], x[0]))
        for lineno, quote, count in hits[:max_per_family]:
            if not _is_prose_line(quote):
                continue
            flags.append(Flag(
                lineno=lineno,
                section=section_for_line(lines, lineno),
                quote=quote,
                family="Family A",
                strength="medium" if count < 2 else "high",
                why=f"Lexicon/template phrasing clusters here ({count} hit(s) on the safe-lexicon list).",
                rewrite_direction="Rewrite in plainer language. Remove filler phrases; add one concrete mechanism or example right after the claim.",
            ))

    # Family C: structural patterns — show exact template-y lines
    struct = rules.get("structural", {})
    neg_pats = struct.get("negative_parallelism", {}).get("patterns", [])
    sym_pats = struct.get("symmetric_contrast", {}).get("patterns", [])
    r3_pat = r"\b\w+\b,\s+\b\w+\b,\s+and\s+\b\w+\b"
    for family, pats, why, rewrite in [
        ("Family C", neg_pats, "Negative parallelism template ('not just X, but Y') pattern.", "Keep the idea, but rewrite without the rhetorical scaffold; add the specific decision or tradeoff it’s pointing at."),
        ("Family C", sym_pats, "Symmetric contrast template ('from X to Y') pattern.", "Replace the symmetry with the real causal sequence: what happened, what constraint changed, what you did next."),
        ("Family C", [r3_pat], "Rule-of-three cadence pattern can read template-like when repeated.", "If you keep the list, make the third item concrete (not a vague synonym) or collapse to 1–2 items."),
    ]:
        if not pats:
            continue
        hits = _find_line_matches(lines, pats)
        hits.sort(key=lambda x: (-x[2], x[0]))
        for lineno, quote, _ in hits[:max_per_family]:
            if not quote.strip():
                continue
            flags.append(Flag(
                lineno=lineno,
                section=section_for_line(lines, lineno),
                quote=quote,
                family=family,
                strength="medium",
                why=why,
                rewrite_direction=rewrite,
            ))

    # Family B/G: em-dash heavy lines (actionable micro-edits)
    em_lines = []
    for i, line in enumerate(lines, start=1):
        raw = line.rstrip("\n").strip()
        if not raw:
            continue
        c = raw.count("\u2014") + raw.count("--")
        if c >= 1 and _is_prose_line(raw):
            em_lines.append((i, raw, c))
    em_lines.sort(key=lambda x: (-x[2], x[0]))
    for lineno, quote, c in em_lines[:max(2, max_per_family // 2)]:
        flags.append(Flag(
            lineno=lineno,
            section=section_for_line(lines, lineno),
            quote=quote,
            family="Family G",
            strength="low" if c == 1 else "medium",
            why=f"Em-dash usage here ({c} occurrence(s) on this line) contributes to an AI-ish punctuation fingerprint.",
            rewrite_direction="Replace em-dashes with a colon (definition), parentheses (aside), comma (pause), or semicolon (two independent clauses).",
        ))

    # Family D/F: low-specificity prompts — anchor prompts with a real quote
    spec = score_map.get("specificity_quality")
    if spec and spec.details.get("strong_anchors", 0) < 2:
        # Choose a representative prose line (first substantive prose line)
        for i, line in enumerate(lines, start=1):
            raw = line.rstrip("\n").strip()
            if _is_prose_line(raw) and len(get_words(raw)) >= 8:
                flags.append(Flag(
                    lineno=i,
                    section=section_for_line(lines, i),
                    quote=raw,
                    family="Family D",
                    strength="high",
                    why="This section reads claim-heavy but low on anchors (dates, numbers, named systems/incidents, constraints). Low-anchor writing is a strong AI-likeness driver.",
                    rewrite_direction="Add 1–2 anchors: a time window, a measurable outcome, and a concrete constraint/tradeoff. Use `[placeholder: …]` if needed.",
                ))
                break

    # Family F: low-ownership prompts — add scars/tradeoffs
    own = score_map.get("ownership_texture")
    if own and own.details.get("total_texture_markers", 0) < 2:
        for i, line in enumerate(lines, start=1):
            raw = line.rstrip("\n").strip()
            if _is_prose_line(raw) and len(get_words(raw)) >= 8:
                flags.append(Flag(
                    lineno=i,
                    section=section_for_line(lines, i),
                    quote=raw,
                    family="Family F",
                    strength="medium",
                    why="Low ownership/decision-scar texture: it’s hard to see what you chose, what failed, and what tradeoff you accepted.",
                    rewrite_direction="Add one sentence with a decision scar: 'We tried X, it failed because Y, so we changed to Z.' Or add one explicit tradeoff.",
                ))
                break

    # De-dupe (lineno + quote)
    seen = set()
    uniq: List[Flag] = []
    for f in flags:
        k = (f.lineno, f.quote)
        if k in seen:
            continue
        seen.add(k)
        uniq.append(f)
    return uniq


# ──────────────────────────────────────────────
# Cluster boosts
# ──────────────────────────────────────────────

def apply_cluster_boosts(
    family_scores: List[FamilyScore],
    rules: Dict[str, Any],
) -> List[Tuple[str, int]]:
    boosts: List[Tuple[str, int]] = []
    boost_defs = rules.get("cluster_boosts", [])

    # Build a lookup for easy condition checking
    details_map: Dict[str, Any] = {}
    score_map: Dict[str, FamilyScore] = {}
    for fs in family_scores:
        score_map[fs.key] = fs
        for k, v in fs.details.items():
            details_map[k] = v

    for bd in boost_defs:
        conditions = bd["conditions"]
        all_met = True
        for cond_key, cond_val in conditions.items():
            # Parse condition: key_operator -> lookup the detail
            if cond_key.endswith("_gt"):
                metric = cond_key[:-3]
                val = details_map.get(metric)
                if val is None or not (val > cond_val):
                    all_met = False
            elif cond_key.endswith("_gte"):
                metric = cond_key[:-4]
                val = details_map.get(metric)
                if val is None or not (val >= cond_val):
                    all_met = False
            elif cond_key.endswith("_lt"):
                metric = cond_key[:-3]
                val = details_map.get(metric)
                if val is None or not (val < cond_val):
                    all_met = False
            elif cond_key == "specificity_score_pct_gt":
                fs = score_map.get("specificity_quality")
                if fs is None or not (fs.score / fs.max_weight > cond_val):
                    all_met = False
            elif cond_key == "avg_windowed_ttr_lt":
                val = details_map.get("avg_windowed_ttr")
                if val is None or not (val < cond_val):
                    all_met = False
            else:
                all_met = False  # unknown condition
        if all_met:
            boosts.append((bd["name"], bd["boost"]))

    return boosts


# ──────────────────────────────────────────────
# Classification
# ──────────────────────────────────────────────

def classify(score: int, rules: Dict[str, Any]) -> str:
    bands = rules["classification"]
    if score <= bands["likely_human"][1]:
        return "Likely Human"
    if score <= bands["ambiguous_hybrid"][1]:
        return "Ambiguous / Hybrid"
    if score <= bands["probably_ai_assisted"][1]:
        return "Probably AI-Assisted"
    return "Likely AI-Generated"


def detect_dialect(flags: List[Flag], family_scores: List[FamilyScore], channel: str) -> str:
    score_map = {fs.key: fs for fs in family_scores}
    if any("LinkedIn" in f.family or "LinkedIn" in f.why for f in flags):
        return "LinkedIn-Template"

    struct = score_map.get("structural_symmetry")
    spec = score_map.get("specificity_quality")
    if struct and spec and struct.score >= struct.max_weight * 0.6 and spec.score >= spec.max_weight * 0.5:
        return "Corporate-Generic"

    if channel.lower() in {"marketing", "landing-page"} and struct and struct.score >= struct.max_weight * 0.6:
        return "Marketing-Polish"

    return "None"


# ──────────────────────────────────────────────
# Cluster inference guard
# ──────────────────────────────────────────────

def enforce_cluster_inference(
    final_score: int,
    family_scores: List[FamilyScore],
    rules: Dict[str, Any],
) -> int:
    """
    Never classify above Ambiguous/Hybrid unless at least N families
    score above 50% of their max weight.
    """
    min_families = rules.get("cluster_inference_min_families", 3)
    ambiguous_max = rules["classification"]["ambiguous_hybrid"][1]

    families_above_50 = sum(
        1 for fs in family_scores
        if fs.max_weight > 0 and (fs.score / fs.max_weight) > 0.5
    )

    if final_score > ambiguous_max and families_above_50 < min_families:
        return ambiguous_max  # cap at top of ambiguous band

    return final_score


# ──────────────────────────────────────────────
# Main analysis
# ──────────────────────────────────────────────

def analyze(file_path: str, text: str, rules: Dict[str, Any],
            channel: str = "blog", intent: str = "inform",
            author_profile: str = "unknown", topic: str = "") -> Report:
    lines = text.replace("\r\n", "\n").split("\n")
    words = get_words(text)
    word_count = len(words)
    sents = get_sentences(text)
    paras = get_paragraphs(text)

    # Score all 8 families
    fs_a = score_lexicon(text, rules)
    fs_b = score_cadence(text, rules)
    fs_c = score_structural(text, lines, rules)
    fs_d = score_specificity(text, lines, rules)
    fs_e = score_vocabulary(text, rules)
    fs_f = score_ownership(text, lines, rules)
    fs_g = score_formatting(text, rules)
    fs_h = score_hard_artifacts(text, rules)
    family_scores = [fs_a, fs_b, fs_c, fs_d, fs_e, fs_f, fs_g, fs_h]

    # Short-text normalization
    short_cfg = rules.get("short_text", {})
    short_warning = word_count < short_cfg.get("word_count_threshold", 300)
    if short_warning:
        exempt = set(short_cfg.get("exempt_families", []))
        multiplier = short_cfg.get("weight_multiplier", 0.5)
        for fs in family_scores:
            if fs.key not in exempt:
                fs.score = int(round(fs.score * multiplier))

    # Base score
    base_score = sum(fs.score for fs in family_scores)

    # Cluster boosts
    boosts = apply_cluster_boosts(family_scores, rules)
    boost_total = sum(b for _, b in boosts)

    raw_final = min(100, base_score + boost_total)
    if short_warning:
        raw_final = min(short_cfg.get("max_score", 60), raw_final)

    # Cluster inference guard
    final_score = enforce_cluster_inference(raw_final, family_scores, rules)

    classification = classify(final_score, rules)

    # Flags
    flags = gather_flags(lines, rules)
    # Ensure evidence-first: derive additional evidence flags from computed signals.
    derived = derive_evidence_flags(lines, text, rules, family_scores)
    if derived:
        flags = flags + derived
        # Deduplicate (lineno + quote)
        seen = set()
        deduped: List[Flag] = []
        for f in flags:
            k = (f.lineno, f.quote)
            if k in seen:
                continue
            seen.add(k)
            deduped.append(f)
        flags = deduped

    dialect = detect_dialect(flags, family_scores, channel)

    # If score is high but evidence is thin, cap to avoid false precision.
    # (Still returns the computed family scores, so an editor can see drivers.)
    if final_score >= 60 and len(flags) < 5:
        final_score = min(final_score, rules["classification"]["ambiguous_hybrid"][1])
        classification = classify(final_score, rules)

    return Report(
        file_path=file_path,
        word_count=word_count,
        sentence_count=len(sents),
        paragraph_count=len(paras),
        family_scores=family_scores,
        cluster_boosts=boosts,
        base_score=base_score,
        boost_total=boost_total,
        final_score=final_score,
        classification=classification,
        dialect=dialect,
        flags=flags,
        short_text_warning=short_warning,
    )


# ──────────────────────────────────────────────
# Output: human-readable
# ──────────────────────────────────────────────

def print_report(report: Report, verbose: bool = False,
                 channel: str = "blog", intent: str = "inform",
                 author_profile: str = "unknown", topic: str = "",
                 max_flags: int = 15) -> None:
    r = report

    # 1) Executive Summary
    print("=" * 70)
    print("AI WRITING FORENSICS — UNIFIED REPORT")
    print("=" * 70)
    print(f"\n1) Executive Summary")
    print(f"   Score: {r.final_score}/100 ({r.classification})")
    print(f"   Dialect: {r.dialect}")
    print(f"   Context: channel={channel}, intent={intent}, "
          f"author_profile={author_profile}, topic={topic or '(none)'}")
    if r.short_text_warning:
        print(f"   WARNING: Short text ({r.word_count} words) — scores are less reliable.")
    print(f"   Words: {r.word_count} | Sentences: {r.sentence_count} | "
          f"Paragraphs: {r.paragraph_count}")

    # Main drivers
    print("\n   Main drivers:")
    for fs in sorted(r.family_scores, key=lambda x: x.score / max(x.max_weight, 1), reverse=True):
        pct = fs.score / fs.max_weight * 100 if fs.max_weight else 0
        if pct >= 50:
            print(f"   - {fs.name}: {fs.score}/{fs.max_weight} ({pct:.0f}%) — contributing")
        elif pct == 0:
            print(f"   - {fs.name}: {fs.score}/{fs.max_weight} — clean")
    if r.cluster_boosts:
        for name, pts in r.cluster_boosts:
            print(f"   - Cluster boost '{name}': +{pts}")

    # 2) Component Breakdown
    print(f"\n{'─' * 70}")
    print("2) Component Breakdown")
    print(f"{'─' * 70}")
    for fs in r.family_scores:
        pct = fs.score / fs.max_weight * 100 if fs.max_weight else 0
        bar = "█" * int(pct / 10) + "░" * (10 - int(pct / 10))
        print(f"   {fs.name:42s} {fs.score:2d}/{fs.max_weight:2d}  {bar}")
    print(f"   {'Base score':42s} {r.base_score:2d}/100")
    if r.cluster_boosts:
        print(f"   {'Cluster boosts':42s} +{r.boost_total}")
    print(f"   {'FINAL SCORE':42s} {r.final_score:2d}/100")
    print()

    # What NOT to over-edit
    print("   What NOT to over-edit:")
    for fs in r.family_scores:
        if fs.score == 0:
            print(f"   - {fs.name} is clean — no edits needed here.")

    # 3) Top Red Flags
    print(f"\n{'─' * 70}")
    print("3) Top Red Flags (Evidence Quotes)")
    print(f"{'─' * 70}")
    sev_order = {"high": 0, "medium": 1, "low": 2}
    sorted_flags = sorted(r.flags, key=lambda f: (sev_order.get(f.strength, 9), f.lineno))
    top_flags = sorted_flags[:max_flags]
    if not top_flags:
        print("   No high-signal lines matched. (Does NOT prove the draft is human.)")
    else:
        for f in top_flags:
            print(f"\n   Line {f.lineno} [{f.strength}] ({f.family})")
            print(f"   Quote: \"{f.quote[:100]}{'...' if len(f.quote) > 100 else ''}\"")
            print(f"   Why: {f.why}")
            print(f"   Rewrite: {f.rewrite_direction}")

    # 4) Deep Forensic Findings (verbose only)
    if verbose:
        print(f"\n{'─' * 70}")
        print("4) Deep Forensic Findings")
        print(f"{'─' * 70}")
        for fs in r.family_scores:
            print(f"\n   ## {fs.name} ({fs.score}/{fs.max_weight})")
            for k, v in fs.details.items():
                if isinstance(v, float):
                    print(f"      {k}: {v:.4f}")
                elif isinstance(v, list) and len(v) > 5:
                    print(f"      {k}: [{', '.join(str(x) for x in v[:5])}, ... ({len(v)} total)]")
                else:
                    print(f"      {k}: {v}")

    # 5) Section-wise guidance (from flags)
    print(f"\n{'─' * 70}")
    print("5) Actionable Rewrite Guidance")
    print(f"{'─' * 70}")
    if not top_flags:
        print("   No section-wise guidance generated (no flags matched).")
    else:
        sections_seen: Dict[str, List[Flag]] = {}
        for f in top_flags:
            sections_seen.setdefault(f.section, []).append(f)
        for sec, sec_flags in sections_seen.items():
            print(f"\n   ## {sec}")
            for f in sec_flags[:6]:
                print(f"   - Line {f.lineno}: \"{f.quote[:80]}{'...' if len(f.quote) > 80 else ''}\"")
                print(f"     Fix: {f.rewrite_direction}")

    print()


# ──────────────────────────────────────────────
# Output: JSON
# ──────────────────────────────────────────────

def report_to_dict(report: Report) -> Dict[str, Any]:
    return {
        "file_path": report.file_path,
        "word_count": report.word_count,
        "sentence_count": report.sentence_count,
        "paragraph_count": report.paragraph_count,
        "base_score": report.base_score,
        "boost_total": report.boost_total,
        "final_score": report.final_score,
        "classification": report.classification,
        "dialect": report.dialect,
        "short_text_warning": report.short_text_warning,
        "family_scores": [
            {
                "name": fs.name,
                "key": fs.key,
                "score": fs.score,
                "max_weight": fs.max_weight,
                "raw": round(fs.raw, 5),
                "details": fs.details,
            }
            for fs in report.family_scores
        ],
        "cluster_boosts": [
            {"name": name, "boost": boost}
            for name, boost in report.cluster_boosts
        ],
        "flags": [
            {
                "lineno": f.lineno,
                "section": f.section,
                "quote": f.quote,
                "family": f.family,
                "strength": f.strength,
                "why": f.why,
                "rewrite_direction": f.rewrite_direction,
            }
            for f in report.flags
        ],
    }


# ──────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="AI Writing Forensics — Unified Engine"
    )
    parser.add_argument("--file", "-f", required=True,
                        help="Path to markdown/text file to analyze")
    parser.add_argument("--channel", default="blog",
                        help="Context: blog / LinkedIn / memo / marketing / email")
    parser.add_argument("--author-profile", default="unknown",
                        help="Author type: technical / exec / non-native / unknown")
    parser.add_argument("--intent", default="inform",
                        help="Purpose: persuade / inform / narrate / announce / explain / sell")
    parser.add_argument("--topic", default="",
                        help="Short topic label")
    parser.add_argument("--max-flags", type=int, default=15,
                        help="Max items in Top Red Flags section")
    parser.add_argument("--json", action="store_true",
                        help="Output JSON instead of human-readable report")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Include deep forensic findings")
    parser.add_argument("--rules", default=str(RULES_PATH),
                        help="Path to rules JSON (default: ai_forensics_rules.json)")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"Error: File not found: {path}", file=sys.stderr)
        return 1

    rules_path = Path(args.rules)
    if not rules_path.exists():
        print(f"Error: Rules file not found: {rules_path}", file=sys.stderr)
        return 1

    rules = load_rules(rules_path)

    raw = path.read_text(encoding="utf-8")
    body = strip_frontmatter(raw)

    report = analyze(
        file_path=str(path),
        text=body,
        rules=rules,
        channel=args.channel,
        intent=args.intent,
        author_profile=args.author_profile,
        topic=args.topic,
    )

    if args.json:
        print(json.dumps(report_to_dict(report), indent=2))
    else:
        print_report(
            report,
            verbose=args.verbose,
            channel=args.channel,
            intent=args.intent,
            author_profile=args.author_profile,
            topic=args.topic,
            max_flags=args.max_flags,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
