#!/usr/bin/env python3
"""
Regression tests for the Unified AI Writing Forensics engine.

Validates that:
1. All corpus samples score within their expected bands.
2. Key flags appear for known examples.
3. Scores are deterministic (same input → same output).
4. Cluster inference guard prevents single-family classification inflation.

Usage:
  python3 -m pytest scripts/tests/test_ai_forensics_unified.py -v
  # or directly:
  python3 scripts/tests/test_ai_forensics_unified.py
"""

from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path

# Ensure the scripts directory is importable
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from ai_forensics_unified import analyze, load_rules, strip_frontmatter

RULES_PATH = REPO_ROOT / "scripts" / "ai_forensics_rules.json"
MANIFEST_PATH = REPO_ROOT / "scripts" / "tests" / "forensics_corpus" / "manifest.json"


def _load_manifest():
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        return json.load(f)


def _analyze_file(file_path: str, rules=None):
    """Helper: read file, strip frontmatter, run analysis."""
    if rules is None:
        rules = load_rules(RULES_PATH)
    path = REPO_ROOT / file_path
    raw = path.read_text(encoding="utf-8")
    body = strip_frontmatter(raw)
    return analyze(file_path=str(path), text=body, rules=rules)


class TestCorpusScoreBands(unittest.TestCase):
    """All corpus samples must score within their expected bands."""

    @classmethod
    def setUpClass(cls):
        cls.rules = load_rules(RULES_PATH)
        cls.manifest = _load_manifest()

    def test_all_samples_in_band(self):
        """Each sample's final score falls within [expected_lo, expected_hi]."""
        failures = []
        for sample in self.manifest["samples"]:
            report = _analyze_file(sample["file"], self.rules)
            lo, hi = sample["expected_band"]
            if not (lo <= report.final_score <= hi):
                failures.append(
                    f"{sample['file']}: score={report.final_score}, "
                    f"expected=[{lo},{hi}] ({report.classification})"
                )
        self.assertEqual(failures, [], "Samples outside expected bands:\n" + "\n".join(failures))


class TestKeyFlags(unittest.TestCase):
    """Known examples should produce specific flags."""

    @classmethod
    def setUpClass(cls):
        cls.rules = load_rules(RULES_PATH)

    def test_stock_photo_flagged_in_long_live(self):
        """The stock photo credit in 'long live software engineering' should be flagged."""
        report = _analyze_file(
            "content/writing/scratch/long live software engineering.txt", self.rules
        )
        stock_flags = [f for f in report.flags if "stock photo" in f.why.lower() or "image credit" in f.why.lower()]
        self.assertGreater(
            len(stock_flags), 0,
            "Expected stock photo credit to be flagged in 'long live software engineering.txt'"
        )

    def test_no_ai_self_reference_in_human_posts(self):
        """Human-written posts should not contain AI self-reference flags."""
        for file_path in [
            "content/writing/ai-software-engg.md",
            "content/writing/coding-agents-2025.md",
        ]:
            report = _analyze_file(file_path, self.rules)
            ai_flags = [f for f in report.flags if "self-reference" in f.why.lower()]
            self.assertEqual(
                len(ai_flags), 0,
                f"Unexpected AI self-reference flag in {file_path}"
            )

    def test_ai_text_has_no_ownership_markers(self):
        """The AI-generated scratchpad should have near-zero ownership markers."""
        report = _analyze_file("content/writing/scratch/scratchpad.txt", self.rules)
        ownership_fs = next(
            fs for fs in report.family_scores if fs.key == "ownership_texture"
        )
        # Score should be high (meaning low ownership detected)
        self.assertGreater(
            ownership_fs.score, ownership_fs.max_weight * 0.5,
            f"AI text ownership_texture score too low: {ownership_fs.score}/{ownership_fs.max_weight}"
        )


