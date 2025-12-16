# Agent: personal-site-polish

## Mission

Upgrade the personal website hosted at **https://srinidhi.dev** (Hugo + PaperMod + GitHub Pages) into a polished, production-quality personal site.

The CI/CD and deployment setup are already working and must not be modified unless absolutely necessary. Work only inside this repository.
Do not modify DNS, domain settings, or the core GitHub Pages deployment workflow unless there is a clear, deployment-blocking issue.
If you need to install any new libraries, bring them up with a clear need, and impact and only after my approval should you go ahead. 


Your objectives:

- Improve structure and navigation
- Improve homepage content and layout
- Add Hugo archetypes for `writing`, `fiction`, and `link` posts
- Add favicon + app icons + social preview card
- Improve metadata, SEO, and social share settings
- Add basic authoring workflow documentation (how to create posts)

Make small, focused commits with clear messages. Explain your reasoning in the Codex log as you go.

---

## Current Context

- Framework: Hugo 0.152.x
- Theme: PaperMod (installed as a git submodule)
- Deployment: GitHub Pages via GitHub Actions (already working)
- Primary domain: https://srinidhi.dev (live and healthy)
- Content sections exist for: `writing`, `fiction`, `links`, `about`
- Domain redirect / DNS for `srinidhiramanujam.com` is handled elsewhere and is out of scope

Do not change DNS, GoDaddy settings, or the core GitHub Actions deploy job unless absolutely required.

---

## High-Level Plan

You will work in these phases:

1. Inspect current repo state
2. Fix/standardize site structure & navigation
3. Improve homepage content and layout
4. Add Hugo archetypes for common post types
5. Add favicons and basic visual identity
6. Improve SEO, metadata, and social card behavior
7. Verify everything locally and in production
8. Summarize changes and usage instructions

Proceed step by step.

---

## Phase 1: Inspect Current State

Actions:

1. Inspect key files and directories:

   - `hugo.toml`
   - `content/_index.md`
   - `content/about/`
   - `content/writing/`
   - `content/fiction/`
   - `content/links/`
   - `layouts/` (if present)
   - `static/` (existing icons, images, etc.)

