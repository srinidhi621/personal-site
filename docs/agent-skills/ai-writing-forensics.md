# AI Writing Forensics — Deep Assessment

> **Skill metadata**
> - **Use when**: rigorous, evidence-backed forensic analysis of a draft for AI-writing patterns
> - **Speed**: 10–20 minutes; thorough word-level and sentence-level assessment
> - **Inputs**: draft text (up to ~5,000 words) + optional channel/author/intent/topic context
> - **Output**: 1–10 score with 8-family breakdown, evidence quotes, line-level rewrite guidance
> - **Pair with**: `ai-smell-lint.md` (run the fast pass first; use this for deeper investigation when lint score ≥ 6)
> - **Helper scripts**: `scripts/ai_forensics_unified.py` (canonical), plus `ai_writing_forensics.py`, `ai_forensics_deep.py`, `ai_forensics_linefinder.py`

---

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

- `text` (required): up to ~5,000 words of prose.
- `context` (optional but recommended):
  - `channel`: blog / LinkedIn / memo / marketing / email / other
  - `author_profile`: technical / exec / non-native / unknown
  - `intent`: persuade / inform / narrate / announce / explain / sell
  - `topic`: short label

If context is missing, assume **blog / technical / inform**.

---

## Signal taxonomy (8 families)

### Family A — Lexicon / phrase clusters

AI text clusters "safe" vocabulary. Flag when frequent or clustered, especially in intros and conclusions.

**Classic AI safe-words (verbs)**: delve, underscore, foster, navigate, harness, leverage, optimize, encapsulate, reimagine, unlock, unleash, unpack, dissect, showcase

**Classic AI safe-words (nouns)**: tapestry, landscape (metaphorical), realm, synergy, paradigm, testament, catalyst, beacon, cornerstone, journey

**Classic AI safe-words (adjectives)**: pivotal, crucial, intricate, seamless, robust, transformative, dynamic, unparalleled, vibrant, multifaceted, nuanced, comprehensive, cutting-edge, ever-evolving

**Transitional fillers**: "In conclusion," "In summary," "Ultimately," "It is important to note," "Moreover," "Furthermore," "In today's [fast-paced/digital] world," "Not only… but also…," "Additionally" (sentence-start)

**Modern AI-era terms** (GPT-4/Claude-era patterns):
- Invented portmanteaus and compound nouns (e.g. "compute-flation", "intelligence infrastructure")
- Dramatic framing terms: "regime change", "paradigm shift", "inflection point" used without earned context
- Corporate neologisms that don't appear in standard dictionaries

Track density **per section** (intro / body / conclusion), not just document-level totals. Intro and conclusion clusters are higher signal than body clusters.

### Family B — Cadence / mechanical framing

AI text has low "burstiness" — uniform sentence lengths, flat rhythmic patterns, predictable paragraph structure.

**Sentence-level signals:**
- Sentence length coefficient of variation (CV): CV < 0.30 is suspicious, CV > 0.55 is healthy
- Sentence starter variety: unique first words / total sentences. Score < 0.40 is low variety
- Clause depth variance: approximate by counting commas + subordinating conjunctions per sentence; low variance is a signal

**Paragraph-level signals:**
- One-sentence paragraph ratio: > 0.45 is strong "LinkedIn broetry" signal
- Average sentences per paragraph: < 1.5 across the whole piece is suspicious

**Punctuation fingerprint:**
- Em-dash density: > 4 per 1,000 words is suspicious; > 8 is strong signal
- Semicolon frequency: AI tends to under-use semicolons relative to human technical writers
- Question frequency: AI uses questions strategically (often in hooks); look for mechanical placement
- Parenthetical ratio: compare parentheses usage to em-dash usage; AI prefers em-dashes

### Family C — Structural symmetry / template scaffolding

AI loves neat frameworks, balanced contrasts, and repeatable rhetorical structures.

**Individual patterns to detect:**
- **Rule-of-three addiction**: compulsive triads ("X, Y, and Z") where the third item is vague or redundant. 5+ occurrences is suspicious.
- **Negative parallelism**: "not just X, but Y"; "more than X"; "this isn't about A, it's about B". 2+ in a single piece is suspicious.
- **Symmetric contrasts**: "from X to Y" constructions. 3+ is suspicious.
- **Anaphora**: repeated sentence starters in sequence. Deliberate literary anaphora is fine; flag when combined with other template signals.
- **Framework scaffolding**: principle → bullets → maxim pattern. Repeated across sections = strong signal.
- **Heading regularity**: perfectly regular heading patterns (same depth, similar length, same format) suggest template generation.

