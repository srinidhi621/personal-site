# Authoring Workflow

A quick checklist for adding new content to [srinidhi.dev](https://srinidhi.dev).

## Local preview

```bash
hugo server -D
```

- Visit http://localhost:1313 while writing.
- Run `hugo --minify` for a production build before committing.

## Create a writing post

```bash
hugo new writing/my-new-post.md
```

The `archetypes/writing.md` template includes:
- `summary` and `description` fields for SEO/social cards
- Draft mode enabled by default—flip `draft` to `false` when ready
- Placeholder intro text you can overwrite

Writing posts live under `/writing/`.

## Create a fiction piece

```bash
hugo new fiction/my-story.md
```

This uses `archetypes/fiction.md`, which is tuned for short narratives:
- Adds the `fiction` tag automatically
- Encourages a strong opening line and short paragraphs

Fiction posts are published at `/fiction/<slug>/`.

## Create a link entry

```bash
hugo new links/some-link.md
```

The `archetypes/links.md` template includes a `link` field plus sections for
"Why it matters" notes. The list view lives at `/links/`.

## Update section intros or the homepage

- `content/_index.md`: homepage hero + summary blocks
- `content/<section>/_index.md`: overview text at the top of each list page

## Brand assets

All icons and the social preview live under `static/`:
- `favicon*.png`, `favicon.ico`: tab icons
- `apple-touch-icon.png`: mobile shortcut icon
- `safari-pinned-tab.svg`: Safari pinned tab asset
- `social-card.png`: shared across OpenGraph/Twitter cards

Replace these files with assets of the same name to refresh the visual identity.
