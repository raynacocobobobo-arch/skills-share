"""YouTube transcript fetcher.

This collector only uses captions already available on YouTube. It does not
fall back to Whisper; videos without accessible captions are skipped.
"""


def _build_api(cookie_path=None):
    """Build a YouTubeTranscriptApi, optionally injecting Netscape cookies.

    youtube-transcript-api 1.x disabled its own cookie_path argument, but it
    accepts a custom ``requests.Session``. We load the Netscape cookie file into
    a MozillaCookieJar and hand it a pre-authenticated session.
    """
    from youtube_transcript_api import YouTubeTranscriptApi

    if not cookie_path:
        return YouTubeTranscriptApi()

    import http.cookiejar

    import requests

    jar = http.cookiejar.MozillaCookieJar(cookie_path)
    jar.load(ignore_discard=True, ignore_expires=True)
    session = requests.Session()
    session.cookies.update(jar)
    return YouTubeTranscriptApi(http_client=session)


def fetch_transcript(video_id, languages=("en",), cookie_path=None):
    """Fetch an existing YouTube transcript.

    Returns a dict with ``status=ok`` and normalized text, or ``status=skip``
    when captions are not available.
    """
    try:
        from youtube_transcript_api._errors import CouldNotRetrieveTranscript
    except ImportError as exc:
        raise RuntimeError(
            "Missing dependency: install youtube-transcript-api to fetch captions."
        ) from exc

    try:
        api = _build_api(cookie_path)
        transcript = api.fetch(video_id, languages=languages)
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
