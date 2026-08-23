#!/usr/bin/env bash
set -euo pipefail

SKILLS_SHARE="$HOME/skills-share"
DAILY_REPORT="$HOME/hermes-daily-report"
TODAY=$(date '+%Y-%m-%d')
NOW=$(date '+%Y-%m-%d %H:%M:%S')

cd "$SKILLS_SHARE"

echo "[$NOW] Pulling skills-share..."
git pull --ff-only

echo "[$NOW] Running collector..."
source .venv/bin/activate
export HTTPS_PROXY=http://127.0.0.1:7890
export HTTP_PROXY=http://127.0.0.1:7890
export ALL_PROXY=http://127.0.0.1:7890
PYTHONDONTWRITEBYTECODE=1 python3 scripts/knowledge-collector/cli.py --limit-sources 1

echo "[$NOW] Generating research input..."
PYTHONDONTWRITEBYTECODE=1 python3 scripts/generate-research-input.py

echo "[$NOW] Syncing to hermes-daily-report..."
cd "$DAILY_REPORT"
git pull --ff-only

# Sync raw transcripts
SUBTITLE_DIR="subtitles/$TODAY"
mkdir -p "$SUBTITLE_DIR"
cp -r "$SKILLS_SHARE"/shared/knowledge-library/raw/youtube/* "$SUBTITLE_DIR/" 2>/dev/null || true

# Sync research input
mkdir -p data/latest
cp "$SKILLS_SHARE"/data/latest/research-input.md data/latest/research-input.md

# Commit + push if changed
if ! git diff --quiet -- subtitles data/latest; then
  git add subtitles data/latest
  git commit -m "chore: daily collector run $TODAY"
  git push
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Push done."
else
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] No new data."
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Complete."