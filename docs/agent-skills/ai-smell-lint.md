# AI Smell Lint — Fast Pass

> **Skill metadata**
> - **Use when**: quick pre-publish check on any draft (post, memo, email, keynote, LinkedIn)
> - **Speed**: 2–3 minutes; this is a lint pass, not a rewrite engine
> - **Inputs**: draft text + optional audience/tone/format context
> - **Output**: 1–10 smell score, top triggers with quotes, ranked surgical fixes
> - **Pair with**: `ai-writing-forensics.md` for deep analysis when score ≥ 6
> - **Complements**: `content-review.md` (structural/editorial), `executive-communication.md` (work formats)

---

## What "AI smell" means

AI smell is not about grammar quality. It is a combination of:

1. **Pattern predictability** — same rhetorical move repeated
2. **Generic abstraction** — high-level words, low sensory detail
3. **Premature polish** — sounds finished before it sounds true
4. **Low-friction argumentation** — no tension, no trade-offs, no uncertainty
5. **Internet-optimized cadence** — performative punchlines and sermon endings

A draft can be well-written and still trigger this if pattern density is too high.

---

## Smell score (1–10)

| Score | Meaning |
|------:|---------|
| 1–2 | Natural — low pattern visibility, reads human |
| 3–4 | Polished but mostly human-feeling |
| 5–6 | Visible AI-assisted texture; pattern repetition noticeable |
| 7–8 | Strong pattern repetition, generic rhetoric dominates |
| 9–10 | Highly synthetic / template-heavy |

---

## Detection rules

### A. Pattern repetition

Flag if any appears repeatedly within a short span:

- "It's not X, it's Y" / "This isn't about X, it's about Y" (2+ in <500 words = visible)
- "The real question is…"
- "In today's world…"
- "This is not just about…"
- "Let that sink in"
- "Here's the thing…"
- "This changes everything."
- Repeated triads ("X, Y, Z") every paragraph
- Repeated sentence openings (unintentional anaphora)
- 3+ one-sentence paragraphs in a short piece
- Repeated rhetorical questions
- Overuse of colon-led dramatic reveals

**Rule**: one use may be fine. Clustered repetition is the problem.

### B. Composite structural templates

#### "Reframe Sandwich" — the most recognizable AI thought-leadership template

```
[[Topic]] is not [[analogy]].

[[Dramatic one-liner]].
[[Dramatic one-liner]].
[[Dramatic one-liner]].

[[Summary sentence.]] [[Topic]] is [[different analogy]].

[[Implications delivered with certainty]].
```

Why it smells — five signals that individually might pass but in combination are unmistakable:

1. **Opening negative reframe** ("is not [[analogy]]") — template entry point, not earned insight
2. **Stacked one-sentence dramatic paragraphs** — each pretends to be a mic-drop without evidence, mechanism, or scene
3. **Double reframe** (opening "is not X" → closing "is Y") — bookended template structure; predetermined framing, not reasoning
4. **Certainty without evidence** — implications delivered without trade-offs, hedging, or "it depends"
5. **Portability** — swap the topic and analogies and the piece still "works," which means it was never really about the topic

**Flag when**: negative reframe + 3+ stacked one-sentence paragraphs + affirmation reframe appear within a short span. Flag the whole block as a unit.

#### Other composite templates

- **The LinkedIn Sermon**: hook → stacked dramatic lines → moral conclusion
- **The Framework Drop**: principle → bullets → portable maxim, repeated across sections
- **The Contrarian Flip**: "Everyone thinks X. Actually, Y." — without evidence for either claim
- **The Elegant Escalation**: three parallel statements that build from mild to dramatic, where the drama is unearned

### C. Abstraction density

Flag high concentration of unsupported abstract nouns:

> value, trust, transformation, innovation, leadership, strategy, excellence, future, impact, change, journey, progress

Each requires a concrete anchor nearby — a metric, artifact, workflow, role, incident, or observable outcome. No anchor = smell.

### D. Cadence / performance

Flag when prose feels "performed" rather than argued:

- Too many punchy endings
- Too many contrastive pivots
- Every paragraph trying to be quotable
- Elevated tone with little evidence
- Sermon-close ("we must do better") without direction
- Overuse of cinematic contrasts with no specifics
- Faux contrarianism without evidence ("everyone thinks X but actually Y")
- Conclusion that restates the hook

### E. Argument weakness

Often mistaken for style problems. Flag if:

