"""Hermes knowledge asset storage interface."""

from pathlib import Path
import json


def save_metadata(directory, metadata):
    path = Path(directory) / "metadata.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2))
    return path