class TestDeterminism(unittest.TestCase):
    """Same input must produce the same score across multiple runs."""

    @classmethod
    def setUpClass(cls):
        cls.rules = load_rules(RULES_PATH)

    def test_deterministic_scores(self):
        """Running analysis twice on the same file produces identical scores."""
        for sample_file in [
            "content/writing/scratch/scratchpad.txt",
            "content/writing/ai-software-engg.md",
        ]:
            r1 = _analyze_file(sample_file, self.rules)
            r2 = _analyze_file(sample_file, self.rules)
            self.assertEqual(
                r1.final_score, r2.final_score,
                f"Non-deterministic score for {sample_file}: {r1.final_score} vs {r2.final_score}"
            )
            # Also check family subscores
            for fs1, fs2 in zip(r1.family_scores, r2.family_scores):
                self.assertEqual(
                    fs1.score, fs2.score,
                    f"Non-deterministic {fs1.key} for {sample_file}: {fs1.score} vs {fs2.score}"
                )


class TestClusterInferenceGuard(unittest.TestCase):
    """The cluster inference guard should prevent single-family inflation."""

    @classmethod
    def setUpClass(cls):
        cls.rules = load_rules(RULES_PATH)

    def test_human_posts_not_classified_above_ambiguous(self):
        """Human-authored posts should not be classified as 'Probably AI-Assisted' or higher."""
        human_files = [
            "content/writing/ai-software-engg.md",
            "content/writing/coding-agents-2025.md",
            "content/writing/context-engg-prelude.md",
            "content/writing/context-engg-conclusions.md",
        ]
        for file_path in human_files:
            report = _analyze_file(file_path, self.rules)
            ambiguous_max = self.rules["classification"]["ambiguous_hybrid"][1]
            self.assertLessEqual(
                report.final_score, ambiguous_max,
                f"{file_path} scored {report.final_score} (above ambiguous max {ambiguous_max})"
            )


class TestClassificationLabels(unittest.TestCase):
    """Classification labels must match score bands."""

    @classmethod
    def setUpClass(cls):
        cls.rules = load_rules(RULES_PATH)

    def test_ai_text_classified_above_ambiguous(self):
        """The AI-generated scratchpad should be classified as at least 'Probably AI-Assisted'."""
        report = _analyze_file("content/writing/scratch/scratchpad.txt", self.rules)
        ambiguous_max = self.rules["classification"]["ambiguous_hybrid"][1]
        self.assertGreater(
            report.final_score, ambiguous_max,
            f"AI text scored only {report.final_score} — expected above {ambiguous_max}"
        )

    def test_human_text_classified_as_likely_human(self):
        """The human-written ai-software-engg post should be 'Likely Human'."""
        report = _analyze_file("content/writing/ai-software-engg.md", self.rules)
        human_max = self.rules["classification"]["likely_human"][1]
        self.assertLessEqual(
            report.final_score, human_max,
            f"Human text scored {report.final_score} — expected <= {human_max}"
        )

    def test_hybrid_text_in_ambiguous_band(self):
        """The hybrid 'long live' text should be in the ambiguous band."""
        report = _analyze_file(
            "content/writing/scratch/long live software engineering.txt", self.rules
        )
        lo = self.rules["classification"]["ambiguous_hybrid"][0]
        hi = self.rules["classification"]["ambiguous_hybrid"][1]
        self.assertTrue(
            lo <= report.final_score <= hi,
            f"Hybrid text scored {report.final_score} — expected [{lo},{hi}]"
        )


class TestShortTextNormalization(unittest.TestCase):
    """Short texts should be normalized and capped."""

    @classmethod
    def setUpClass(cls):
        cls.rules = load_rules(RULES_PATH)

    def test_very_short_text_capped(self):
        """A very short text should trigger the short-text warning and cap."""
        body = "This is a test sentence."
        report = analyze(
            file_path="<inline>",
            text=body,
            rules=self.rules,
        )
        self.assertTrue(report.short_text_warning, "Short text warning not triggered")
        max_score = self.rules["short_text"]["max_score"]
        self.assertLessEqual(
            report.final_score, max_score,
            f"Short text scored {report.final_score} — should be capped at {max_score}"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
