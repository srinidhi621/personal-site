# Skill: Rhetorical Lint Checker (AI-Smell Test)

## Purpose
Run a fast, high-signal review on any draft (memo, email, post, essay, speech notes) to detect “AI smell” and improve authenticity, specificity, and rhetorical control **without flattening the writing**.

This is a **lint pass**, not a rewrite engine.
It should:
- flag visible pattern repetition
- detect generic abstractions and over-polished phrasing
- preserve the writer’s intent and voice
- suggest targeted fixes, not broad rewrites

---

## What “AI Smell” Means (Operational Definition)

AI smell is usually **not** about grammar quality.
It is about a combination of:
1. **Pattern predictability** (same rhetorical move repeated)
2. **Generic abstraction** (high-level words, low sensory detail)
3. **Premature polish** (sounds finished before it sounds true)
4. **Low friction argumentation** (no tension, no trade-offs, no uncertainty)
5. **Internet-optimized cadence** (performative punch lines and sermon endings)

A draft can be excellent and still trigger this if pattern density is too high.

---

## Use Cases

- Final pass before publishing a LinkedIn post
- Final pass before sending a leadership memo
- Review of keynote/script language for over-the-top cadence
- Revision of “good but too polished” AI-assisted drafts
- Self-editing pass to preserve voice

---

## Inputs This Skill Expects
Provide:
- the draft text
- audience (optional but useful)
- goal (inform / persuade / align / provoke / reflect)
- tone target (plain / executive / reflective / keynote / etc.)

If not provided, infer a reasonable default and proceed.

---

## Output Format (Always Use This)

### 1) Smell Score (0–10)
- **0–2** = natural / low pattern visibility
- **3–4** = polished but mostly human-feeling
- **5–6** = visible AI-assisted texture
- **7–8** = strong pattern repetition / generic rhetoric
- **9–10** = highly synthetic / template-heavy

### 2) Top Triggers Detected (max 5)
List exact triggers with quoted examples.

### 3) Pattern Frequency Map
Count and flag repeated moves (e.g., reframes, triads, anaphora, one-line paragraphs, rhetorical questions).

### 4) Specificity Audit
List vague nouns / verbs and suggest concrete replacements.

### 5) Argument Integrity Check
- What is the core claim?
- What is unstated but assumed?
- Where is it overstated / under-evidenced?
- What tension or counterpoint is missing?

### 6) Revision Actions (ranked)
Give 3–7 surgical edits, highest leverage first.

### 7) Optional Rewrites
Provide up to 3 short rewrites:
- **line fixes** (micro)
- **paragraph fix** (meso)
- **tone-safe rewrite** (preserve voice)

---

## Detection Rules (Lint Heuristics)

### A. Pattern Repetition Heuristics
Flag if any appears repeatedly within short span:
- “It’s not X, it’s Y” (2+ in <500 words = visible)
- “The real question is…”
- “In today’s world…”
- “This is not just about…”
- “Let that sink in”
- repeated triads (“X, Y, Z”) every paragraph
- repeated sentence openings (unintentional anaphora)
- 3+ one-sentence paragraphs in a short piece
- repeated rhetorical questions
- repeated “Here’s the thing”

**Rule:** one use may be fine; clustered repetition is the problem.

### B. Abstraction Density Heuristics
Flag high concentration of nouns like:
- value, trust, transformation, innovation, leadership, strategy, excellence, future, impact, change, journey, progress

If used, require:
- metric
- artifact
- workflow
- role
- incident
- or observable outcome nearby

### C. Cadence / Performance Heuristics
Flag when prose feels “performed” rather than argued:
- too many punchy endings
- too many contrastive pivots
- every paragraph trying to be quotable
- elevated tone with little evidence
- sermon-close (“we must do better”) without direction

### D. Argument Weakness Heuristics (often mistaken for style problems)
Flag if:
- no clear claim
- no audience-specific relevance
- no trade-off
- no counterargument
- no action / implication
- thesis repeated but not developed

### E. Authenticity Signals (positive signals)
Boost confidence if draft includes:
- domain-specific detail
- local context
- honest uncertainty
- concrete failure modes
- named stakeholders
- trade-offs
- asymmetry in sentence rhythm (not over-tuned)

