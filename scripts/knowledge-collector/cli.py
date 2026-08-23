"""Hermes Knowledge Collector CLI MVP."""

import argparse
from pathlib import Path

import yaml

from analysis_queue import create_analysis_task, should_analyze
from dedup import should_collect
from discovery import discover_sources
from providers.youtube.transcript_fetcher import fetch_transcript
from providers.youtube.youtube_provider import build_metadata, get_latest_videos
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
            metadata = build_metadata(
                video.video_id,
                video.title,
                video.channel,
                url=video.url,
                published=video.published,
            )

            if not should_collect(index, metadata["source_id"]):
                skipped.append({
                    "source": source["name"],
                    "source_id": metadata["source_id"],
                    "reason": "duplicate",
                })
                continue

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
