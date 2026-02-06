# AI-Writing Forensics (Text-Only, Editor-Friendly)

## Purpose
Evaluate whether a draft shows patterns consistent with AI generation or heavy AI assistance, using **text-only forensic analysis**.

This is **not proof of authorship**. It’s a **risk signal** based on clustered artifacts.

## What “good” output looks like (interaction rule)
In an interactive editing session, every line of the report must be useful to the author in one of two ways:

1) **Flags a specific sentence** that risks sounding like LinkedIn influencer / template prose (with an exact quote and location), or  
2) **Gives a concrete fix** (rewrite suggestion, or a prompt for missing anchors like numbers/incidents/tradeoffs).

Avoid long tables. Avoid dumping large machine-readable blobs. The author should be able to scan the report and immediately edit the draft.

---

## Local helper scripts

This repo includes helper scripts that support the rubric with deterministic counts and line-numbered flags.

### 1. Base Forensics Script: `scripts/ai_writing_forensics.py`

The primary script for AI writing detection. Produces an editor-friendly report with:
- Executive summary (score, classification, dialect)
- Component scores (lexicon, cadence, template, abstraction, texture, etc.)
- Top red flags with exact line numbers, quotes, and rewrite directions
- Section-wise actionable guidance

**Usage:**
```bash
python3 scripts/ai_writing_forensics.py \
  --file content/writing/<post>.md \
  --channel blog \
  --intent inform \
  --topic "<topic>"
```

**Options:**
- `--file` (required): Path to markdown/text file
- `--channel`: Context (blog / LinkedIn / marketing / memo / email)
- `--author-profile`: Author type (technical / exec / non-native / unknown)
- `--intent`: Purpose (persuade / inform / narrate / announce / explain / sell)
- `--topic`: Short topic label
- `--max-flags`: Maximum red flags to show (default: 15)

---

### 2. Deep Analysis Script: `scripts/ai_forensics_deep.py`

Extended forensics for deeper pattern detection. Analyzes:
- N-gram frequency (repeated phrases, a strong AI signal)
- Sentence starter patterns (AI tends to overuse certain openings)
- Transition word density (overuse of "however", "moreover", etc.)
- One-sentence paragraph ratio ("LinkedIn broetry" detection)
- Hedging language density
- Blockquote/callout aphorism detection
- Specificity ratio (concrete details vs abstract claims)

**Usage:**
```bash
python3 scripts/ai_forensics_deep.py \
  --file content/writing/<post>.md \
  --verbose
```

**Options:**
- `--file` / `-f` (required): Path to markdown/text file
- `--verbose` / `-v`: Include detailed findings
- `--json`: Output as JSON instead of human-readable

**Typical workflow:** Run the base script first for an actionable editing report, then run the deep script for additional signal detection.

---

### 3. Line Finder Utility: `scripts/ai_forensics_linefinder.py`

Utility to find exact line numbers for specific phrases or patterns. Useful for:
- Locating repeated phrases flagged by deep analysis
- Finding all instances of template language
- Creating actionable edit lists with line numbers

**Usage:**
```bash
# Search for specific phrases
python3 scripts/ai_forensics_linefinder.py \
  --file content/writing/<post>.md \
  --phrases "non-negotiable" "earn the right" "the pattern that held up"

# Use a preset phrase list
python3 scripts/ai_forensics_linefinder.py \
  --file content/writing/<post>.md \
  --preset template_phrases

# Search with regex pattern
python3 scripts/ai_forensics_linefinder.py \
  --file content/writing/<post>.md \
  --pattern "^>\s+"  # Find all blockquotes
```

**Available presets:**
- `ai_lexicon`: Classic AI safe-words (delve, unlock, harness, robust, seamless...)
- `linkedin_dialect`: LinkedIn influencer markers (stop doing, let that sink in...)
- `template_phrases`: Thought-leadership boilerplate (non-negotiable, key takeaway...)
- `hedging`: Hedging language (may, might, could, potentially...)
- `transitions`: Transition words (however, moreover, furthermore...)
- `universal_claims`: Overconfident language (always, never, everyone...)
- `portable_maxims`: Slide-ready maxims (is not a strategy, cannot leak what...)

**Options:**
- `--file` / `-f` (required): Path to file
- `--phrases` / `-p`: Custom phrases to search
- `--pattern` / `-r`: Regex pattern to search
- `--preset`: Use a preset phrase list
- `--case-sensitive` / `-c`: Case-sensitive search
- `--context` / `-C`: Lines of context to show around matches
- `--list-presets`: Show available presets and exit

---

### Recommended forensic workflow

1. **Quick scan:** Run `ai_writing_forensics.py` for score and top flags
2. **Deep dive:** Run `ai_forensics_deep.py --verbose` for pattern analysis
3. **Edit prep:** Run `ai_forensics_linefinder.py` with specific phrases to get exact line numbers
4. **Manual review:** Use the rubric below to assess signal families the scripts may miss

