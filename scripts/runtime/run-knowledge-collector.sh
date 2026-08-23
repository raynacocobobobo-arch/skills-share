#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Pulling latest..."
git pull --ff-only

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Running collector..."
source .venv/bin/activate
export HTTPS_PROXY=http://127.0.0.1:7890
export HTTP_PROXY=http://127.0.0.1:7890
export ALL_PROXY=http://127.0.0.1:7890
PYTHONDONTWRITEBYTECODE=1 python3 scripts/knowledge-collector/cli.py

if ! git diff --quiet -- shared/knowledge-library; then
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] New assets found, pushing..."
  git add shared/knowledge-library
  git commit -m "chore: collect knowledge assets"
  git push
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Push done."
else
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] No new assets."
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Complete."