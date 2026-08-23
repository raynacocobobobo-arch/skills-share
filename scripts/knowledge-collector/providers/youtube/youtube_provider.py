"""YouTube provider MVP for Hermes Knowledge Collector.

The provider separates source acquisition from knowledge analysis.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


YOUTUBE_WATCH_URL = "https://www.youtube.com/watch?v={video_id}"


@dataclass
class YouTubeAsset:
    video_id: str
    title: str
    channel: str
    url: str
    published: Optional[str] = None


def get_latest_videos(source, limit=5):
    """Resolve a watchlist source to its N latest YouTube videos (most recent first)."""
    try:
        import yt_dlp
    except ImportError as exc:
        raise RuntimeError("Missing dependency: install yt-dlp to discover YouTube videos.") from exc

    channel_url = source.get("url") or source.get("channel_url")
    if not channel_url:
        channel_url = resolve_channel_url(source["name"], yt_dlp)

    videos_url = channel_url.rstrip("/") + "/videos"
    opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": True,
        "playlistend": limit,
        "ignoreerrors": True,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        playlist = ydl.extract_info(videos_url, download=False)

    entries = [entry for entry in playlist.get("entries", []) if entry]
    if not entries:
        return []

    videos = []
    for flat_video in entries:
        video_id = flat_video["id"]
        try:
            with yt_dlp.YoutubeDL({"quiet": True, "skip_download": True}) as ydl:
                info = ydl.extract_info(YOUTUBE_WATCH_URL.format(video_id=video_id), download=False)
        except Exception:
            info = None

        videos.append(YouTubeAsset(
            video_id=video_id,
            title=(info.get("title") if info else None) or flat_video.get("title") or "",
            channel=(info.get("channel") if info else None)
                    or (info.get("uploader") if info else None)
                    or flat_video.get("channel")
                    or flat_video.get("uploader")
                    or source["name"],
            url=(info.get("webpage_url") if info else None) or YOUTUBE_WATCH_URL.format(video_id=video_id),
            published=format_published(info) if info else None,
        ))
    return videos


def get_latest_video(source):
    """Resolve a watchlist source to its latest YouTube video."""
    videos = get_latest_videos(source, limit=1)
    return videos[0] if videos else None


def resolve_channel_url(channel_name, yt_dlp):
    """Find the best channel URL for a watchlist channel name."""
    opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": True,
        "playlistend": 5,
        "ignoreerrors": True,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        results = ydl.extract_info(f"ytsearch5:{channel_name} YouTube channel", download=False)

    normalized_name = channel_name.casefold()
    for entry in results.get("entries", []):
        if not entry:
            continue
        entry_channel = (entry.get("channel") or entry.get("uploader") or "").casefold()
        channel_url = entry.get("channel_url")
        if channel_url and entry_channel == normalized_name:
            return channel_url

    for entry in results.get("entries", []):
        if entry and entry.get("channel_url"):
            return entry["channel_url"]

    raise RuntimeError(f"Could not resolve YouTube channel: {channel_name}")


def format_published(info):
    timestamp = info.get("timestamp") or info.get("release_timestamp")
    if timestamp:
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()

    upload_date = info.get("upload_date")
    if upload_date and len(upload_date) == 8:
        return f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"

    return None


def build_metadata(video_id, title, channel, url=None, published=None, collected_at=None):
    return {
        "source_id": f"youtube:{video_id}",
        "platform": "youtube",
        "channel": channel,
        "title": title,
        "url": url or YOUTUBE_WATCH_URL.format(video_id=video_id),
        "published": published,
        "collected_at": collected_at or datetime.now(timezone.utc).isoformat(),
    }


def build_transcript_asset(metadata, transcript):
    return {
        "metadata": metadata,
        "transcript": transcript,
        "status": "normalized",
    }


# Real API/transcript adapters will plug into this interface.
