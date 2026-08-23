#!/usr/bin/python3
"""Bilibili knowledge collector — 采集 B站 AI/创作 UP主 到 knowledge-library.

用系统 python 跑（依赖 bilibili_api，venv 里没有）。资产结构与 YouTube 对齐：
raw/bilibili/{up_name}/{bvid}/{metadata.json, transcript.md, source-info.md}

从 ~/skills-share 目录运行（storage.py 用相对路径 shared/knowledge-library/...）。
"""

import json
import sys
from pathlib import Path

import yaml

# 让 providers/ 和 storage 可 import
sys.path.insert(0, str(Path(__file__).resolve().parent))

from providers.bilibili.bilibili_provider import (
    build_metadata,
    fetch_subtitle,
    get_latest_videos,
)
from storage import load_source_index, save_youtube_asset

WATCHLIST = Path("plugins/hermes-skills/skills/hermes-knowledge-scout/config/watchlist.yaml")
RAW_BILIBILI_DIR = Path("shared/knowledge-library/raw/bilibili")


def collect_bilibili(watchlist, limit=5):
    sources = watchlist.get("sources", {}).get("bilibili", [])
    index = load_source_index(raw_dir=RAW_BILIBILI_DIR)
    collected = []
    skipped = []

    for source in sources:
        videos = get_latest_videos(source, limit=limit)
        if not videos:
            skipped.append({"source": source.get("name"), "reason": "no_video"})
            continue

        for v in videos:
            source_id = f"bilibili:{v['video_id']}"
            if source_id in index:
                skipped.append({"source": source.get("name"), "source_id": source_id, "reason": "duplicate"})
                continue

            sub = fetch_subtitle(v["video_id"])
            if not sub:
                skipped.append({"source": source.get("name"), "source_id": source_id, "reason": "no_subtitle"})
                continue

            metadata = build_metadata(v["video_id"], v["title"], v["channel"], url=v["url"], published=v["published"])
            paths = save_youtube_asset(metadata, sub, raw_dir=RAW_BILIBILI_DIR)
            index[source_id] = {"path": str(paths["directory"]), "metadata": metadata}
            collected.append({
                "source": source.get("name"),
                "source_id": source_id,
                "path": str(paths["directory"]),
            })

    return {
        "sources_found": len(sources),
        "collected": collected,
        "skipped": skipped,
        "status": "collection_complete",
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Bilibili knowledge collector")
    parser.add_argument("--watchlist", default=WATCHLIST)
    parser.add_argument("--videos-per-source", type=int, default=5)
    args = parser.parse_args()

    wl = yaml.safe_load(Path(args.watchlist).read_text())
    print(json.dumps(collect_bilibili(wl, limit=args.videos_per_source), ensure_ascii=False))
