# Agent: hugo-pages-debugger

## Mission

Debug and fix the deployment of my personal Hugo website that is hosted via GitHub Pages and mapped to the custom domain `srinidhi.dev`.

## Current Symptoms

- The repo in the current directory is a Hugo site (`hugo.toml` present, `themes/PaperMod` submodule).
- GitHub Actions workflow `Deploy Hugo site to GitHub Pages` completes successfully.
- GitHub Pages settings show:
  - Source: GitHub Actions
  - Custom domain: `srinidhi.dev` (DNS check successful)
- The live site at `https://srinidhi.dev/` consistently returns an **XML RSS feed**, not the HTML home page.
- Navigating to `https://srinidhi.dev/index.html`, `https://srinidhi.dev/about/`, etc. also results in XML (or 404).
- Locally, running `hugo` produces a `public/` directory that appears to contain valid HTML.

Your job is to figure out why GitHub Pages is serving XML and make the site serve the correct HTML homepage.

## Environment / Assumptions

- You are running inside the repo root on my Mac.
- `git`, `gh`, `hugo`, `curl` and standard Unix tools (`ls`, `grep`, `sed`, `awk`, `jq`, etc.) are available.
- I am OK with you:
  - Modifying files in this repo.
  - Running `hugo` locally.
  - Committing and pushing to the `main` branch of `srinidhi621/personal-site`.
- Do **not** touch DNS or GoDaddy directly; just assume the `srinidhi.dev` DNS and GitHub Pages configuration is already correct (as long as curl confirms it).

## High-level Goals

1. Confirm what exactly Hugo is generating for the homepage and sections.
2. Confirm what GitHub Pages is actually serving on `https://srinidhi.dev/` (status codes, headers, body).
3. Identify the mismatch between the built artifact and what Pages serves.
4. Implement the minimal changes in this repo (and, if needed, Pages config) so that:
   - `https://srinidhi.dev/` returns an HTML homepage.
   - Section URLs like `/writing/first-post/` and `/about/` also return HTML.
5. Keep the deployment path via GitHub Actions + Pages; do not switch to `gh-pages` branch hacks unless absolutely required.

## Tools You Should Use

You can and should use:

- **Local inspection**
  - `ls`, `tree`, `find`, `cat`, `grep`, `rg`
  - `cat hugo.toml`, inspect `content/`, `layouts/`, `themes/PaperMod/`
- **Hugo**
  - `hugo`
  - `hugo --minify`
  - Inspect `public/index.html`, `public/index.xml`, and section outputs.
- **GitHub / Pages**
  - `git status`, `git log`
  - `gh repo view`, `gh api` if useful
  - Inspect `.github/workflows/deploy.yml`
- **HTTP / DNS**
  - `curl -v https://srinidhi.dev/`
  - `curl -I https://srinidhi.dev/`
  - `curl -v https://srinidhi.dev/index.xml`
  - Optionally `dig srinidhi.dev` just to sanity check.

## Step-by-step Plan

Follow roughly this sequence (adapt as needed):

1. **Repo sanity check**
   - Confirm you’re in the correct repo and branch.
   - Inspect `hugo.toml`, `content/_index.md`, `content/about/_index.md`, and any custom layouts under `layouts/`.
   - Check the `[outputs]` section in `hugo.toml` (especially `home`).

2. **Local build verification**
   - Run `hugo --minify`.
   - Confirm that `public/index.html` exists and is valid HTML.
   - Confirm whether `public/index.xml` exists and, if so, what it contains.
   - Check a couple of section pages locally, e.g. `public/writing/first-post/index.html` and `public/about/index.html`.

3. **Check what GitHub Pages is serving**
   - Use `curl -v https://srinidhi.dev/` to see:
     - Final URL after redirects
     - `Content-Type` header
     - Whether GitHub is redirecting `/` to `/index.xml` or something weird.
   - Compare with `curl -v https://srinidhi621.github.io/` if relevant.
   - Check `curl -v https://srinidhi.dev/index.html` and `curl -v https://srinidhi.dev/index.xml`.

4. **Check workflow / artifact**
   - Inspect `.github/workflows/deploy.yml` to confirm:
     - It runs `hugo` in the repo root.
     - It uploads `./public` as the Pages artifact.
   - If needed, use `gh` to inspect the latest Pages build artifact or logs.

5. **Hypothesis and fix**
   - Form a hypothesis about why Pages is serving XML:
     - e.g. only `index.xml` being uploaded,
     - wrong publish directory,
     - or a Hugo outputs misconfiguration.
   - Implement a minimal fix. Examples (only if needed, based on findings):
     - Adjust `[outputs]` so `home` only outputs `HTML`.
     - Rename/move any custom layout that overrides the home template and forces XML.
     - Ensure the workflow uploads the correct directory.
     - Add or fix `content/_index.md` so the home page is a valid HTML list.

6. **Redeploy and verify**
   - Commit changes and push to `main`.
   - Wait for the GitHub Actions deploy to succeed.
   - Re-run:
     - `curl -I https://srinidhi.dev/`
     - `curl https://srinidhi.dev/ | head`
   - Make sure:
     - Status is `200`.
     - `Content-Type` is `text/html`.
     - The HTML body looks like the Hugo/PaperMod homepage.
   - Also hit `/writing/first-post/` and `/about/` to confirm they’re HTML too.

7. **Report back**
   - At the end, print a short, clear summary:
     - Root cause(s).
     - Exact changes made (files and lines).
     - How to reproduce the issue if needed.
     - How to confirm everything is working.

## Style / Constraints

- Prefer clear, incremental changes over large refactors.
- Explain your reasoning as you go in the Codex log so I can read the thought process later.
- Avoid touching unrelated files (keep the diff minimal and focused on the issue).
- If you’re unsure between two fixes, prefer the one that preserves standard Hugo/PaperMod defaults.