The scripts print to stdout for easy terminal use. All are parameterized for reuse across files.

---

## Inputs
- `text` (required): Up to ~5000 words.
- `context` (optional but recommended):
  - `channel`: LinkedIn / blog / internal memo / marketing / email / other
  - `author_profile`: technical / exec / non-native / unknown
  - `intent`: persuade / inform / narrate / announce / explain / sell
  - `topic`: short label

If `context` is missing, assume: **blog / corporate thought-leadership**.

---

## Non-negotiable constraints
1. **No external detectors** (no web, no vendor “AI detectors”, no citations). Local repo scripts are allowed only for counts/scoring support.
2. **No moralizing**. Output is purely analytical and edit-oriented.
3. **No single-tell verdicts**. Only label “Likely AI” when multiple independent signals cluster.
4. **Always provide evidence quotes** for anything you flag as high risk.
5. **Calibrate for corporate writing**: professional tone can mimic AI. Raise the bar before “Likely AI.”
6. **Never invent details**. Use `[placeholder: ...]` for facts only the author can supply.

---

## Core detection model
AI-like writing often shows a cluster of:
- **Low surprise** (predictable phrasing)
- **Template scaffolding** (portable frameworks, slide-ready maxims)
- **Generic abstraction** where the draft should have scars (incidents, numbers, constraints)
- **Over-confident conclusions** (unearned universals)
- **Platform dialect leakage** (LinkedIn “broetry” / contrarian hooks)

---

## Signal families (what to look for)

### Family A — AI lexicon & safe-words (weak alone, stronger when clustered)
Watch for repeated corporate-safe words/phrases (examples):
- “unlock”, “harness”, “robust”, “seamless”, “delve”
- “at its core”, “key takeaway”, “it’s worth noting”, “important to note”

### Family B — LinkedIn influencer dialect (medium-to-strong)
Watch for:
- Faux-contrarian hooks: “Stop doing X…”, “Here’s what nobody tells you…”
- One-sentence paragraphs stacked for effect
- Moral-ending platitudes
- “Not just X, but Y” repeated as cadence

### Family C — Rhetorical templates (strong when repeated)
Examples:
- Slide-ready maxims: “X is not a strategy”, “A system can’t leak what it never saw”
- Neat frameworks without scars: “three rings”, “five layers”, “simple and non-negotiable”
- Rule-of-three addiction (“X, Y, and Z”) where the third item is vague

### Family D — Abstraction vs specificity (strong signal)
High-risk pattern:
- Many claims + few anchors (dates, numbers, named artifacts, real incidents, constraints).

### Family E — Thought texture (medium-to-strong)
Human writing usually shows:
- Decision scars: “we tried X, it failed because Y, so we changed Z”
- Uneven emphasis in a human way
- A specific surprise or tradeoff

### Family F — Contradictions / loose ends (strong when present)
- Claims that don’t match later claims
- Overreach without a mechanism
- Placeholders that never get resolved

### Family G — Hard artifacts (rare but very strong)
- `[placeholder: ...]` in final prose
- Fake citations
- Register flips (“marketing voice” → “academic voice”) without reason
- Self-referential AI slips

---

## Report format (required, editor-friendly)

1) **Executive Summary**
   - Overall score (0–100) + classification
   - Primary dialect (None / Corporate-Generic / LinkedIn-Template / Marketing-Polish / Mixed)
   - 3–7 “why” bullets

2) **Overall Assessment**
   - Component totals (deterministic)
   - What is *not* a problem (to avoid over-editing)

3) **Top Red Flags (Evidence Quotes)**
   - 8–15 items (depending on length)
   - Each item must include:
     - Exact quote
     - Location (prefer file line number if available)
     - Why it’s risky (name the family)
     - Rewrite direction (1–2 lines)

4) **Deep Forensic Findings**
   - Lexicon & phraseology (cluster vs isolated)
   - Template scaffolding (what repeats)
   - Where the draft needs anchors (which sections)
   - LinkedIn dialect leakage (if any)

5) **Actionable Rewrite Guidance (section-wise)**
   - For each major section:
     - “Keep” (what works)
     - “Fix” (specific lines to change + why)
     - 2–6 “Before → After” rewrites (short, targeted)
     - 1–3 anchor prompts (what to add, in `[placeholder: ...]` form)

---

## Confidence scoring rubric (0–100)
| Score | Classification | Signals |
|------:|----------------|---------|
| 0–29 | Likely Human | Anchors + decision scars + unevenness |
| 30–59 | Ambiguous/Hybrid | Polished structure but some template/low-anchor clusters |
| 60–79 | Probably AI-Assisted | Repeated templates + low anchors + dialect leakage |
| 80–100 | Likely AI-Generated | Strong clustering + hard artifacts + interchangeable paragraphs |

