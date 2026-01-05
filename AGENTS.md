## Repo overview (for agents)

This repository contains the source for **[srinidhi.dev](https://srinidhi.dev)** — a personal site built with **Hugo** and the **PaperMod** theme, published via **GitHub Pages**.

- **Production site**: `https://srinidhi.dev/`
- **GitHub repo**: `https://github.com/srinidhi621/personal-site`
- **Stack**: Hugo (extended) + PaperMod (git submodule) + GitHub Actions → GitHub Pages

---

## Guardrails (read first)

- **No DNS / domain registrar changes**: out of scope for this repo.
- **Avoid changes to deployment**: `.github/workflows/deploy.yml` is production-critical. Only change if deployment is broken.
- **No new dependencies** (npm/pip/etc.) without explicit owner approval.
- **Do not commit build output**: `public/` must remain ignored (see `.gitignore`).
- **Prefer small, focused commits** with clear messages.

---

## How the site works

### Hugo configuration

Primary config: `config/_default/hugo.toml`

- **`baseURL`**: `https://srinidhi.dev/`
- **Theme**: `PaperMod`
- **Menu**: Writing / Fiction / Links / About
- **Home feed sections**: `params.mainSections = ["writing", "fiction", "links"]`
- **Icons/social**:
  - `params.assets.*` point to files under `static/`
  - `params.images = ["social-card.png"]` for OpenGraph/Twitter defaults

Staging override: `config/staging/hugo.toml`

- **Drafts on staging**: `buildDrafts = true`
- **Env flag**: `params.env = "staging"`
- **Local baseURL**: `http://localhost:1313/`

### Theme

PaperMod is included as a git submodule:

- `themes/PaperMod` (see `.gitmodules`)
- Prefer configuration and light overrides over editing theme files directly.

### Content model (sections → URLs)

All content is Markdown under `content/`:

- **Home**: `content/_index.md` → `/`
- **Writing**: `content/writing/` → `/writing/<slug>/`
- **Fiction**: `content/fiction/` → `/fiction/<slug>/`
- **Links**: `content/links/` → `/links/<slug>/`
- **About**: `content/about/` → `/about/`

Each section has a list page:

- `content/writing/_index.md`
- `content/fiction/_index.md`
- `content/links/_index.md`
- `content/about/_index.md`

---

## Publishing mode: where to edit what

This section is the “navigation map” agents should use when helping with content.

### Staging vs production (worktree workflow)

- **Production worktree**: this repo root on `main`
- **Staging worktree**: `../personal-site-staging` on `staging`
- **Default authoring target**: use the staging worktree for all new drafts and edits
- **Compare versions**: `git diff main..staging -- content/writing/<post>.md`
- **Publish**: merge `staging` → `main` and set `draft = false` when explicitly asked to publish
- **Commits/push**: commit with a clear message; only push if the user asks

### Example publish flow (commands)

```bash
# in staging worktree
cd ../personal-site-staging
git status -sb
# edit content, set draft = false when publishing
git add content/writing/<post>.md
git commit -m "Update <post> draft"

# in production worktree
cd ../personal-site
./scripts/publish_staging.sh
```

### Quick content map

- **Homepage copy**: `content/_index.md`
  - Includes the homepage intro + the `{{< spotlight >}}` block.
- **Section intros**:
  - Writing: `content/writing/_index.md`
  - Fiction: `content/fiction/_index.md`
  - Links: `content/links/_index.md`
  - About: `content/about/_index.md`
- **Posts**:
  - Writing: `content/writing/*.md`
  - Fiction: `content/fiction/*.md`
  - Links: `content/links/*.md`

### Common “change requests” → file to touch

- **Update site title/menu/SEO defaults/social card**: `config/_default/hugo.toml`
- **Change what appears on home feed**: `config/_default/hugo.toml` → `params.mainSections`
- **Change how the home list renders**: `layouts/index.html` (override of PaperMod list behavior)
- **Change spotlight selection/rendering**: `layouts/shortcodes/spotlight.html`
- **Add or update per-post images/diagrams**:
  - Put assets in `static/<section>/<slug>/...`
  - Reference them by URL (e.g. `/writing/my-post/diagram.svg`)
- **Update icons / social preview**: `static/` (see “Static assets” section above)

### Content front matter expectations

Agents should preserve existing patterns, but in general:

- **Draft control**: `draft = true/false`
- **Good share previews**: fill `summary` and/or `description` (archetypes already include these)
- **Tags**: keep tags consistent (used for taxonomy pages)

---

## Agent skills (authoring & review)

When working with Srinidhi on writing/publishing, use these skill guides in `docs/agent-skills/`:

| File | Purpose |
|------|---------|
| `README.md` | Overview |
| `authoring-workflow.md` | Hugo commands for creating/previewing content |
| `content-authoring.md` | Turning ideas into outlines and drafts |
| `content-review.md` | Reviewing for clarity, structure, tone |
| `ai-writing-detection.md` | Detecting AI-like patterns and humanizing drafts |
| `publishing-checklist.md` | Final checks before publishing |
| `style-guide.md` | Markdown/Hugo formatting conventions |

### Custom layout overrides (minimal)

This repo intentionally keeps customization small, but two overrides matter:

- **Home/list template override**: `layouts/index.html`
  - On home, it lists pages from `params.mainSections` (via PaperMod-style paginator logic).
- **Homepage spotlight shortcode**: `layouts/shortcodes/spotlight.html`
  - Used from `content/_index.md` as `{{< spotlight >}}`
  - Currently shows the latest *non-draft* post from the **writing** section.

### Scripts

Utility scripts live in `scripts/`:

- `generate_context_engg_svgs.py` — generates SVG charts for the context engineering posts
- `publish_staging.sh` — merges `staging` into `main` with a no-ff merge commit

### Static assets (published at site root)

Everything in `static/` is served from `/`:

- **Custom domain**: `static/CNAME`
- **Favicons/app icons**: `static/favicon.ico`, `static/favicon-16x16.png`, `static/favicon-32x32.png`, `static/apple-touch-icon.png`, `static/safari-pinned-tab.svg`
- **Social preview image**: `static/social-card.png`
- **Per-post assets**: put files under `static/<section>/<slug>/...` and reference by URL.

---

## Common workflows

See `docs/agent-skills/authoring-workflow.md` for the full checklist. Quick reference:

```bash
hugo server --environment staging   # Staging preview (includes drafts)
hugo server                         # Production preview (no drafts)
hugo --minify           # Production build
hugo new writing/x.md   # New writing post
hugo new fiction/x.md   # New fiction post
hugo new links/x.md     # New link entry
```

Archetypes: `archetypes/writing.md`, `archetypes/fiction.md`, `archetypes/links.md`

---

## Conventions & gotchas

- **Drafts**: drafts won’t publish on production builds. Flip `draft = false` when ready, and use the staging environment to preview drafts.
- **Spotlight behavior**: `spotlight.html` currently only considers `content/writing/` and excludes drafts.
  - If you want the spotlight to cover Fiction/Links, adjust the shortcode (small, safe change).
- **Styling**: prefer PaperMod params and small additive overrides.
  - If custom CSS is needed, prefer adding it via Hugo’s assets pipeline (e.g. `assets/css/extended/*.css`) rather than editing `themes/PaperMod`.
- **Binaries**: avoid committing large binary files (PDF/DOCX) unless intentionally providing downloads.

---

## Deployment (GitHub Pages)

Workflow: `.github/workflows/deploy.yml`

Trigger:

- Pushes to `main`

What it does (high level):

- Checks out the repo **with submodules**
- Sets up **Hugo extended**
- Runs `hugo --minify` (outputs to `public/`)
- Uploads `public/` as the Pages artifact and deploys it

Treat this workflow as **production-critical**.
