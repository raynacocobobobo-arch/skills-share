"""Hermes Knowledge Collector CLI MVP."""

import argparse
from pathlib import Path

import yaml

from analysis_queue import create_analysis_task, should_analyze
from dedup import should_collect
from discovery import discover_sources
from providers.youtube.transcript_fetcher import fetch_transcript
from providers.youtube.youtube_provider import (
    build_metadata,
    format_published,
    get_latest_videos,
    get_video_details,
)
from storage import append_analysis_task, load_source_index, save_youtube_asset


DEFAULT_WATCHLIST = Path("plugins/hermes-skills/skills/hermes-knowledge-scout/config/watchlist.yaml")


def load_watchlist(path):
    return yaml.safe_load(Path(path).read_text())


def collect(watchlist, limit_sources=None, videos_per_source=5, cookie_path=None):
    sources = discover_sources(watchlist)
    if limit_sources:
        sources = sources[:limit_sources]

    index = load_source_index()
    collected = []
    skipped = []

    for source in sources:
        videos = get_latest_videos(source, limit=videos_per_source, cookie_path=cookie_path)
        if not videos:
            skipped.append({"source": source["name"], "reason": "no_video"})
            continue

        for video in videos:
            source_id = f"youtube:{video.video_id}"
            if not should_collect(index, source_id):
                skipped.append({
                    "source": source["name"],
                    "source_id": source_id,
                    "reason": "duplicate",
                })
                continue

            # 只有未采集的新视频才解析完整元数据，避免每天重复请求
            info = get_video_details(video.video_id, cookie_path)
            if info:
                video.title = info.get("title") or video.title
                video.channel = info.get("channel") or info.get("uploader") or video.channel
                video.url = info.get("webpage_url") or video.url
                video.published = format_published(info)

            metadata = build_metadata(
                video.video_id,
                video.title,
                video.channel,
                url=video.url,
                published=video.published,
            )

            transcript_result = fetch_transcript(
                video.video_id,
                languages=(source.get("language") or "en", "en"),
                cookie_path=cookie_path,
            )
            if transcript_result["status"] != "ok":
                skipped.append({
                    "source": source["name"],
                    "source_id": metadata["source_id"],
                    "reason": f"no_transcript:{transcript_result['reason']}",
                })
                continue

            paths = save_youtube_asset(metadata, transcript_result["transcript"])
            asset = {
                **metadata,
                "knowledge_type": source.get("knowledge_type", []),
                "asset_path": str(paths["directory"]),
            }
            queued = False
            if should_analyze(asset):
                task = create_analysis_task(asset)
                task["asset_path"] = asset["asset_path"]
                queued = append_analysis_task(task)

            index[metadata["source_id"]] = {"path": str(paths["directory"]), "metadata": metadata}
            collected.append({
                "source": source["name"],
                "source_id": metadata["source_id"],
                "path": str(paths["directory"]),
                "analysis_queued": queued,
            })

    return {
        "sources_found": len(sources),
        "collected": collected,
        "skipped": skipped,
        "status": "collection_complete",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hermes Knowledge Collector MVP")
    parser.add_argument("--watchlist", default=DEFAULT_WATCHLIST)
    parser.add_argument("--limit-sources", type=int, default=0, help="0 = all sources")
    parser.add_argument("--videos-per-source", type=int, default=5)
    parser.add_argument("--cookies", default=None, help="Netscape cookie file for YouTube auth")
    args = parser.parse_args()

    print(collect(
        load_watchlist(args.watchlist),
        limit_sources=args.limit_sources,
        videos_per_source=args.videos_per_source,
        cookie_path=args.cookies,
    ))