2. Run a local build:

   ```bash
   hugo --minify

	3.	Inspect generated files, e.g.:
	•	public/index.html
	•	public/writing/first-post/index.html (or similar)
	•	public/about/index.html

Do not modify anything during this phase. Your goal is simply to understand how the site is currently structured and rendered.

⸻

Phase 2: Site Structure & Navigation

Goal: Clear and intentional structure matching how the site will be used.

Required sections and URLs:
	•	Home: /
	•	Writing: /writing/
	•	Fiction: /fiction/
	•	Links: /links/
	•	About: /about/

Tasks:
	1.	Ensure each section has a proper list page:
	•	content/writing/_index.md
	•	content/fiction/_index.md
	•	content/links/_index.md
	•	content/about/_index.md
For each _index.md, include:
	•	Minimal front matter with title
	•	A short intro paragraph describing what the section is for
(If you add placeholder text, mark with TODO: Srinidhi so the owner can refine later.)
	2.	Fix the main menu in hugo.toml so it reflects these sections in the following order:
	•	Writing
	•	Fiction
	•	Links
	•	About
Example (adapt as needed to align with existing config and PaperMod expectations):

[menu]

  [[menu.main]]
    name = "Writing"
    url  = "/writing/"
    weight = 10

  [[menu.main]]
    name = "Fiction"
    url  = "/fiction/"
    weight = 20

  [[menu.main]]
    name = "Links"
    url  = "/links/"
    weight = 30

  [[menu.main]]
    name = "About"
    url  = "/about/"
    weight = 40


	3.	Ensure the URLs for content under each section are clean, e.g.:

	•	/writing/some-post/
	•	/fiction/some-story/
	•	/links/some-link/

⸻

Phase 3: Homepage Content & Layout

Goal: The root URL / should be a concise personal introduction and navigation hub.

Tasks:
	1.	Rewrite content/_index.md to:
	•	Introduce Srinidhi Ramanujam in 2–3 sentences.
	•	State what he does (data/AI engineering leader) and what he writes about (data engineering, AI, technology, and fiction).
	•	Provide clear links to:
	•	/writing/
	•	/fiction/
	•	/links/
	•	/about/
	•	Optionally mention that the home page lists recent posts.
Example (for structure, not exact wording):

---
title: "Srinidhi Ramanujam"
---

Hi, I'm **Srinidhi Ramanujam**.

I work at the intersection of data engineering, machine learning, and applied AI. This site is where I write about technology, AI, software engineering practice, and occasionally share fiction experiments.

- [Writing](/writing/) — essays on data, AI, and engineering
- [Fiction](/fiction/) — short stories and experiments
- [Links](/links/) — links and commentary on things I find interesting
- [About](/about/) — more about who I am and what I do


	2.	Do not add custom layouts unless necessary. Prefer to stay within PaperMod’s standard list/home behavior.
	3.	Rebuild locally with hugo --minify and confirm that public/index.html is a proper HTML home page.

⸻

Phase 4: Post Archetypes (Writing, Fiction, Links)

Goal: Make it easy to create consistent new posts with hugo new.

Create the following archetype files:
	•	archetypes/writing.md
	•	archetypes/fiction.md
	•	archetypes/link.md

Suggested contents:

archetypes/writing.md

---
title: ""
date: {{ .Date }}
draft: true
tags: []
summary: ""
description: ""
---

archetypes/fiction.md

---
title: ""
date: {{ .Date }}
draft: true
tags: ["fiction"]
summary: ""
description: ""
---

archetypes/link.md

---
title: ""
date: {{ .Date }}
draft: true
tags: ["link"]
summary: ""
description: ""
link_target: ""
---

Then, update or create a README.md in the repo root with a short “Authoring” section. Document:
	•	How to create a new writing post:

hugo new writing/my-new-post.md


	•	How to create a new fiction piece:

hugo new fiction/my-new-story.md


	•	How to create a new link post:

hugo new links/my-new-link.md



Explain briefly where each type will appear (under which section and URL pattern).

⸻

Phase 5: Favicons & App Icons

Goal: Minimal but professional identity via icons.

Create basic icons in static/:
	•	static/favicon.ico
	•	static/favicon-32x32.png
	•	static/favicon-16x16.png
	•	static/apple-touch-icon.png
	•	static/safari-pinned-tab.svg

Characteristics:
	•	Simple, clean design is acceptable (e.g., “SR” initials on a solid background, or a simple shape).
	•	The exact design can be minimal; the goal is not deep branding but avoiding missing icons.

If tools are available, you may generate them (e.g., via ImageMagick or simple SVG). If not, create minimal valid files and ensure they are correctly referenced.

Verify that PaperMod picks them up by default; if it does not:
	•	Adjust hugo.toml to point to these assets using the minimal set of theme parameters required.
	•	Do not overcomplicate configuration.

Rebuild with hugo --minify and check public/index.html for appropriate <link rel="icon"...> and related tags.

⸻

Phase 6: SEO, Metadata & Social Cards

Goal: Reasonable defaults so that sharing the site on social platforms looks good.

Tasks:
	1.	In hugo.toml, under [params] (and related sections as required by PaperMod), ensure:
	•	A good description, e.g.:

description = "Writing on data engineering, AI, technology, and fiction."


	•	Author and site metadata:

[params]
  author = "Srinidhi Ramanujam"
  # existing params like defaultTheme, ShowReadingTime, etc. should remain


	•	Ensure OpenGraph and Twitter metadata are enabled if the theme requires explicit toggles (check PaperMod docs in themes/PaperMod/).

	2.	Add a social preview image:
	•	Create static/social-card.png (1200x630 is a common size).
	•	Simple content is fine: name + tagline on a plain background.
	3.	Configure hugo.toml so that the home page includes:
	•	<meta property="og:image" content="https://srinidhi.dev/social-card.png">
	•	<meta name="twitter:image" content="https://srinidhi.dev/social-card.png">
	4.	After running hugo --minify, validate by checking public/index.html:
	•	grep -i "og:title" public/index.html
	•	grep -i "og:description" public/index.html
	•	grep -i "og:image" public/index.html
	•	grep -i "twitter:image" public/index.html
	•	Check <link rel="canonical" ...> is correct (points to https://srinidhi.dev/).

⸻

Phase 7: Verification & Cleanliness

Tasks:
	1.	Ensure public/ remains in .gitignore and is not tracked by git.
	2.	Run local verification:

hugo --minify
git status -sb

Confirm only intended files are modified.

	3.	Commit changes in logical groups, for example:
	•	Structure sections and navigation
	•	Improve homepage content
	•	Add archetypes and authoring guide
	•	Add favicon and social preview assets
	•	Improve metadata and SEO config
	4.	Push to main and verify deployment:
	•	Check GitHub Actions → Pages workflow is green.
	•	From a terminal, run:

curl -I https://srinidhi.dev/
curl -I https://srinidhi.dev/writing/first-post/
curl -I https://srinidhi.dev/about/


Expect:
	•	HTTP/2 200
	•	Content-Type: text/html; charset=utf-8

⸻

Phase 8: Final Summary

At the end of your work, print a concise summary containing:
	1.	A high-level list of changes:
	•	Structure and navigation changes
	•	Homepage content changes
	•	Archetypes added
	•	Assets (favicons, icons, social card) added
	•	SEO and metadata improvements
	2.	Instructions for the site owner:
	•	How to create new writing / fiction / link posts using hugo new
	•	Where to edit homepage and section intros
	•	Where favicon and social card files live and how to replace them
	•	How to run local preview (hugo server) and production build (hugo --minify)
	3.	Verification notes:
	•	Which URLs were checked with curl -I
	•	Any caveats or TODOs (clearly marked as TODO: Srinidhi)

Do not modify DNS, domain settings, or the core GitHub Pages deployment workflow unless there is a clear, deployment-blocking issue.
If you need to install any new libraries, bring them up with a clear need, and impact and only after my approval should you go ahead. 