**Composite structural templates:**

These are multi-move templates where the individual moves might pass but the combination is unmistakable.

**"Reframe Sandwich"** — the most recognizable AI thought-leadership template:
```
[[Topic]] is not [[analogy]].

[[Dramatic one-liner]].
[[Dramatic one-liner]].
[[Dramatic one-liner]].

[[Summary sentence.]] [[Topic]] is [[different analogy]].

[[Implications delivered with certainty]].
```
Components: opening negative reframe + stacked one-sentence dramatic paragraphs + closing affirmation reframe + unearned certainty. Key tell: the structure is portable — swap the topic and it still "works."

**"LinkedIn Sermon"**: contrarian hook → stacked dramatic lines → moral conclusion without direction.

**"Framework Drop"**: principle → bullets → portable maxim, repeated across multiple sections.

**"Contrarian Flip"**: "Everyone thinks X. Actually, Y." — without evidence for either claim.

**"Elegant Escalation"**: three parallel statements building mild → dramatic, where the drama is unearned by evidence.

### Family D — Specificity quality

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
- Hallucination-avoidance vagueness: "many believe," "research shows," "experts agree" with no specific citation — AI hedges attribution to avoid fabricating sources

**Information density variance:**
Measure per-paragraph anchor density (strong anchors / words). Compute standard deviation across paragraphs. Low variance (uniform distribution) is an AI signal. Humans cluster specifics unevenly — dense in the parts they care about, sparse in transitions.

**Discourse pattern:**
- Human pattern: claim → evidence → reflection (or claim → failure → adjustment)
- AI pattern: claim → claim → claim → sweeping conclusion

### Family E — Vocabulary richness

AI reuses vocabulary more uniformly than humans.

**Metrics:**
- Type-token ratio (TTR): unique words / total words, measured in 100-word sliding windows. Average windowed TTR < 0.60 is low.
- Hapax legomena ratio: words appearing exactly once / total unique words. Ratio < 0.50 is low richness.
- Referential density: AI tends to re-state full noun phrases instead of using pronouns. Very low pronoun usage relative to content nouns is a signal.
- Elegant variation: cycling through unusual synonyms to avoid repetition ("the tech mogul… the visionary entrepreneur… the Silicon Valley titan") — a strong signal when the variation adds no meaning.

### Family F — Ownership / thought texture

Human writing shows the marks of real experience. AI writing is smooth where real life is rough.

**Ownership markers** (each reduces the score):
- First-person decision ownership: "I chose", "we decided", "I observed"
- Decision scars: "we tried X, it failed because Y, so we changed to Z"
- Explicit tradeoffs: "we gave up A to get B"
- Surprises: "what I didn't expect was..."
- Constraints: "we couldn't do X because of Y"

**Hedging asymmetry:**
Humans hedge asymmetrically — more hedging on novel claims, less on established facts. AI hedges uniformly. Low variance in per-section hedging density is a signal.

### Family G — Formatting artifacts

Surface-level tells from AI tools and prompting patterns.

- Em-dash overuse: > 3–4 per article is a known signal. Suggest replacements: definition → colon, aside → parentheses, light pause → comma, related clauses → semicolon.
- Smart/curly quotes vs straight quotes — inconsistent mixing is a tell.
- Title-case heading overuse where sentence case is the site convention.
- Emoji-decorated bullets with perfectly matched emoji per item.
- Markdown artifacts: leftover image credits, suspiciously neat numbered lists, placeholder text.
- Decorative formatting: excessive boldface for emphasis, bolded inline headers in lists.

### Family H — Hard artifacts

Rare but very strong tells. Any single hard artifact is significant.

- Placeholders in final prose: `[placeholder: ...]`, `[TODO: ...]`, `[TBD]`
- Suspicious citation scaffolding: vague or fabricated-looking references
- Register flips: sudden shift from casual to academic tone without reason
- Leftover image/stock-photo credit lines
- Knowledge-cutoff tells: "as of my last update", "I don't have access to real-time data"
- Self-referential AI slips: "as an AI language model", "I'd be happy to help"
- Chatbot training residue: "Certainly!", "Of course!", "Great question!", "Absolutely!", "Let me explain…", "Hope this helps!" — collaborative openers and helper phrasing that leak from assistant fine-tuning
- Platform dialect spillover: Wikipedia-ism ("It is widely regarded," detached encyclopedic tone, title-case-heavy subheads), SEO-bot intros ("In today's fast-paced world…"), LinkedIn broetry (one-sentence paragraphs, emoji bullets, faux-contrarian hooks)

