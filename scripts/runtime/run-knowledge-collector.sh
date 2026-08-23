#!/usr/bin/env bash
set -euo pipefail

SKILLS_SHARE="$HOME/skills-share"
DAILY_REPORT="$HOME/hermes-daily-report"
TODAY=$(date '+%Y-%m-%d')
NOW=$(date '+%Y-%m-%d %H:%M:%S')

cd "$SKILLS_SHARE"

COOKIES="$HOME/.hermes/cookies/youtube_cookies.txt"
if [[ ! -f "$COOKIES" ]]; then
  echo "[$NOW] WARN: YouTube cookies 缺失 ($COOKIES)，采集可能被反爬拦截"
fi

echo "[$NOW] Pulling skills-share..."
git pull --ff-only

echo "[$NOW] Running collector..."
source .venv/bin/activate
export HTTPS_PROXY=http://127.0.0.1:7890
export HTTP_PROXY=http://127.0.0.1:7890
export ALL_PROXY=http://127.0.0.1:7890
PYTHONDONTWRITEBYTECODE=1 python3 scripts/knowledge-collector/cli.py --cookies "$COOKIES"

echo "[$NOW] Running Bilibili collector..."
/usr/bin/python3 scripts/knowledge-collector/bilibili_collect.py

echo "[$NOW] Generating research input..."
PYTHONDONTWRITEBYTECODE=1 python3 scripts/generate-research-input.py

echo "[$NOW] Syncing to hermes-daily-report..."
cd "$DAILY_REPORT"
git pull --ff-only

SUBTITLE_DIR="subtitles/$TODAY"
mkdir -p "$SUBTITLE_DIR" data/latest

# Sync raw transcripts as flat .txt files matching existing schema
RAW_DIRS=(
  "$SKILLS_SHARE/shared/knowledge-library/raw/youtube"
  "$SKILLS_SHARE/shared/knowledge-library/raw/bilibili"
)
INDEX_ENTRIES=()
SUB_ADDED=0

for RAW_DIR in "${RAW_DIRS[@]}"; do
if [[ -d "$RAW_DIR" ]]; then
  for metadata_file in "$RAW_DIR"/*/*/metadata.json; do
    [[ -f "$metadata_file" ]] || continue

    channel=$(jq -r '.channel' "$metadata_file")
    title=$(jq -r '.title' "$metadata_file")
    url=$(jq -r '.url' "$metadata_file")
    video_id=$(jq -r '.source_id' "$metadata_file" | cut -d: -f2)
    asset_dir=$(dirname "$metadata_file")
    transcript_file="$asset_dir/transcript.md"

    if [[ ! -f "$transcript_file" ]]; then
      continue
    fi

    # Build flat .txt filename: {channel}-{title}.txt (truncate to 200 chars)
    safe_title=$(echo "$title" | tr '/' '_' | tr -d '\n' | head -c 200)
    txt_filename="${channel}-${safe_title}.txt"
    txt_path="$SUBTITLE_DIR/$txt_filename"

    # Build UP主 + 标题 header (matching existing Bilibili format)
    {
      echo "UP主：$channel"
      echo "标题：$title"
      echo "链接：$url"
      echo ""
      cat "$transcript_file"
    } > "$txt_path"

    size=$(stat -c%s "$txt_path")
    sha=$(sha256sum "$txt_path" | awk '{print $1}')

    INDEX_ENTRIES+=("$(jq -cn \
      --arg source "$txt_filename" \
      --arg up_name "$channel" \
      --arg title "$title" \
      --arg repository_path "subtitles/$TODAY/$txt_filename" \
      --arg sha256 "$sha" \
      --argjson size_bytes "$size" \
      '{
        source: $source,
        up_name: $up_name,
        title: $title,
        repository_path: $repository_path,
        format: "txt",
        size_bytes: $size_bytes,
        sha256: $sha256
      }')")

    SUB_ADDED=$((SUB_ADDED + 1))
    echo "  + $txt_filename"
  done
fi
done

# Generate index.json
if [[ ${#INDEX_ENTRIES[@]} -gt 0 ]]; then
  ENTRIES_JSON=$(printf '%s\n' "${INDEX_ENTRIES[@]}" | jq -s 'sort_by(.source)')
else
  ENTRIES_JSON='[]'
fi

jq -n \
  --arg schema_version "2.1" \
  --arg date "$TODAY" \
  --arg generated_at "$(date -Iseconds)" \
  --arg source_directory "subtitles/$TODAY" \
  --argjson total "$SUB_ADDED" \
  --argjson rejected 0 \
  --argjson entries "$ENTRIES_JSON" \
  '{
    schema_version: $schema_version,
    date: $date,
    generated_at: $generated_at,
    total: $total,
    rejected: $rejected,
    source_directory: $source_directory,
    entries: $entries
  }' > "$SUBTITLE_DIR/index.json"

echo "  index.json: $SUB_ADDED entries"

# Sync research input
cp "$SKILLS_SHARE"/data/latest/research-input.md data/latest/research-input.md

# Commit + push
if ! git diff --quiet -- subtitles data/latest; then
  git add subtitles data/latest
  git commit -m "同步 $TODAY (YT+BL:$SUB_ADDED)"
  git push
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Push done."
else
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] No new data."
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Complete."