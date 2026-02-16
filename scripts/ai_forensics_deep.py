#!/usr/bin/env python3
"""
AI Writing Forensics — Deep Analysis Module.

DEPRECATED: This script has been superseded by scripts/ai_forensics_unified.py.
Use the unified script for all new analyses. This script is kept for backward
compatibility and will be removed in a future cleanup.

Extends the base forensics script with additional signal detection:
- N-gram frequency analysis (detecting repetitive phrases)
- Sentence starter patterns (AI tends to overuse certain openings)
- Transition word density analysis
- One-sentence paragraph detection (LinkedIn "broetry")
- Hedging language detection
- Blockquote/callout density
- Specificity ratio (concrete details vs abstract claims)

Supports the rubric in `docs/agent-skills/ai-detection-2.md`.

Usage:
  python3 scripts/ai_forensics_deep.py --file content/writing/<post>.md [--json] [--verbose]
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Tuple, Optional


WORD_RE = re.compile(r"[A-Za-z][A-Za-z'_-]*")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def strip_frontmatter(raw: str) -> str:
    """Remove YAML or TOML frontmatter from markdown."""
    if raw.startswith("---\n"):
        return re.sub(r"^---.*?---\s*", "", raw, flags=re.S)
    if raw.startswith("+++\n"):
        return re.sub(r"^\+\+\+.*?\+\+\+\s*", "", raw, flags=re.S)
    return raw


def get_sentences(text: str) -> List[str]:
    """Split text into sentences."""
    flat = re.sub(r"\s+", " ", text).strip()
    sents = [s.strip() for s in SENTENCE_SPLIT_RE.split(flat) if s.strip()]
    return sents


def get_words(text: str) -> List[str]:
    """Extract words from text."""
    return WORD_RE.findall(text.lower())


def get_ngrams(words: List[str], n: int) -> List[Tuple[str, ...]]:
    """Generate n-grams from word list."""
    return [tuple(words[i:i+n]) for i in range(len(words) - n + 1)]


@dataclass
class NgramAnalysis:
    """N-gram frequency analysis results."""
    bigram_repeats: List[Tuple[str, int]]  # (phrase, count) for count >= 3
    trigram_repeats: List[Tuple[str, int]]
    quadgram_repeats: List[Tuple[str, int]]
    total_bigrams: int
    total_trigrams: int
    repetition_score: int  # 0-100, higher = more repetitive


def analyze_ngrams(text: str) -> NgramAnalysis:
    """Analyze n-gram frequencies to detect repetitive AI patterns."""
    words = get_words(text)
    
    bigrams = Counter(get_ngrams(words, 2))
    trigrams = Counter(get_ngrams(words, 3))
    quadgrams = Counter(get_ngrams(words, 4))
    
    # Filter to meaningful repeats (3+ occurrences)
    bigram_repeats = [(" ".join(k), v) for k, v in bigrams.most_common(20) if v >= 3]
    trigram_repeats = [(" ".join(k), v) for k, v in trigrams.most_common(15) if v >= 3]
    quadgram_repeats = [(" ".join(k), v) for k, v in quadgrams.most_common(10) if v >= 2]
    
    # Score: more unusual repetition = higher score
    score = 0
    score += min(30, len(trigram_repeats) * 5)
    score += min(40, len(quadgram_repeats) * 10)
    # Penalize very high repetition of certain phrases
    if any(c >= 5 for _, c in trigram_repeats):
        score += 15
    
    return NgramAnalysis(
        bigram_repeats=bigram_repeats,
        trigram_repeats=trigram_repeats,
        quadgram_repeats=quadgram_repeats,
        total_bigrams=len(bigrams),
        total_trigrams=len(trigrams),
        repetition_score=min(100, score),
    )


@dataclass
class SentenceStarterAnalysis:
    """Analysis of sentence opening patterns."""
    starter_counts: Dict[str, int]  # normalized first word/phrase -> count
    top_starters: List[Tuple[str, int]]
    pronoun_heavy: bool  # >40% start with we/I/they/it
    variety_score: int  # 0-100, higher = more varied (good)


# Common AI sentence starters to watch for
AI_SENTENCE_STARTERS = [
    "this", "that", "it", "we", "the", "in", "for", "when", "if",
    "once", "most", "many", "some", "all", "by", "at", "from", "to"
]

def analyze_sentence_starters(text: str) -> SentenceStarterAnalysis:
    """Analyze sentence opening patterns."""
    sentences = get_sentences(text)
    
    starters: Counter[str] = Counter()
    pronoun_starts = 0
    
    for sent in sentences:
        words = get_words(sent)
        if not words:
            continue
        first = words[0].lower()
        starters[first] += 1
        if first in ["we", "i", "they", "it", "he", "she"]:
            pronoun_starts += 1
    
    total_sents = len(sentences)
    pronoun_heavy = (pronoun_starts / total_sents) > 0.4 if total_sents else False
    
    # Variety score: how many unique starters vs total sentences
    unique_ratio = len(starters) / total_sents if total_sents else 0
    variety_score = min(100, int(unique_ratio * 150))  # 0.66 unique ratio = 100
    
    return SentenceStarterAnalysis(
        starter_counts=dict(starters),
        top_starters=starters.most_common(10),
        pronoun_heavy=pronoun_heavy,
        variety_score=variety_score,
    )


@dataclass
class TransitionAnalysis:
    """Analysis of transition word usage."""
    transition_count: int
    transition_density: float  # transitions per 100 words
    flagged_transitions: List[Tuple[str, int]]  # overused transitions
    score: int  # 0-100, higher = more AI-like overuse


TRANSITION_WORDS = [
    "however", "moreover", "furthermore", "additionally", "consequently",
    "therefore", "thus", "hence", "accordingly", "meanwhile",
    "nevertheless", "nonetheless", "conversely", "similarly",
    "specifically", "particularly", "notably", "importantly",
    "essentially", "fundamentally", "ultimately", "basically",
]

def analyze_transitions(text: str) -> TransitionAnalysis:
    """Analyze transition word density."""
    lower = text.lower()
    words = get_words(text)
    word_count = len(words)
    
    counts: Dict[str, int] = {}
    total = 0
    for t in TRANSITION_WORDS:
        c = len(re.findall(rf"\b{re.escape(t)}\b", lower))
        if c > 0:
            counts[t] = c
            total += c
    
    density = (total / word_count * 100) if word_count else 0
    
    # Flag overused (2+ occurrences in short text, 4+ in longer)
    threshold = 2 if word_count < 1000 else 4
    flagged = [(t, c) for t, c in counts.items() if c >= threshold]
    
    # Score: high density or flagged transitions = higher score
    score = 0
    if density > 2.0:
        score += 30
    elif density > 1.0:
        score += 15
    score += min(40, len(flagged) * 10)
    
    return TransitionAnalysis(
        transition_count=total,
        transition_density=round(density, 3),
        flagged_transitions=flagged,
        score=min(100, score),
    )


@dataclass
class ParagraphStructureAnalysis:
    """Analysis of paragraph structure patterns."""
    total_paragraphs: int
    one_sentence_paragraphs: int
    one_sentence_ratio: float
    avg_sentences_per_para: float
    broetry_score: int  # 0-100, higher = more LinkedIn-style


def analyze_paragraph_structure(text: str) -> ParagraphStructureAnalysis:
    """Detect LinkedIn 'broetry' patterns (short one-sentence paragraphs)."""
    # Split into paragraphs (double newline)
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    
    # Filter out headings, lists, blockquotes
    prose_paras = []
    for p in paragraphs:
        lines = p.split("\n")
        # Skip if starts with #, >, -, *, number
        if lines and re.match(r"^(#{1,6}\s|>|\s*[-*]\s|\s*\d+\.\s)", lines[0]):
            continue
        prose_paras.append(p)
    
    one_sentence = 0
    total_sentences = 0
    
    for para in prose_paras:
        sents = get_sentences(para)
        if len(sents) == 1:
            one_sentence += 1
        total_sentences += len(sents)
    
    total_paras = len(prose_paras)
    one_sent_ratio = (one_sentence / total_paras) if total_paras else 0
    avg_sents = (total_sentences / total_paras) if total_paras else 0
    
    # Broetry score: many short paragraphs = higher
    score = 0
    if one_sent_ratio > 0.5:
        score += 50
    elif one_sent_ratio > 0.3:
        score += 25
    elif one_sent_ratio > 0.15:
        score += 10
    
    return ParagraphStructureAnalysis(
        total_paragraphs=total_paras,
        one_sentence_paragraphs=one_sentence,
        one_sentence_ratio=round(one_sent_ratio, 3),
        avg_sentences_per_para=round(avg_sents, 2),
        broetry_score=score,
    )


@dataclass
class HedgingAnalysis:
    """Analysis of hedging language."""
    hedge_count: int
    hedge_density: float  # per 100 words
    hedge_phrases: List[Tuple[str, int]]
    score: int  # 0-100, higher = more hedging


HEDGE_PATTERNS = [
    r"\bmay\b", r"\bmight\b", r"\bcould\b", r"\bperhaps\b",
    r"\bpossibly\b", r"\bpotentially\b", r"\bgenerally\b",
    r"\btypically\b", r"\busually\b", r"\boften\b",
    r"\btends to\b", r"\bseems to\b", r"\bappears to\b",
    r"\bit is likely\b", r"\bin some cases\b", r"\bin many cases\b",
    r"\bcan be\b", r"\bmay be\b", r"\bmight be\b",
]

def analyze_hedging(text: str) -> HedgingAnalysis:
    """Analyze hedging language density."""
    lower = text.lower()
    words = get_words(text)
    word_count = len(words)
    
    counts: List[Tuple[str, int]] = []
    total = 0
    
    for pattern in HEDGE_PATTERNS:
        matches = len(re.findall(pattern, lower))
        if matches > 0:
            # Clean up pattern for display
            display = pattern.replace(r"\b", "").replace("\\", "")
            counts.append((display, matches))
            total += matches
    
    density = (total / word_count * 100) if word_count else 0
    
    # Score
    score = 0
    if density > 3.0:
        score += 40
    elif density > 2.0:
        score += 25
    elif density > 1.0:
        score += 10
    
    return HedgingAnalysis(
        hedge_count=total,
        hedge_density=round(density, 3),
        hedge_phrases=sorted(counts, key=lambda x: -x[1]),
        score=min(100, score),
    )


@dataclass
class BlockquoteAnalysis:
    """Analysis of blockquote/callout usage."""
    blockquote_count: int
    blockquote_ratio: float  # blockquotes per 500 words
    blockquote_texts: List[str]
    aphorism_score: int  # 0-100, higher = more "portable wisdom" style


def analyze_blockquotes(text: str) -> BlockquoteAnalysis:
    """Analyze blockquote density and content."""
    words = get_words(text)
    word_count = len(words)
    
    # Find blockquotes (lines starting with >)
    blockquotes = re.findall(r"^>\s*(.+)$", text, flags=re.M)
    
    ratio = (len(blockquotes) / word_count * 500) if word_count else 0
    
    # Aphorism detection: short, pithy, no specific details
    aphorism_markers = 0
    for bq in blockquotes:
        words_in_bq = len(get_words(bq))
        # Short blockquotes with universal language
        if words_in_bq < 30:
            aphorism_markers += 1
        if re.search(r"\b(always|never|every|all|no one)\b", bq, re.I):
            aphorism_markers += 1
    
    score = 0
    if len(blockquotes) >= 4:
        score += 20
    if aphorism_markers >= 3:
        score += 30
    
    return BlockquoteAnalysis(
        blockquote_count=len(blockquotes),
        blockquote_ratio=round(ratio, 3),
        blockquote_texts=blockquotes[:5],  # First 5
        aphorism_score=min(100, score),
    )


@dataclass
class SpecificityAnalysis:
    """Analysis of specificity vs abstraction."""
    specific_markers: int  # numbers, dates, names, acronyms
    abstract_markers: int  # vague quantifiers, generic claims
    specificity_ratio: float
    sections_needing_anchors: List[str]
    score: int  # 0-100, higher = more abstract (bad)


def analyze_specificity(text: str, lines: List[str]) -> SpecificityAnalysis:
    """Measure ratio of specific details to abstract claims."""
    # Specific markers
    numbers = len(re.findall(r"\b\d+(?:\.\d+)?%?\b", text))
    dates = len(re.findall(r"\b20\d{2}\b", text))
    acronyms = len(re.findall(r"\b[A-Z]{2,}\b", text))
    named_entities = len(re.findall(r"\b(?:SQL|API|JSON|RBAC|WAF|CFO)\b", text))
    specifics = numbers + dates + acronyms + named_entities
    
    # Abstract markers (vague quantifiers)
    vague = len(re.findall(
        r"\b(many|most|some|often|usually|generally|typically|sometimes|various|several)\b",
        text, re.I
    ))
    
    # Universal claims
    universal = len(re.findall(
        r"\b(always|never|everyone|no one|every|all)\b",
        text, re.I
    ))
    
    abstract = vague + universal
    
    word_count = len(get_words(text))
    spec_rate = specifics / word_count if word_count else 0
    abs_rate = abstract / word_count if word_count else 0
    
    ratio = spec_rate / abs_rate if abs_rate > 0 else spec_rate * 10
    
    # Find sections that need more anchors
    sections_needing = []
    current_section = "Intro"
    section_specifics = 0
    section_words = 0
    
    for i, line in enumerate(lines):
        if line.startswith("## "):
            # Check previous section
            if section_words > 100 and section_specifics / section_words < 0.01:
                sections_needing.append(current_section)
            current_section = line[3:].strip()
            section_specifics = 0
            section_words = 0
        else:
            section_words += len(get_words(line))
            section_specifics += len(re.findall(r"\b\d+(?:\.\d+)?%?\b", line))
    
    # Score: low specificity = high score
    score = 0
    if ratio < 0.5:
        score += 40
    elif ratio < 1.0:
        score += 20
    elif ratio < 2.0:
        score += 10
    
    return SpecificityAnalysis(
        specific_markers=specifics,
        abstract_markers=abstract,
        specificity_ratio=round(ratio, 3),
        sections_needing_anchors=sections_needing,
        score=min(100, score),
    )


@dataclass
class DeepForensicsReport:
    """Complete deep forensics report."""
    file_path: str
    word_count: int
    sentence_count: int
    ngrams: NgramAnalysis
    sentence_starters: SentenceStarterAnalysis
    transitions: TransitionAnalysis
    paragraph_structure: ParagraphStructureAnalysis
    hedging: HedgingAnalysis
    blockquotes: BlockquoteAnalysis
    specificity: SpecificityAnalysis
    composite_score: int
    classification: str
    primary_concerns: List[str]


def classify_score(score: int) -> str:
    """Classify based on composite score."""
    if score <= 25:
        return "Likely Human"
    if score <= 45:
        return "Low Risk (Human with polish)"
    if score <= 60:
        return "Ambiguous/Hybrid"
    if score <= 80:
        return "Probably AI-Assisted"
    return "Likely AI-Generated"


def generate_report(file_path: str, text: str, lines: List[str]) -> DeepForensicsReport:
    """Generate comprehensive forensics report."""
    words = get_words(text)
    sentences = get_sentences(text)
    
    ngrams = analyze_ngrams(text)
    starters = analyze_sentence_starters(text)
    transitions = analyze_transitions(text)
    paragraphs = analyze_paragraph_structure(text)
    hedging = analyze_hedging(text)
    blockquotes = analyze_blockquotes(text)
    specificity = analyze_specificity(text, lines)
    
    # Weighted composite score
    composite = int(
        ngrams.repetition_score * 0.10 +
        (100 - starters.variety_score) * 0.10 +
        transitions.score * 0.15 +
        paragraphs.broetry_score * 0.15 +
        hedging.score * 0.10 +
        blockquotes.aphorism_score * 0.15 +
        specificity.score * 0.25
    )
    
    # Primary concerns
    concerns = []
    if ngrams.repetition_score > 30:
        concerns.append(f"High phrase repetition (score: {ngrams.repetition_score})")
    if starters.variety_score < 50:
        concerns.append(f"Low sentence starter variety (score: {starters.variety_score})")
    if transitions.score > 30:
        concerns.append(f"Transition word overuse (density: {transitions.transition_density}%)")
    if paragraphs.broetry_score > 25:
        concerns.append(f"LinkedIn 'broetry' pattern ({paragraphs.one_sentence_ratio:.0%} one-sentence paragraphs)")
    if hedging.score > 25:
        concerns.append(f"Hedging language overuse (density: {hedging.hedge_density}%)")
    if blockquotes.aphorism_score > 20:
        concerns.append(f"Aphorism-heavy blockquotes ({blockquotes.blockquote_count} blockquotes)")
    if specificity.score > 30:
        concerns.append(f"Low specificity ratio ({specificity.specificity_ratio})")
    
    return DeepForensicsReport(
        file_path=file_path,
        word_count=len(words),
        sentence_count=len(sentences),
        ngrams=ngrams,
        sentence_starters=starters,
        transitions=transitions,
        paragraph_structure=paragraphs,
        hedging=hedging,
        blockquotes=blockquotes,
        specificity=specificity,
        composite_score=composite,
        classification=classify_score(composite),
        primary_concerns=concerns,
    )


def print_report(report: DeepForensicsReport, verbose: bool = False) -> None:
    """Print human-readable report."""
    print("=" * 70)
    print("AI WRITING FORENSICS — DEEP ANALYSIS")
    print("=" * 70)
    print(f"\nFile: {report.file_path}")
    print(f"Word count: {report.word_count}")
    print(f"Sentence count: {report.sentence_count}")
    
    print(f"\n{'─' * 70}")
    print("COMPOSITE SCORE")
    print(f"{'─' * 70}")
    print(f"Score: {report.composite_score}/100 — {report.classification}")
    
    if report.primary_concerns:
        print("\nPrimary concerns:")
        for c in report.primary_concerns:
            print(f"  • {c}")
    else:
        print("\nNo major concerns detected.")
    
    print(f"\n{'─' * 70}")
    print("COMPONENT SCORES")
    print(f"{'─' * 70}")
    print(f"  N-gram repetition:       {report.ngrams.repetition_score:3}/100")
    print(f"  Sentence starter variety: {report.sentence_starters.variety_score:3}/100 (higher=better)")
    print(f"  Transition overuse:      {report.transitions.score:3}/100")
    print(f"  Broetry/short paras:     {report.paragraph_structure.broetry_score:3}/100")
    print(f"  Hedging language:        {report.hedging.score:3}/100")
    print(f"  Aphorism blockquotes:    {report.blockquotes.aphorism_score:3}/100")
    print(f"  Abstraction (low spec):  {report.specificity.score:3}/100")
    
    if verbose:
        print(f"\n{'─' * 70}")
        print("DETAILED FINDINGS")
        print(f"{'─' * 70}")
        
        print("\n## N-gram Analysis")
        if report.ngrams.trigram_repeats:
            print("  Repeated trigrams (3+ occurrences):")
            for phrase, count in report.ngrams.trigram_repeats[:5]:
                print(f"    '{phrase}' × {count}")
        if report.ngrams.quadgram_repeats:
            print("  Repeated quadgrams (2+ occurrences):")
            for phrase, count in report.ngrams.quadgram_repeats[:5]:
                print(f"    '{phrase}' × {count}")
        
        print("\n## Sentence Starters")
        print(f"  Top starters: {report.sentence_starters.top_starters[:5]}")
        print(f"  Pronoun-heavy: {report.sentence_starters.pronoun_heavy}")
        
        print("\n## Transitions")
        if report.transitions.flagged_transitions:
            print("  Flagged (overused):")
            for t, c in report.transitions.flagged_transitions:
                print(f"    '{t}' × {c}")
        print(f"  Density: {report.transitions.transition_density}%")
        
        print("\n## Paragraph Structure")
        print(f"  Total paragraphs: {report.paragraph_structure.total_paragraphs}")
        print(f"  One-sentence: {report.paragraph_structure.one_sentence_paragraphs} ({report.paragraph_structure.one_sentence_ratio:.0%})")
        print(f"  Avg sentences/para: {report.paragraph_structure.avg_sentences_per_para}")
        
        print("\n## Hedging")
        print(f"  Total hedges: {report.hedging.hedge_count}")
        print(f"  Density: {report.hedging.hedge_density}%")
        if report.hedging.hedge_phrases[:5]:
            print(f"  Top phrases: {report.hedging.hedge_phrases[:5]}")
        
        print("\n## Blockquotes")
        print(f"  Count: {report.blockquotes.blockquote_count}")
        if report.blockquotes.blockquote_texts:
            print("  Sample blockquotes:")
            for bq in report.blockquotes.blockquote_texts[:3]:
                print(f"    > {bq[:80]}...")
        
        print("\n## Specificity")
        print(f"  Specific markers: {report.specificity.specific_markers}")
        print(f"  Abstract markers: {report.specificity.abstract_markers}")
        print(f"  Ratio: {report.specificity.specificity_ratio}")
        if report.specificity.sections_needing_anchors:
            print(f"  Sections needing anchors: {report.specificity.sections_needing_anchors}")
    
    print()


def main() -> int:
    print("WARNING: This script is deprecated. Use scripts/ai_forensics_unified.py instead.\n",
          file=__import__("sys").stderr)

    parser = argparse.ArgumentParser(
        description="Deep AI writing forensics analysis (DEPRECATED — use ai_forensics_unified.py)"
    )
    parser.add_argument(
        "--file", "-f",
        required=True,
        help="Path to markdown/text file to analyze"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON instead of human-readable"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Include detailed findings in output"
    )
    args = parser.parse_args()
    
    path = Path(args.file)
    if not path.exists():
        print(f"Error: File not found: {path}", file=__import__("sys").stderr)
        return 1
    
    raw = path.read_text(encoding="utf-8")
    body = strip_frontmatter(raw)
    lines = body.replace("\r\n", "\n").split("\n")
    
    report = generate_report(str(path), body, lines)
    
    if args.json:
        # Convert dataclasses to dict for JSON
        def to_dict(obj):
            if hasattr(obj, "__dict__"):
                return {k: to_dict(v) for k, v in asdict(obj).items()}
            if isinstance(obj, list):
                return [to_dict(i) for i in obj]
            if isinstance(obj, tuple):
                return list(obj)
            return obj
        print(json.dumps(to_dict(report), indent=2))
    else:
        print_report(report, verbose=args.verbose)
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