---

## Scoring model

### Family scoring: each family produces a subscore from 0 to 10

| Family | Weight | What it measures |
|--------|-------:|------------------|
| A. Lexicon / phrase clusters | 10% | Overused safe vocabulary |
| B. Cadence / mechanical framing | 20% | Rhythm flatness, paragraph structure |
| C. Structural symmetry / scaffolding | 15% | Template patterns, composite templates |
| D. Specificity quality | 20% | Claims vs evidence, anchor density |
| E. Vocabulary richness | 10% | TTR, hapax ratio, referential density |
| F. Ownership / thought texture | 10% | Decision scars, tradeoffs, hedging |
| G. Formatting artifacts | 10% | Em-dashes, quotes, markdown tells |
| H. Hard artifacts | 5% | Placeholders, register flips, AI slips |

**Overall score** = Σ(family_score × weight), producing a 0–10 number, rounded to nearest 0.5.

### Cluster boost rules (additive, applied after base score)

No single family can force a high classification. Cluster boosts reward co-occurrence of independent signals:

- `em_dash_count > 4` AND `one_sentence_para_ratio > 0.45`: **+0.8**
- `negative_parallelism >= 2` AND weak ownership (no decision scars/tradeoffs): **+0.6**
- `abstraction_high` AND `weak_anchor_quality` AND `low_TTR`: **+0.8**
- `symmetric_contrasts >= 3` AND `no_decision_scars`: **+0.6**
- **Reframe Sandwich detected** (negative reframe + 3+ stacked one-liners + affirmation reframe): **+1.0**

Cap final score at 10.

### Classification bands

| Score | Classification |
|------:|----------------|
| 1–3 | Likely Human |
| 4–5 | Ambiguous / Hybrid |
| 6–7 | Probably AI-Assisted |
| 8–10 | Likely AI-Generated |

The 4–5 band is intentionally wide: the hybrid zone is the hardest to classify and should be treated with nuance, not false precision.

### Short-text normalization

For texts under 300 words: halve all family weights except Hard Artifacts, cap score at 6, and emit a confidence warning. Short texts lack the statistical basis for reliable classification.

### Cluster-based inference rule

**Never classify above "Ambiguous / Hybrid" unless at least 3 of the 8 families score above 5.** This prevents a single noisy family from driving a misleading overall score.

---

## Line-level editing heuristics

When producing rewrite guidance, apply these heuristics at the word and sentence level.

### Prefer

- Specific nouns over abstract categories
- Active verbs over passive constructions
- Honest qualifiers over false certainty
- Precise contrasts over formula reframes ("not X, but Y")
- One strong image over multiple vague gestures

### Reduce

- Stacked adjectives
- Inflated transitions ("Moreover," "Furthermore," "It is worth noting")
- Generic slogans and portable maxims
- Repeated sentence stems
- Over-clever reframes

### Watch for repeated stems

If multiple sentences begin with the same word or structure, determine: is this intentional cadence (anaphora for rhetorical effect) or accidental repetition? Accidental repetition is almost always a signal.

### Watch for pattern frequency

Any single rhetorical pattern repeated 3+ times in a short piece becomes visible and triggers AI-smell regardless of quality.

### Argument integrity check

For each major section, assess:
- What is the core claim?
- What is unstated but assumed?
- Where is it overstated or under-evidenced?
- What tension or counterpoint is missing?
- Are implications earned by the preceding evidence?

---

## Report format (required output)

### 1) Executive summary

- Overall score (1–10) + classification
- Primary dialect: None / Corporate-Generic / LinkedIn-Template / Marketing-Polish / Mixed
- 3–7 "why" bullets (evidence-based reasons for the score)
- Context used: channel, intent, author_profile, topic

### 2) Component breakdown

- Family subscores (all 8, each 0–10)
- Cluster boosts applied (if any)
- What is **not** a problem (to prevent over-editing)

### 3) Top red flags (evidence quotes)

5–15 items, prioritized by strength. Each item must include:
- **Exact quote** from the text
- **Location** (line number or section name)
- **Signal family** (A–H)
- **Why it's risky** (1–2 sentences)
- **Rewrite direction** (1–2 sentences)

### 4) Deep forensic findings

