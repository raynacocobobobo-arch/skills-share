"""Hermes knowledge asset storage interface."""

from pathlib import Path
import json
import re


RAW_YOUTUBE_DIR = Path("shared/knowledge-library/raw/youtube")
ANALYSIS_QUEUE_PATH = Path("shared/knowledge-library/analysis-queue.jsonl")


def save_metadata(directory, metadata):
    path = Path(directory) / "metadata.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2))
    return path


def slugify(value):
    slug = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return slug or "unknown"


def load_source_index(raw_dir=RAW_YOUTUBE_DIR):
    """Load collected source_ids by scanning immutable raw metadata files."""
    index = {}
    raw_path = Path(raw_dir)
    if not raw_path.exists():
        return index

    for metadata_path in raw_path.glob("*/*/metadata.json"):
        try:
            metadata = json.loads(metadata_path.read_text())
        except json.JSONDecodeError:
            continue
        source_id = metadata.get("source_id")
        if source_id:
            index[source_id] = {
                "path": str(metadata_path.parent),
                "metadata": metadata,
            }
    return index


def asset_directory(metadata, raw_dir=RAW_YOUTUBE_DIR):
    video_id = metadata["source_id"].split(":", 1)[1]
    return Path(raw_dir) / slugify(metadata["channel"]) / video_id


def save_youtube_asset(metadata, transcript, raw_dir=RAW_YOUTUBE_DIR):
    directory = asset_directory(metadata, raw_dir)
    directory.mkdir(parents=True, exist_ok=True)

    metadata_path = save_metadata(directory, metadata)
    transcript_path = directory / "transcript.md"
    transcript_path.write_text(transcript.strip() + "\n")

    source_info_path = directory / "source-info.md"
    source_info_path.write_text(
        "\n".join(
            [
                f"# {metadata['title']}",
                "",
                f"- Platform: {metadata['platform']}",
                f"- Channel: {metadata['channel']}",
                f"- URL: {metadata['url']}",
                f"- Published: {metadata.get('published') or 'unknown'}",
                f"- Collected at: {metadata['collected_at']}",
                "",
            ]
        )
    )

    return {
        "directory": directory,
        "metadata": metadata_path,
        "transcript": transcript_path,
        "source_info": source_info_path,
    }


def append_analysis_task(task, queue_path=ANALYSIS_QUEUE_PATH):
    path = Path(queue_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("", encoding="utf-8")

    existing = path.read_text().splitlines()
    for line in existing:
        if not line:
            continue
        try:
            existing_task = json.loads(line)
        except json.JSONDecodeError:
            continue
        if existing_task.get("source_id") == task.get("source_id"):
            return False

    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(task, ensure_ascii=False) + "\n")
    return True
