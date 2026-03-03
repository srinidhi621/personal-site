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

### Archived (do not use)

Older detection skills have been consolidated into the two canonical passes above and moved to `archive/`. All unique signals from these files have been folded into `ai-smell-lint.md` and `ai-writing-forensics.md`.

| File | Status |
|------|--------|
| `archive/ai-writing-detection.md` | Consolidated into `ai-smell-lint.md` + `ai-writing-forensics.md` |
| `archive/ai-detection-2.md` | Consolidated into `ai-writing-forensics.md` (helper scripts, signal families) |
