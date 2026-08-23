# Hermes Knowledge Collector

## Purpose

MVP execution layer for Hermes external knowledge acquisition.

This layer collects and normalizes external sources. It does not decide skill upgrades.

## Pipeline

```
watchlist.yaml
    ↓
discovery
    ↓
dedup/index check
    ↓
transcript collection
    ↓
metadata generation
    ↓
knowledge-library/raw
```

## YouTube MVP

Run the first real collection chain against the first enabled YouTube channel
in the watchlist:

```bash
python3 scripts/knowledge-collector/cli.py --limit-sources 1
```

Dependencies:

```bash
python3 -m pip install PyYAML yt-dlp youtube-transcript-api
```

Rules:

- Channel discovery uses the YouTube channel's videos feed through `yt-dlp`.
- Transcript collection uses existing YouTube captions only.
- Videos without accessible captions are skipped.
- Whisper or other audio transcription is intentionally not used in this MVP.
- Raw assets are saved under `shared/knowledge-library/raw/youtube/<channel>/<video_id>/`.
- Existing `source_id` values are skipped by scanning raw `metadata.json` files.
- Assets with `workflow`, `methodology`, or `prompt_method` enter `shared/knowledge-library/analysis-queue.jsonl`.

## Planned Modules

```
knowledge-collector/

cli.py
scheduler.py
discovery.py
dedup.py
transcript.py
storage.py
```

## Rules

- Never duplicate collected assets.
- Keep raw sources immutable.
- Analysis is a separate stage.