- Lexicon clustering patterns (where in the piece, not just totals)
- Composite template detection (Reframe Sandwich, LinkedIn Sermon, etc.)
- Template scaffolding (what repeats and where)
- Sections needing more anchors
- Cadence/rhythm analysis highlights
- Vocabulary richness assessment
- Argument integrity assessment (per section)
- Platform dialect leakage (if any)

### 5) Actionable rewrite guidance (section-wise)

For each major section:
- **Keep**: what works well
- **Fix**: specific lines to change + why + line-level heuristic applied
- 2–6 **Before → After** rewrites (short, targeted)
- 1–3 **anchor prompts**: what details to add, in `[placeholder: ...]` form

---

## Helper scripts

Four scripts in `scripts/` support this rubric. All print to stdout for terminal use.

> **Note**: scripts produce 0–100 raw scores internally. Divide by 10 and round to nearest 0.5 to get the 1–10 scale used in this skill.

### 1. Unified forensics (canonical): `scripts/ai_forensics_unified.py`

Implements this rubric deterministically. Reads pattern definitions and weights from `scripts/ai_forensics_rules.json`.

```bash
python3 scripts/ai_forensics_unified.py --file content/writing/<post>.md
python3 scripts/ai_forensics_unified.py --file <path> --channel blog --intent inform --topic "AI engineering"
python3 scripts/ai_forensics_unified.py --file <path> --json      # JSON for regression testing
python3 scripts/ai_forensics_unified.py --file <path> --verbose   # Deep findings
```

### 2. Base forensics: `scripts/ai_writing_forensics.py`

Editor-friendly report with executive summary, component scores, top red flags with line numbers and rewrite directions.

```bash
python3 scripts/ai_writing_forensics.py --file <path> --channel blog --intent inform --topic "<topic>"
```

Options: `--file`, `--channel`, `--author-profile`, `--intent`, `--topic`, `--max-flags` (default 15).

### 3. Deep analysis: `scripts/ai_forensics_deep.py`

Extended pattern detection: n-gram frequency, sentence starter patterns, transition word density, one-sentence paragraph ratio, hedging density, specificity ratio.

```bash
python3 scripts/ai_forensics_deep.py --file <path> --verbose
python3 scripts/ai_forensics_deep.py --file <path> --json
```

### 4. Line finder: `scripts/ai_forensics_linefinder.py`

Locate exact line numbers for specific phrases or patterns. Useful after deep analysis to build edit lists.

```bash
python3 scripts/ai_forensics_linefinder.py --file <path> --phrases "non-negotiable" "earn the right"
python3 scripts/ai_forensics_linefinder.py --file <path> --preset ai_lexicon
python3 scripts/ai_forensics_linefinder.py --file <path> --pattern "^>\s+"
python3 scripts/ai_forensics_linefinder.py --list-presets
```

Available presets: `ai_lexicon`, `linkedin_dialect`, `template_phrases`, `hedging`, `transitions`, `universal_claims`, `portable_maxims`.

### Recommended workflow

1. **Quick scan**: run `ai_forensics_unified.py` for score and top flags
2. **Deep dive**: run `ai_forensics_deep.py --verbose` for pattern analysis
3. **Edit prep**: run `ai_forensics_linefinder.py` with specific phrases for exact line numbers
4. **Manual review**: use the rubric above to assess signals the scripts may miss

---

## Interaction guidelines (for agents using this skill)

1. **Read this skill doc first.** You can perform a good forensic review using only the rubric above, without running any script.
2. **Run the script for deterministic counts** when precision matters (especially for calibration or when scores are borderline).
3. **Every line of the report must be useful to the author**: either flag a specific sentence with evidence, or give a concrete fix.
4. **Avoid long tables and machine-readable blobs.** The author should be able to scan the report and immediately start editing.
5. **When scoring borderline (4–5)**, lean toward describing *what to watch* rather than asserting a verdict. Acknowledge uncertainty.
6. **When the author has revised a draft**, re-run the analysis on the new version and note what improved.
7. **Apply line-level editing heuristics** in the rewrite guidance — don't just flag problems, show the word-level and sentence-level fix.

---

## Quick-reference checklist

When scanning a draft quickly, check for:

- [ ] AI lexicon clusters (especially intro/conclusion)
- [ ] Rule-of-three overuse
- [ ] Negative parallelism ("not just X, but Y") repetition
- [ ] Composite templates (Reframe Sandwich, LinkedIn Sermon, Framework Drop)
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
- [ ] Argument integrity gaps (claims without evidence, certainty without trade-offs)
