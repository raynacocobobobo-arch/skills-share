import json

import sys
from pathlib import Path


COLLECTOR_DIR = Path(__file__).resolve().parents[1] / "scripts" / "knowledge-collector"
sys.path.insert(0, str(COLLECTOR_DIR))

from providers.youtube.transcript_fetcher import normalize_segments
from storage import append_analysis_task, load_source_index, save_youtube_asset


def test_save_youtube_asset_and_load_source_index(tmp_path):
    metadata = {
        "source_id": "youtube:abc123",
        "platform": "youtube",
        "channel": "OpenAI",
        "title": "Demo",
        "url": "https://www.youtube.com/watch?v=abc123",
        "published": "2026-08-23",
        "collected_at": "2026-08-23T00:00:00+00:00",
    }

    paths = save_youtube_asset(metadata, "hello\nworld", raw_dir=tmp_path)

    assert paths["directory"] == tmp_path / "openai" / "abc123"
    assert json.loads(paths["metadata"].read_text())["source_id"] == "youtube:abc123"
    assert paths["transcript"].read_text() == "hello\nworld\n"
    assert "https://www.youtube.com/watch?v=abc123" in paths["source_info"].read_text()

    index = load_source_index(raw_dir=tmp_path)
    assert "youtube:abc123" in index


def test_append_analysis_task_is_deduped(tmp_path):
    queue_path = tmp_path / "analysis-queue.jsonl"
    task = {"source_id": "youtube:abc123", "task": "knowledge_extraction", "status": "pending"}

    assert append_analysis_task(task, queue_path=queue_path) is True
    assert append_analysis_task(task, queue_path=queue_path) is False
    assert len(queue_path.read_text().splitlines()) == 1


def test_normalize_segments_supports_dicts_and_snippets():
    class Snippet:
        text = "  second   line "

    assert normalize_segments([{"text": " first   line "}, Snippet()]) == "first line\nsecond line"
