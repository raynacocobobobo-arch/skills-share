#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting knowledge collector run..."

git pull --ff-only

source .venv/bin/activate
export HTTPS_PROXY=http://127.0.0.1:7890
export HTTP_PROXY=http://127.0.0.1:7890
export ALL_PROXY=http://127.0.0.1:7890
PYTHONDONTWRITEBYTECODE=1 python3 scripts/knowledge-collector/cli.py

if ! git diff --quiet -- shared/knowledge-library; then
  git add shared/knowledge-library
  git commit -m "chore: collect knowledge assets"
  git push
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Pushed new assets."
else
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] No new assets to push."
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Run complete."