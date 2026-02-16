#!/usr/bin/env python3
"""
AI Writing Forensics — Line Finder Utility.

DEPRECATED: This script has been superseded by scripts/ai_forensics_unified.py.
The unified script includes line-level flagging. This script is kept for backward
compatibility and will be removed in a future cleanup.

Finds exact line numbers for specified phrases or patterns in a markdown file.
Useful for creating actionable forensic reports with edit locations.

Supports the rubric in `docs/agent-skills/ai-detection-2.md`.

Usage:
  python3 scripts/ai_forensics_linefinder.py --file <path> --phrases "phrase1" "phrase2" ...
  python3 scripts/ai_forensics_linefinder.py --file <path> --pattern "regex pattern"
  python3 scripts/ai_forensics_linefinder.py --file <path> --preset ai_lexicon
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, List, Tuple


def strip_frontmatter(raw: str) -> Tuple[str, int]:
    """
    Remove YAML or TOML frontmatter from markdown.
    Returns (body, offset) where offset is the line number where body starts.
    """
    lines = raw.split("\n")
    if not lines:
        return raw, 0
    
    if lines[0].strip() == "---":
        for i, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                body = "\n".join(lines[i+1:])
                return body, i + 1
    
    if lines[0].strip() == "+++":
        for i, line in enumerate(lines[1:], start=1):
            if line.strip() == "+++":
                body = "\n".join(lines[i+1:])
                return body, i + 1
    
    return raw, 0


def find_phrase_lines(
    raw_text: str,
    phrases: List[str],
    case_sensitive: bool = False
) -> Dict[str, List[Tuple[int, str]]]:
    """
    Find line numbers where each phrase appears.
    Returns dict mapping phrase -> list of (line_number, line_text).
    """
    lines = raw_text.split("\n")
    results: Dict[str, List[Tuple[int, str]]] = {p: [] for p in phrases}
    
    for lineno, line in enumerate(lines, start=1):
        check_line = line if case_sensitive else line.lower()
        for phrase in phrases:
            check_phrase = phrase if case_sensitive else phrase.lower()
            if check_phrase in check_line:
                results[phrase].append((lineno, line.strip()))
    
    return results


def find_pattern_lines(
    raw_text: str,
    pattern: str,
    flags: int = re.IGNORECASE
) -> List[Tuple[int, str, str]]:
    """
    Find line numbers where regex pattern matches.
    Returns list of (line_number, line_text, matched_text).
    """
    lines = raw_text.split("\n")
    results: List[Tuple[int, str, str]] = []
    
    rx = re.compile(pattern, flags)
    
    for lineno, line in enumerate(lines, start=1):
        match = rx.search(line)
        if match:
            results.append((lineno, line.strip(), match.group()))
    
    return results


# Preset phrase lists for common forensic searches
PRESETS: Dict[str, List[str]] = {
    "ai_lexicon": [
        "delve", "unlock", "harness", "robust", "seamless",
        "at its core", "key takeaway", "important to note",
        "it's worth noting", "leverage", "synergy", "holistic",
        "paradigm", "ecosystem", "scalable", "cutting-edge",
        "game-changer", "revolutionary", "transformative",
    ],
    "linkedin_dialect": [
        "stop doing", "here's what nobody tells you",
        "let that sink in", "read that again",
        "unpopular opinion", "hot take", "truth bomb",
        "this is huge", "game changer", "let me explain",
        "I'll say it louder", "hear me out",
    ],
    "template_phrases": [
        "simple and non-negotiable", "non-negotiable",
        "the pattern that held up", "we converged on",
        "think of it as", "the goal is not",
        "most of this will still apply",
        "this is a short list", "here's what we learned",
        "lessons learned", "key insights",
    ],
    "hedging": [
        "may", "might", "could", "perhaps", "possibly",
        "potentially", "generally", "typically", "usually",
        "tends to", "seems to", "appears to", "in some cases",
    ],
    "transitions": [
        "however", "moreover", "furthermore", "additionally",
        "consequently", "therefore", "thus", "hence",
        "accordingly", "meanwhile", "nevertheless",
        "nonetheless", "conversely", "similarly",
    ],
    "universal_claims": [
        "always", "never", "everyone", "no one",
        "every", "all", "none", "impossible",
    ],
    "portable_maxims": [
        "is not a strategy", "is the real",
        "can't leak what it never", "never had access to",
        "think in concentric circles", "layered defences",
        "earn the right", "show its work",
    ],
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Find line numbers for phrases/patterns in markdown files"
    )
    parser.add_argument(
        "--file", "-f",
        required=True,
        help="Path to markdown/text file to search"
    )
    parser.add_argument(
        "--phrases", "-p",
        nargs="+",
        help="Phrases to search for (case-insensitive)"
    )
    parser.add_argument(
        "--pattern", "-r",
        help="Regex pattern to search for"
    )
    parser.add_argument(
        "--preset",
        choices=list(PRESETS.keys()),
        help="Use a preset phrase list"
    )
    parser.add_argument(
        "--case-sensitive", "-c",
        action="store_true",
        help="Make phrase search case-sensitive"
    )
    parser.add_argument(
        "--context", "-C",
        type=int,
        default=0,
        help="Lines of context to show before/after match"
    )
    parser.add_argument(
        "--list-presets",
        action="store_true",
        help="List available presets and exit"
    )
    args = parser.parse_args()
    
    if args.list_presets:
        print("Available presets:")
        for name, phrases in PRESETS.items():
            print(f"\n  {name}:")
            for p in phrases[:5]:
                print(f"    - {p}")
            if len(phrases) > 5:
                print(f"    ... and {len(phrases) - 5} more")
        return 0
    
    path = Path(args.file)
    if not path.exists():
        print(f"Error: File not found: {path}", file=__import__("sys").stderr)
        return 1
    
    raw = path.read_text(encoding="utf-8")
    all_lines = raw.split("\n")
    
    if args.pattern:
        results = find_pattern_lines(raw, args.pattern)
        print(f"Pattern: /{args.pattern}/")
        print(f"Matches: {len(results)}")
        print()
        for lineno, line, matched in results:
            print(f"  Line {lineno}: {line[:80]}")
            if matched != line.strip():
                print(f"    Matched: '{matched}'")
            if args.context > 0:
                for i in range(max(0, lineno - args.context - 1), lineno - 1):
                    print(f"    {i+1}| {all_lines[i][:70]}")
                print(f"  > {lineno}| {all_lines[lineno-1][:70]}")
                for i in range(lineno, min(len(all_lines), lineno + args.context)):
                    print(f"    {i+1}| {all_lines[i][:70]}")
                print()
    else:
        phrases = args.phrases or []
        if args.preset:
            phrases = PRESETS[args.preset]
        
        if not phrases:
            print("Error: Provide --phrases, --pattern, or --preset")
            return 1
        
        results = find_phrase_lines(raw, phrases, args.case_sensitive)
        
        found_any = False
        for phrase, matches in results.items():
            if matches:
                found_any = True
                print(f'"{phrase}" ({len(matches)} matches):')
                for lineno, line in matches:
                    print(f"  Line {lineno}: {line[:80]}")
                print()
        
        if not found_any:
            print("No matches found.")
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
