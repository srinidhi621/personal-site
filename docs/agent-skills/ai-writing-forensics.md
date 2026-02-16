# AI Writing Forensics — Unified Skill

> **Canonical reference** for detecting AI-writing patterns and guiding humanization edits.
> Supersedes `ai-writing-detection.md` (Skill A) and `ai-detection-2.md` (Skill B).

## Purpose

Evaluate whether a draft shows patterns consistent with AI generation or heavy AI assistance, using **text-only forensic analysis**. Produce actionable, evidence-backed editing guidance.

This is **not proof of authorship**. It is a **risk signal** based on clustered artifacts.

---

## Non-negotiable constraints

1. **No external detectors** — no web APIs, no vendor "AI detectors", no ML model calls. Only local text analysis and the repo helper scripts.
2. **No moralizing** — output is purely analytical and edit-oriented.
3. **No single-tell verdicts** — only classify as "Probably AI-Assisted" or higher when multiple independent signal families cluster. See "Cluster-based inference" below.
4. **Always provide evidence quotes** — every high-risk flag must include an exact quote, location, signal family, and rewrite direction.
5. **Calibrate for corporate writing** — professional tone can mimic AI. Raise the bar before labeling anything above "Ambiguous."
6. **Never invent details** — use `[placeholder: ...]` for specifics only the author can supply.
7. **Deterministic** — same input must produce the same score, flags, and classification.

---

## Inputs

- `text` (required): up to ~5 000 words of prose.
- `context` (optional but recommended):
  - `channel`: blog / LinkedIn / memo / marketing / email / other
  - `author_profile`: technical / exec / non-native / unknown
  - `intent`: persuade / inform / narrate / announce / explain / sell
  - `topic`: short label

If context is missing, assume **blog / technical / inform**.

---

## Signal taxonomy (8 families)

### Family A — Lexicon / phrase clusters (max 10 pts)

AI text clusters "safe" vocabulary. Flag when frequent or clustered, especially in intros and conclusions.

**Classic AI safe-words** (verbs): delve, underscore, foster, navigate, harness, leverage, optimize, encapsulate, reimagine, unlock, unleash, unpack, dissect, showcase

**Classic AI safe-words** (nouns): tapestry, landscape (metaphorical), realm, synergy, paradigm, testament, catalyst, beacon, cornerstone, journey

**Classic AI safe-words** (adjectives): pivotal, crucial, intricate, seamless, robust, transformative, dynamic, unparalleled, vibrant, multifaceted, nuanced, comprehensive, cutting-edge, ever-evolving

**Transitional fillers**: "In conclusion," "In summary," "Ultimately," "It is important to note," "Moreover," "Furthermore," "In today's [fast-paced/digital] world," "Not only… but also…," "Additionally" (sentence-start)

**Modern AI-era terms** (GPT-4/Claude-era patterns):
- Invented portmanteaus and compound nouns (e.g. "compute-flation", "intelligence infrastructure")
- Dramatic framing terms: "regime change", "paradigm shift", "inflection point" used without earned context
- Corporate neologisms that don't appear in standard dictionaries

Track density **per section** (intro / body / conclusion), not just document-level totals. Intro and conclusion clusters are higher signal than body clusters.

### Family B — Cadence / mechanical framing (max 20 pts)

AI text has low "burstiness" — uniform sentence lengths, flat rhythmic patterns, predictable paragraph structure.

**Sentence-level signals:**
- Sentence length coefficient of variation (CV): CV < 0.30 is suspicious, CV > 0.55 is healthy
- Sentence starter variety: measure unique first words / total sentences. Score < 0.40 is low variety
- Clause depth variance: approximate by counting commas + subordinating conjunctions per sentence; low variance across sentences is a signal

**Paragraph-level signals:**
- One-sentence paragraph ratio: > 0.45 is strong "LinkedIn broetry" signal
- Average sentences per paragraph: < 1.5 across the whole piece is suspicious

**Punctuation fingerprint:**
- Em-dash density: > 4 em-dashes per 1000 words is suspicious; > 8 is a strong signal
- Semicolon frequency: AI tends to under-use semicolons relative to human technical writers
- Question frequency: AI uses questions strategically (often in hooks); look for mechanical placement
- Parenthetical ratio: compare parentheses usage to em-dash usage; AI prefers em-dashes

### Family C — Structural symmetry / template scaffolding (max 15 pts)

AI loves neat frameworks, balanced contrasts, and repeatable rhetorical structures.

**Patterns to detect:**
- Rule-of-three addiction: compulsive triads ("X, Y, and Z") where the third item is vague or redundant. Count occurrences; 5+ is suspicious.
- Negative parallelism: "not just X, but Y"; "more than X"; "this isn't about A, it's about B". Count occurrences; 2+ in a single piece is suspicious.
- Symmetric contrasts: "from X to Y" constructions. Count occurrences; 3+ is suspicious.
- Anaphora: repeated sentence starters in sequence (e.g. "What has died is... What has died is... What has died is..."). Deliberate literary anaphora is fine; flag when combined with other template signals.
- Framework scaffolding: principle → bullets → maxim pattern. If repeated across multiple sections, strong signal.
- Heading structure regularity: perfectly regular heading patterns (all same depth, all similar length, all same format) suggest template generation.