---

## AI-Smell Test Checklist (Fast Manual Pass)

Before finalizing, ask:

### Opening
- [ ] Do I open with a concrete scene, artifact, or observation?
- [ ] If abstract, do I ground it within 2–3 sentences?

### Pattern Control
- [ ] Did I overuse “not X, but Y”?
- [ ] Did I repeat the same rhetorical move too often?
- [ ] Is any cadence intentional, or did repetition happen accidentally?

### Specificity
- [ ] Which nouns here are vague?
- [ ] Can I replace at least 3 abstractions with concrete details?

### Argument
- [ ] What is my actual claim in one sentence?
- [ ] What would a smart skeptic object to?
- [ ] Did I address that directly?

### Close
- [ ] Does the ending direct action / judgment / lens?
- [ ] Or does it only sound good?

---

## Smell-Reduction Playbook (What to Do Instead)

### If you overused “It’s not X, it’s Y”
Replace with one of these:
- **show the distinction through example**
- **use a contrast sentence without formula**
- **name the failure mode directly**
- **split into claim + evidence**
- **state a trade-off instead of a reframe**

Example:
- Instead of: “This is not a tooling problem, it’s a culture problem.”
- Try: “Teams already have tools. What they don’t have is a shared standard for when AI output is acceptable in production.”

### If the draft feels too polished
- add one real detail (timestamp, role, artifact, symptom)
- remove one “quotable” line
- keep one imperfect but honest sentence
- reduce line-by-line climaxing

### If the draft is abstract
Insert:
- one workflow step
- one stakeholder role
- one concrete consequence
- one example of failure/success

### If the draft sounds generic
Ask:
- “Could this paragraph apply to any company, any team, any topic?”
If yes, it needs local detail.

---

## Rewrite Modes This Skill Can Produce

### Mode 1: Minimal lint fix
Preserve structure and tone, only remove visible AI smell.

### Mode 2: Authenticity-first revision
Increase specificity and argument integrity, reduce performance.

### Mode 3: Voice-preserving hard reset
Keep the core claim, rebuild the prose in a more human cadence.

---

## Assistant Behavior for Future Conversations (using this skill)
When I say “run the AI-smell test”:
1. Score the draft (0–10).
2. Quote exact trigger phrases / patterns.
3. Identify whether the issue is style, argument, or both.
4. Give ranked fixes.
5. Rewrite only the minimum needed first.
6. If requested, provide a stronger rewrite after preserving my voice.

Important:
- Do not flatten all rhetoric.
- Do not replace my style with sterile prose.
- Preserve strong lines that are earned.
- Explain the mechanism briefly so I learn.

---

## Pattern Frequency Thresholds (Practical Defaults)
Use these as defaults unless context says otherwise.

For ~300–800 words:
- “not X, but Y”: max 1
- rhetorical questions: max 1–2
- triads: max 1–2
- one-sentence dramatic paragraphs: max 2
- repeated sentence stems: only if intentionally escalatory
- refrains/anaphora: only if clearly deliberate and climactic

For executive memos:
- lower tolerance for overt cadence
- higher tolerance for direct contrast
- very low tolerance for vague abstraction

For reflective essays:
- higher tolerance for cadence
- still require concrete anchors

---

## Prompt Starters (for reuse)
- “Use the Rhetorical Lint Checker skill. Run an AI-smell test on this draft, score it, quote triggers, and give ranked fixes before rewriting.”
- “Lint this for pattern repetition and generic abstractions. Preserve my voice. Minimal edits first.”
- “This sounds too polished. Run the smell test and make it feel more human without making it sloppy.”
- “Find where the rhetoric is doing work vs where it is just decoration.”

---

## One-Page Quick Version (Ultra-fast self-check)
If in a hurry, do this:
1. Circle all abstractions.
2. Underline repeated rhetorical formulas.
3. Mark the strongest concrete line.
4. Cut one performative line.
5. Add one skeptic objection.
6. Make the close actionable.

If the piece still reads clean after this, it likely passes.
