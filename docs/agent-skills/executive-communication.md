# Executive Communication — Work Formats Skill

> **Skill metadata**
> - **Use when**: drafting or revising work communication (executive memos, architecture narratives, strategy docs, keynote openings, stakeholder alignment notes)
> - **Inputs**: communication objective + audience + available evidence
> - **Output**: argument-first draft in the appropriate format, with rhetorical force applied after logic
> - **Pair with**: `ai-smell-lint.md` (run as final pass), `content-review.md` (for longer-form review)
> - **Voice**: direct, grounded, high-agency; sharp without contempt; precise without sterile

---

## Core principles

1. **Mechanism over mimicry** — use rhetorical mechanisms (contrast, scale shift, cadence, cataloguing) without copying anyone's voice
2. **Concrete before conceptual** — start from observable reality: a scene, failure mode, artifact, metric, workflow, user moment
3. **Argument before ornament** — if the logic is weak, do not compensate with elevated language
4. **Earn the moral/strategic turn** — move from description to implication only after evidence or shared experience
5. **Respect cognitive load** — reduce jargon density unless the audience expects it; use expert terms only when they compress meaning
6. **Be useful** — end with decisions, trade-offs, or next steps

---

## Anti-patterns to avoid

### High-risk phrases (use sparingly or not at all)

- "It's not X, it's Y" (only when truly reframing, max 1 per piece)
- "In today's world…"
- "The future of X is…"
- "At the end of the day…"
- Generic triads with no specificity ("speed, scale, innovation")
- Inflated contrast without proof
- Vague uplift endings ("we must do better")

### Structural anti-patterns

- Abstract opening with no scene/example
- Too many rhetorical questions
- Repeated cadence patterns in every paragraph
- Too many short punchy lines in sequence (the "LinkedIn Sermon")
- Over-cataloguing (laundry lists)
- Fake certainty or fake humility
- Moralizing before analysis
- The Reframe Sandwich (see `ai-smell-lint.md` for the full pattern)

### Enterprise writing anti-patterns

- "transformation" without workflow change
- "AI-first" without governance model
- "platform" without ownership boundaries
- "value" without time-to-value or KPI definition
- "trust" without provenance/evals/auditability

---

## Rhetorical patterns (use with discipline, not as templates)

1. **Scale Shift** — system-level stakes ↔ one person/workflow and back
2. **Human Inventory** — name real stakeholder roles affected
3. **Contrast Pairing** — meaningful contrasts (benchmark performance vs operational reliability)
4. **Cataloguing** — list roles/scenes/examples for breadth; each item must add a new angle
5. **Moral / Strategic Turn** — "If this is true, what follows for us?"
6. **Sentence-Length Variation** — long sentences to build, short ones to land
7. **Controlled Refrain** — repeat one phrase only if it deepens the argument each time
8. **Tension-Holding** — keep both truths visible when the problem is genuinely paradoxical
9. **Time Compression** — past assumptions → current consequences → future risk
10. **Actionable Close** — finish with a decision frame, standard, or practice

---

## Writing process

### Step 1: Clarify the objective

Ask or infer:
- What must happen after this communication?
- Who is the audience?
- What are they likely worried about?
- What are the political constraints?
- What evidence is available?

### Step 2: Build the argument spine

Draft in bullets first:
- context → problem → evidence/examples → implication → recommendation → trade-offs → next step

### Step 3: Add rhetorical force

Only after the argument works:
- add one scale shift
- add one human inventory (if useful)
- add one contrast
- optionally add one refrain/cadence moment

### Step 4: Run the AI-smell lint pass

Use the `ai-smell-lint.md` fast-pass checklist. Check for:
- repeated reframes
- repeated triads
- repeated cadence openings
- generic abstractions without anchors
- sermon tone
- vague conclusion

### Step 5: Tighten for audience

Produce versions if needed:
- executive summary
- technical detail version
- verbal talking points
- email / memo format

---

## Output mode templates

### 1) Executive memo

- Decision / ask
- Why now
- What changed
- Evidence
- Options and trade-offs
- Recommendation
- Risks
- Next steps

### 2) Architecture / strategy narrative

- Observed failure mode(s)
- System-level pattern
- Design principle
- Target-state operating model
- Rollout path
- Controls / governance
- Success metrics

### 3) Leadership talk / keynote opening

- Concrete image or incident
- Pattern recognized
- Scale shift
- Strategic implication
- Call to responsibility/action

### 4) Stakeholder alignment note

- What we agree on
- Where tension exists
- What decision is needed
- What is reversible vs irreversible
- Proposed path

---

## Agent behavior

When helping draft or revise work communication using this skill:

1. Extract the **argument spine** first
2. Identify audience and hidden objections
3. Suggest 2 contrarian perspectives or second-order effects
4. Apply rhetorical mechanisms intentionally (not mechanically)
5. Run the AI-smell lint pass (`ai-smell-lint.md`) and flag repeated patterns
6. Produce a polished version plus a brief "why this works / where it may fail" note
