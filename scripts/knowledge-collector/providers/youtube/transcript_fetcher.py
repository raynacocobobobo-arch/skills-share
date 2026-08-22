"""YouTube transcript fetcher interface.

Execution adapter for real transcript providers.

Priority:
1. Official captions
2. Creator captions
3. Automatic transcript
4. Whisper fallback
"""


def fetch_transcript(video_id):
    """Fetch transcript for a YouTube video.

    Real adapters will connect here.
    """
    raise NotImplementedError("Connect transcript provider")


def normalize_segments(segments):
    return "\n".join(
        segment.get("text", "") for segment in segments
    ).strip()