### Family D — Specificity quality (max 20 pts)

The strongest signal family. AI text makes claims without earning them. Human text shows scars.

**Strong anchors** (count these):
- Concrete numbers tied to outcomes ("reduced latency by 40ms")
- Dates/time windows tied to events ("in Q3 2024, after the outage")
- Named entities: specific orgs, systems, projects, incidents
- Constraints/tradeoffs linked to decisions ("we chose X because Y was too expensive")

**Weak anchors** (discount these):
- Standalone acronyms without context (just "GPU", "API" as set dressing)
- Generic infrastructure nouns without mechanism ("data centers", "cloud platforms")
- Broad claims without a "because" or "when" ("AI is transforming everything")

**Information density variance:**
Measure per-paragraph anchor density (strong anchors / words). Compute standard deviation across paragraphs. Low variance (uniform distribution) is an AI signal. Humans cluster specifics unevenly — dense in the parts they care about, sparse in transitions.

**Discourse pattern:**
- Human pattern: claim → evidence → reflection (or claim → failure → adjustment)
- AI pattern: claim → claim → claim → sweeping conclusion

### Family E — Vocabulary richness (max 10 pts)

AI reuses vocabulary more uniformly than humans. Humans produce more unique words and more words used exactly once.

**Metrics:**
- Type-token ratio (TTR): unique words / total words, measured in 100-word sliding windows to control for text length. Average windowed TTR < 0.60 is low.
- Hapax legomena ratio: words appearing exactly once / total unique words. Ratio < 0.50 is low richness.
- Referential density: pronoun-to-noun-phrase ratio. AI tends to re-state full noun phrases instead of using pronouns. Very low pronoun usage relative to content nouns is a signal.

### Family F — Ownership / thought texture (max 10 pts)

Human writing usually shows the marks of real experience. AI writing is smooth where real life is rough.

**Ownership markers** (look for presence — each reduces the score):
- First-person decision ownership: "I chose", "we decided", "I observed"
- Decision scars: "we tried X, it failed because Y, so we changed to Z"
- Explicit tradeoffs: "we gave up A to get B"
- Surprises: "what I didn't expect was..."
- Constraints: "we couldn't do X because of Y"

**Hedging asymmetry:**
Measure hedging word density per section. Compute variance across sections. Humans hedge asymmetrically — more hedging on novel claims, less on established facts. AI hedges uniformly. Low variance in per-section hedging density is a signal.

### Family G — Formatting artifacts (max 10 pts)

Surface-level tells from AI tools and prompting patterns.

- Em-dash overuse: > 3-4 per article is a known signal for automated AI detection systems. Suggest replacements: definition → colon, aside → parentheses, light pause → comma, related clauses → semicolon.
- Smart/curly quotes ("...") vs straight quotes ("...") — inconsistent mixing is a tell.
- Title-case heading overuse where sentence case is the site convention.
- Emoji-decorated bullets with perfectly matched emoji per item.
- Markdown artifact tells: leftover image credits or stock-photo attribution lines, suspiciously neat numbered lists, placeholder-style text that was never filled in.
- Decorative formatting: excessive boldface for emphasis, especially bolded inline headers in lists.

### Family H — Hard artifacts (max 5 pts)

Rare but very strong tells. Any single hard artifact is significant.

- Placeholders in final prose: `[placeholder: ...]`, `[TODO: ...]`, `[TBD]`
- Suspicious citation scaffolding: vague or fabricated-looking references
- Register flips: sudden shift from casual to academic tone (or vice versa) without reason
- Leftover image/stock-photo credit lines embedded in prose (e.g. "Free Stock Photo of..." as seen when drafting in AI tools that suggest images)
- Knowledge-cutoff tells: "as of my last update", "I don't have access to real-time data"
- Self-referential AI slips: "as an AI language model", "I'd be happy to help"

---

## Scoring model

### Base score: weighted family subscores

Each family produces a subscore from 0 to its max weight. The base score is the sum.

| Family | Max weight |
|--------|-----------|
| A. Lexicon / phrase clusters | 10 |
| B. Cadence / mechanical framing | 20 |
| C. Structural symmetry / scaffolding | 15 |
| D. Specificity quality | 20 |
| E. Vocabulary richness | 10 |
| F. Ownership / thought texture | 10 |
| G. Formatting artifacts | 10 |
| H. Hard artifacts | 5 |
| **Total** | **100** |

### Cluster boost rules (additive, applied after base score)

No single family can force a high classification. Cluster boosts reward the co-occurrence of independent signals:

