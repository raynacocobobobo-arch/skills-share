#!/usr/bin/env bash
set -euo pipefail

repo_dir="${HERMES_KNOWLEDGE_REPO:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"

cd "$repo_dir"

if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "Refusing to sync: working tree has uncommitted changes." >&2
  git status --short >&2
  exit 1
fi

git fetch origin main
git pull --ff-only origin main

python3 scripts/validate-skills.py --write-registry

echo "Hermes knowledge synced: $(git rev-parse --short HEAD)"

