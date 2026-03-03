# Agent skills: authoring, review, and quality

Guides for agents helping Srinidhi **write, revise, and publish** on this Hugo site, and detect AI-like patterns in drafts.

## Skill inventory

### Writing & publishing workflow

| File | Use when... |
|------|-------------|
| `authoring-workflow.md` | Running Hugo commands to create/preview content |
| `content-authoring.md` | Turning an idea into an outline and draft |
| `content-review.md` | Reviewing a draft for clarity, structure, tone (8-pass editorial review) |
| `executive-communication.md` | Drafting or revising work communication (memos, strategy docs, keynotes, alignment notes) |
| `publishing-checklist.md` | Final checks before merging to `main` |
| `style-guide.md` | Markdown/Hugo formatting questions |

### AI-smell detection & forensics

| File | Use when... | Speed |
|------|-------------|-------|
| **`ai-smell-lint.md`** | **Quick pre-publish lint pass on any text. Smell score 1–10, top triggers, surgical fixes.** | **Fast (2–3 min)** |
| **`ai-writing-forensics.md`** | **Deep word-level and sentence-level forensic analysis. 8-family taxonomy, 1–10 scoring, evidence quotes, line-level rewrite guidance.** | **Thorough (10–20 min)** |

**Recommended workflow**: run the lint pass first. If smell score ≥ 6, run the deep forensics for full analysis.

### How skills connect

```
content-authoring.md          executive-communication.md
        │                              │
        ▼                              ▼
  content-review.md  ◄─── uses ───►  ai-smell-lint.md (fast pass)
        │                              │
        │                              ▼ (if score ≥ 6)
        │                     ai-writing-forensics.md (deep pass)
        │
        ▼
  publishing-checklist.md
```

### Legacy (superseded)

| File | Status |
|------|--------|
| `ai-writing-detection.md` | Superseded by `ai-writing-forensics.md` |
| `ai-detection-2.md` | Superseded by `ai-writing-forensics.md` |

### Source material (untracked, not active skills)

The following files in this folder were used as source material to build the active skills above. They are kept for reference but are not active skills:

| File | Incorporated into |
|------|-------------------|
| `skill_authentic_writing_studio.md` | `content-review.md` (revision workflow, line-level heuristics), `ai-smell-lint.md` (anti-patterns), `ai-writing-forensics.md` (line-level editing) |
| `skill_executive_communication_systems_coach.md` | `executive-communication.md` |
| `skill_rhetorical_lint_checker_ai_smell_test.md` | `ai-smell-lint.md` |
