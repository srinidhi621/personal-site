#!/usr/bin/env bash
set -euo pipefail

repo_root=$(git rev-parse --show-toplevel)
cd "$repo_root"

current_branch=$(git rev-parse --abbrev-ref HEAD)
if [[ "$current_branch" != "main" ]]; then
  echo "Error: run this from the main worktree (current: $current_branch)." >&2
  exit 1
fi

if ! git show-ref --verify --quiet refs/heads/staging; then
  echo "Error: staging branch not found." >&2
  exit 1
fi

if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "Error: working tree is not clean. Commit or stash changes first." >&2
  exit 1
fi

git merge --no-ff -m "Merge staging into main" staging
