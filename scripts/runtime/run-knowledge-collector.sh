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
PYTHONDONTWRITEBYTECODE=1 python3 scripts/knowledge-collector/cli.py --limit-sources 1

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Generating research input..."
PYTHONDONTWRITEBYTECODE=1 python3 scripts/generate-research-input.py

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Syncing data to hermes-daily-report..."
DAILY_REPORT_DIR="$HOME/hermes-daily-report"
cp data/latest/research-input.md "$DAILY_REPORT_DIR/data/latest/research-input.md"
cd "$DAILY_REPORT_DIR"
git pull --ff-only
if ! git diff --quiet -- data/latest; then
  git add data/latest
  git commit -m "chore: daily research input $(date '+%Y-%m-%d')"
  git push
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Push to hermes-daily-report done."
else
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] No new data to push."
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Complete."