- No clear claim
- No audience-specific relevance
- No trade-off or counterargument
- No action / implication
- Thesis repeated but not developed
- Implications delivered with certainty (no hedging, no "it depends")
- Generic certainty or moral posturing masquerading as argument

### F. Chatbot residue / platform dialect

Quick tells that leak from AI assistant training or platform conventions:
- Collaborative openers: "Certainly!", "Of course!", "Great question!", "Absolutely!"
- Helper phrasing: "Let me explain…", "I'd be happy to…", "Hope this helps!"
- Wikipedia-ism: "It is widely regarded," detached encyclopedic tone
- SEO-bot: "In today's fast-paced world…", "In conclusion, as we move forward…"
- Elegant variation: cycling synonyms for no reason ("the tech mogul… the visionary entrepreneur… the Silicon Valley titan")

### G. Authenticity signals (positive — reduce the score)

- Domain-specific detail
- Local context (this team, this system, this incident)
- Honest uncertainty
- Concrete failure modes
- Named stakeholders or artifacts
- Trade-offs acknowledged
- Asymmetry in sentence rhythm (not over-tuned)
- Decision scars ("we tried X, it failed, so we did Y")

---

## Pattern frequency thresholds

### For ~300–800 words

- "not X, but Y" reframes: max 1
- Rhetorical questions: max 1–2
- Triads: max 1–2
- One-sentence dramatic paragraphs: max 2
- Repeated sentence stems: only if intentionally escalatory
- Refrains/anaphora: only if clearly deliberate and climactic

### For executive memos

- Lower tolerance for overt cadence
- Higher tolerance for direct contrast
- Very low tolerance for vague abstraction

### For reflective essays

- Higher tolerance for cadence
- Still require concrete anchors

---

## Output format

### 1) Smell score (1–10)

One number with one-line justification.

### 2) Top triggers (max 5)

Exact quoted phrases/structures with why they trigger.

### 3) Pattern frequency map

Count of repeated moves: reframes, triads, anaphora, one-line paragraphs, rhetorical questions, composite templates.

### 4) Revision actions (ranked, max 7)

Highest-leverage fixes first. Surgical, not broad rewrites.

### 5) Optional rewrites (if requested)

- **Line fixes** (micro — single phrase or sentence)
- **Paragraph fix** (meso — restructure one paragraph)
- **Tone-safe rewrite** (preserve voice, reduce smell)

---

## Smell-reduction playbook

### If "It's not X, it's Y" is overused

Replace with:
- Show the distinction through a concrete example
- Use a contrast sentence without the formula
- Name the failure mode directly
- Split into claim + evidence
- State a trade-off instead of a reframe

Before: "This is not a tooling problem, it's a culture problem."
After: "Teams already have tools. What they don't have is a shared standard for when AI output is acceptable in production."

### If the draft hits the Reframe Sandwich

- Cut the opening reframe; start with the concrete observation instead
- Replace stacked one-liners with one paragraph that develops the point with evidence
- Drop the closing reframe; let the argument earn its own conclusion
- Replace certain implications with specific trade-offs or "it depends" conditions

### If the draft feels too polished

- Add one real detail (timestamp, role, artifact, symptom)
- Remove one "quotable" line
- Keep one imperfect but honest sentence
- Reduce line-by-line climaxing

### If the draft is abstract

Insert:
- One workflow step
- One stakeholder role
- One concrete consequence
- One example of failure/success

### If the draft sounds generic

Ask: "Could this paragraph apply to any company, any team, any topic?"
If yes, it needs local detail.

---

## Quick self-check (ultra-fast, 60 seconds)

1. Circle all abstract nouns without concrete anchors
2. Underline repeated rhetorical formulas
3. Mark the strongest concrete line
4. Cut one performative line
5. Add one skeptic objection
6. Make the close actionable

If the piece reads clean after this, it likely passes.

---

## Agent behavior

When asked to "run the lint check," "fast pass," or "smell test":

1. Score the draft (1–10)
2. Quote exact trigger phrases/patterns
3. Identify whether the issue is style, argument, or both
4. Give ranked fixes
5. Rewrite only the minimum needed
6. Preserve strong lines that are earned
7. Explain the mechanism briefly so the writer learns

**Do not** flatten all rhetoric. **Do not** replace the writer's style with sterile prose. Earned rhetorical force is good writing — the goal is to distinguish earned force from template force.
