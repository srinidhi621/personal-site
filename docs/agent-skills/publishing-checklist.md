# Publishing checklist skill

Use this right before opening a PR or merging to `main`.

## 1) Content correctness

- `draft = false` for posts that should publish.
- Title, `summary`, and (optionally) `description` are filled and accurate.
- Headings are in a logical hierarchy.
- Links work and point where intended.

## 2) Assets (images, diagrams, downloads)

- Prefer storing per-post assets under: `static/<section>/<slug>/...`
- Reference assets by absolute path (site-root), e.g. `/writing/my-post/diagram.svg`
- Ensure filenames are stable (don’t rename assets that existing posts reference).

## 3) Hugo / front matter hygiene

- Tags are consistent (avoid near-duplicates like `llm` vs `LLM`).
- No accidental future dates unless intended.
- If a post should not appear on home, consider `hiddenInHomeList` (only if already used in repo patterns).

## 4) Local verification

Run:

```bash
hugo server -D
```

and verify:

- The post renders correctly on localhost.
- Images load; code blocks render; footnotes/links work.

Then run:

```bash
hugo --minify
```

## 5) Repo cleanliness

- `public/` is not committed (should remain ignored by `.gitignore`).
- Only intended files are changed.

## 6) Optional quick checks (when editing site-wide behavior)

- If you changed `config/_default/hugo.toml` or templates, confirm the homepage and at least one post page renders.
- If you changed the social card or SEO defaults, sanity-check the generated HTML includes OG/Twitter tags.

