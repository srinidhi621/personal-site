---
title: "Unified AI Writing Forensics Plan"
draft: true
---

# Unified AI Writing Forensics Plan

## Objective
Build one canonical AI-writing forensics skill that combines:
- lexical/template detection from `docs/agent-skills/ai-writing-detection.md`
- mechanical framing and cadence analysis from `docs/agent-skills/ai-detection-2.md`

The new system should produce consistent, defensible scores and avoid major disagreements (for example, `7/100` vs `70/100`) on the same draft.

## Problem Summary
Current mismatch exists because the two systems optimize for different signals and thresholds:
- Skill A (manual rubric) strongly penalizes formatting/template artifacts (including em-dash overuse).
- Skill B (scripted) is conservative and uses sparse pattern sets with high trigger thresholds.
- Anchor/specificity logic can over-credit abstract text that includes acronyms or list nouns.
- Composite weighting under-penalizes LinkedIn-style cadence and rhetorical scaffolding.

## Scope
In scope:
- One canonical skill doc (single source of truth)
- One primary scoring/reporting script (or orchestrator over existing scripts)
- Shared lexicon/pattern registry
- Calibration corpus and regression checks

Out of scope:
- External detectors/APIs
- Authorship proof claims
- Topic fact-checking

## Target Artifacts
1. `docs/agent-skills/ai-writing-forensics-unified.md`
2. `scripts/ai_forensics_unified.py` (new canonical CLI)
3. `scripts/ai_forensics_rules.yaml` (or `.json`) for weighted patterns
4. `scripts/tests/forensics_corpus/` (labeled calibration set)
5. `scripts/tests/test_ai_forensics_unified.py` (score-range regression tests)
6. Optional: adapters so old scripts call into unified logic with deprecation warnings

## Design Principles
1. Cluster-based inference
- No single feature can force "Likely AI"; require multiple independent signals.

2. Deterministic scoring
- Same input, same score and same flagged lines.

3. Evidence-first output
- Every high-risk claim must include exact quote + line number + rewrite direction.

4. Corporate-writing calibration
- Avoid false positives on professional prose while still flagging templated AI polish.

5. Editor utility
- Output must be directly actionable for revision.

## Unified Scoring Model (0-100)
Weighted families:
- Lexicon + template phrase clusters: 20
- Cadence + mechanical framing: 30
- Abstraction vs specificity quality: 20
- Formatting artifacts: 15
- Ownership/tradeoff texture: 10
- Hard artifacts: 5

Classification:
- 0-29: Likely Human
- 30-59: Ambiguous/Hybrid
- 60-79: Probably AI-Assisted
- 80-100: Likely AI-Generated

### Cluster Boost Rules
Additive boosts after base score:
- `em_dash_count > 4` and `one_sentence_para_ratio > 0.45`: +10
- negative parallelism (`not X, but Y`) `>= 2` and weak ownership: +8
- abstract claims high + weak anchor quality: +8

Cap final score at 100.

## Signal Definitions (Canonical)
### A. Lexicon/phrase clusters
- Merge and dedupe both skill vocabularies.
- Track density and clustering by section (intro/body/conclusion), not just document-level totals.

### B. Mechanical framing/cadence
- One-sentence paragraph ratio
- Rule-of-three frequency and quality check
- Negative parallelism repetition
- Framework scaffolding patterns (principle -> bullets -> maxim)
- Sentence length variance and sentence starter recurrence

### C. Specificity quality (not raw anchor count)
Strong anchors:
- concrete numbers tied to outcomes
- dates/time windows tied to events
- named entities (org/system/project/incident)
- constraints/tradeoffs linked to decisions

Weak anchors:
- standalone acronyms
- generic infrastructure nouns (for example: GPU, data center) without context
- broad claims without mechanism

### D. Formatting artifacts
- Em-dash count with thresholding and contribution
- smart/curly quote consistency
- title-case heading overuse (context-sensitive)
- decorative formatting patterns when present

### E. Ownership/thought texture
- first-person decision ownership ("I/we chose", "we changed because")
- decision scars (failed attempt -> reason -> adjustment)
- explicit tradeoffs and surprises

### F. Hard artifacts
- placeholders in final prose
- suspicious citation scaffolding
- register flips and mask slips

## Implementation Plan
### Phase 1: Spec Unification
1. Draft `ai-writing-forensics-unified.md` with:
- unified rubric
- signal taxonomy
- scoring math
- required report format
- constraints and caveats
2. Freeze old docs with "superseded by unified skill" note.

### Phase 2: Rule Registry
1. Create `ai_forensics_rules.yaml` with:
- phrase groups
- regex patterns
- per-signal weights
- trigger thresholds
- cluster boost definitions
2. Move hardcoded lists out of scripts into registry.

### Phase 3: Unified Engine
1. Implement `ai_forensics_unified.py`:
- parse text
- extract deterministic features
- compute family subscores
- apply cluster boosts
- emit actionable report
2. Include `--json` mode for regression testing.

### Phase 4: Compatibility and Migration
1. Keep old scripts runnable.
2. Add clear deprecation message pointing to unified CLI.
3. Optionally map old outputs to unified score labels.

### Phase 5: Calibration
1. Build corpus (`10-20` samples minimum):
- human-authored (technical + narrative)
- AI-assisted edited
- AI-heavy polished
2. Store expected score bands per file.
3. Tune weights/thresholds until corpus classification is stable.

### Phase 6: Regression Tests
1. Add tests that assert:
- score stays within expected band
- key flags appear for known examples
- no severe drift across refactors
2. Add CI command for deterministic validation.

## Report Contract (Required Output)
1. Executive Summary
- overall score + class
- primary dialect
- 3-7 reasons

2. Component Breakdown
- family subscores and notable non-issues

3. Top Red Flags
- quote
- line number
- signal family
- why risky
- rewrite direction

4. Deep Findings
- clustering patterns
- cadence/template leaks
- where anchors are missing

5. Rewrite Guidance
- section-wise keep/fix
- short before/after rewrites
- `[placeholder: ...]` prompts for missing specifics

## Acceptance Criteria
1. Same file scored by unified tool should not differ by more than 15 points across repeated runs and option presets.
2. No output should classify as "Likely Human" when:
- em-dash over-threshold + high one-sentence paragraph ratio + repeated negative parallelism all co-occur.
3. Every high-risk score (`>= 60`) must include at least 5 evidence-backed flags with line numbers.
4. Corpus accuracy target:
- >= 80% within expected bands
- 0 critical misclassifications on known AI-heavy samples

## Risk Register
1. Overfitting to current lexicon
- Mitigation: separate rule registry and periodic refresh.

2. Corporate prose false positives
- Mitigation: higher confidence threshold unless multi-family clusters appear.

3. Score instability due to small texts
- Mitigation: short-text normalization and confidence warnings for low word count.

4. Manual rubric drift
- Mitigation: keep one canonical doc and regression suite tied to it.

## Rollout Sequence
1. Publish unified skill doc
2. Implement script + rules registry
3. Calibrate on corpus
4. Add tests
5. Mark old skills as legacy
6. Update AGENTS/README references to unified skill

## Immediate Next Tasks
1. Author `docs/agent-skills/ai-writing-forensics-unified.md` draft.
2. Create `scripts/ai_forensics_rules.yaml` with initial merged pattern sets.
3. Implement `scripts/ai_forensics_unified.py` baseline scoring and report.
4. Build first 10-sample calibration corpus and expected score bands.
5. Add regression test harness and run initial tuning pass.