- `em_dash_count > 4` AND `one_sentence_para_ratio > 0.45`: **+8**
- `negative_parallelism >= 2` AND `weak_ownership` (no decision scars/tradeoffs): **+6**
- `abstraction_high` AND `weak_anchor_quality` AND `low_TTR`: **+8**
- `symmetric_contrasts >= 3` AND `no_decision_scars`: **+6**

Cap final score at 100.

### Classification bands

| Score | Classification |
|------:|----------------|
| 0–29 | Likely Human |
| 30–54 | Ambiguous / Hybrid |
| 55–74 | Probably AI-Assisted |
| 75–100 | Likely AI-Generated |

The 30–54 band is intentionally wide: the hybrid zone is the hardest to classify and should be treated with nuance, not false precision.

### Short-text normalization

For texts under 300 words: halve all family weights except Hard Artifacts, cap score at 60, and emit a confidence warning. Short texts lack the statistical basis for reliable classification.

### Cluster-based inference rule

**Never classify above "Ambiguous / Hybrid" unless at least 3 of the 8 families score above 50% of their individual max weight.** This prevents a single noisy family from driving a misleading overall score.

---

## Report format (required output)

### 1) Executive summary
- Overall score (0–100) + classification
- Primary dialect: None / Corporate-Generic / LinkedIn-Template / Marketing-Polish / Mixed
- 3–7 "why" bullets (evidence-based reasons for the score)
- Context used: channel, intent, author_profile, topic

### 2) Component breakdown
- Family subscores (all 8)
- Cluster boosts applied (if any)
- What is **not** a problem (to prevent over-editing)

### 3) Top red flags (evidence quotes)
- 5–15 items, prioritized by strength
- Each item must include:
  - **Exact quote** from the text
  - **Location** (line number or section name)
  - **Signal family** (A–H)
  - **Why it's risky** (1–2 sentences)
  - **Rewrite direction** (1–2 sentences)

### 4) Deep forensic findings
- Lexicon clustering patterns (where in the piece, not just totals)
- Template scaffolding (what repeats and where)
- Sections needing more anchors
- Cadence/rhythm analysis highlights
- Vocabulary richness assessment
- Platform dialect leakage (if any)

### 5) Actionable rewrite guidance (section-wise)
For each major section:
- **Keep**: what works well
- **Fix**: specific lines to change + why
- 2–6 **Before → After** rewrites (short, targeted)
- 1–3 **anchor prompts**: what details to add, in `[placeholder: ...]` form

---

## Helper script

The canonical CLI is `scripts/ai_forensics_unified.py`. It implements this rubric deterministically.

```bash
# Quick scan
python3 scripts/ai_forensics_unified.py --file content/writing/<post>.md

# With context
python3 scripts/ai_forensics_unified.py \
  --file content/writing/<post>.md \
  --channel blog --intent inform --topic "AI engineering"

# JSON output for regression testing
python3 scripts/ai_forensics_unified.py --file <path> --json

# Verbose deep findings
python3 scripts/ai_forensics_unified.py --file <path> --verbose
```

The script reads pattern definitions and weights from `scripts/ai_forensics_rules.json`. Edit the JSON to update phrase lists, thresholds, and weights without touching the script.

---

## Interaction guidelines (for agents using this skill)

1. **Read this skill doc first.** You can perform a good forensic review using only the rubric above, without running any script.
2. **Run the script for deterministic counts** when precision matters (especially for calibration or when scores are borderline).
3. **Every line of the report must be useful to the author**: either flag a specific sentence with evidence, or give a concrete fix.
4. **Avoid long tables and machine-readable blobs.** The author should be able to scan the report and immediately start editing.
5. **When scoring borderline (30–54)**, lean toward describing *what to watch* rather than asserting a verdict. Acknowledge uncertainty.
6. **When the author has revised a draft**, re-run the analysis on the new version and note what improved.

---

## Quick-reference checklist

When scanning a draft quickly, check for:

- [ ] AI lexicon clusters (especially intro/conclusion)
- [ ] Rule-of-three overuse
- [ ] Negative parallelism ("not just X, but Y") repetition
- [ ] Flat rhythm / uniform sentence length
- [ ] Generic framing without specifics
- [ ] Passive voice dodging ownership
- [ ] Platform dialect markers (LinkedIn broetry, SEO-bot intros)
- [ ] Missing first-person ownership ("I observed", "I decided")
- [ ] "In conclusion" / "In summary" closers
- [ ] Formatting artifacts (smart quotes, emoji bullets)
- [ ] Em-dash count > 3–4 (replace with colons/parentheses/commas/semicolons)
- [ ] Low vocabulary richness (repetitive phrasing, re-stated noun phrases)
- [ ] Symmetric contrasts and neat frameworks without scars
- [ ] Hard artifacts (placeholders, stock-photo credits, register flips)
