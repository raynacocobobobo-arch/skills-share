"""YouTube transcript fetcher.

This collector only uses captions already available on YouTube. It does not
fall back to Whisper; videos without accessible captions are skipped.
"""


def fetch_transcript(video_id, languages=("en",)):
    """Fetch an existing YouTube transcript.

    Returns a dict with ``status=ok`` and normalized text, or ``status=skip``
    when captions are not available.
    """
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        from youtube_transcript_api._errors import CouldNotRetrieveTranscript
    except ImportError as exc:
        raise RuntimeError(
            "Missing dependency: install youtube-transcript-api to fetch captions."
        ) from exc

    try:
        transcript = YouTubeTranscriptApi().fetch(video_id, languages=languages)
    except CouldNotRetrieveTranscript as exc:
        return {
            "status": "skip",
            "reason": exc.__class__.__name__,
            "transcript": "",
        }

    return {
        "status": "ok",
        "reason": None,
        "transcript": normalize_segments(transcript),
    }


def normalize_segments(segments):
    lines = []
    for segment in segments:
        if hasattr(segment, "text"):
            text = segment.text
        else:
            text = segment.get("text", "")
        text = " ".join(text.split())
        if text:
            lines.append(text)
    return "\n".join(lines).strip()
