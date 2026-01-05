# Style & formatting skill (Markdown + Hugo)

Use this to keep posts consistent and easy to read on PaperMod.

## Writing style

- Prefer **short paragraphs** (1–4 lines).
- Prefer **specific nouns + verbs** over abstract phrasing.
- Use headings to help scanning; avoid overly clever headings that hide meaning.

## Markdown conventions

- Use fenced code blocks for code.
- Prefer lists for checklists, tradeoffs, and step-by-step instructions.
- Use blockquotes sparingly (good for epigraphs or short callouts).

## Hugo conventions in this repo

- Posts live under `content/<section>/...` and render to `/<section>/<slug>/`.
- The homepage uses `{{< spotlight >}}` in `content/_index.md`.
- Per-post images/diagrams should generally live under `static/<section>/<slug>/...`.

## Front matter conventions

Archetypes already give a good starting point. Keep these in mind:

- Use `summary` for list views and quick previews.
- Use `description` for richer social/SEO snippets when the post warrants it.
- Use `tags` to align with existing taxonomy pages.

## “What not to do”

- Don’t edit theme files under `themes/PaperMod` unless there’s no alternative.
- Don’t commit `public/` (build output).


