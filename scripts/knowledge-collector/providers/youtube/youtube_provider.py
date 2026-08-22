"""YouTube provider MVP for Hermes Knowledge Collector.

The provider separates source acquisition from knowledge analysis.
"""

from dataclasses import dataclass


@dataclass
class YouTubeAsset:
    video_id: str
    title: str
    channel: str
    url: str


def build_metadata(video_id, title, channel):
    return {
        "source_id": f"youtube:{video_id}",
        "platform": "youtube",
        "title": title,
        "channel": channel,
        "status": "collected",
    }


def build_transcript_asset(metadata, transcript):
    return {
        "metadata": metadata,
        "transcript": transcript,
        "status": "normalized",
    }


# Real API/transcript adapters will plug into this interface.
