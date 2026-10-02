"""YouTube URL parsing, transcript and basic metadata. Replace this file to swap transcript providers."""
import logging
import re
from dataclasses import dataclass
from urllib.parse import parse_qs, urlparse

import httpx
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import CouldNotRetrieveTranscript, NoTranscriptFound

from app.models import errors

log = logging.getLogger(__name__)
_ID_RE = re.compile(r"^[\w-]{11}$")
_YT_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com"}


@dataclass
class Segment:
    text: str
    start: float
    duration: float


def extract_video_id(url: str) -> str:
    try:
        u = urlparse(url.strip())
    except Exception:
        raise errors.invalid_url()
    host = (u.hostname or "").lower()
    vid = None
    if host == "youtu.be":
        vid = u.path.lstrip("/").split("/")[0]
    elif host in _YT_HOSTS:
        if u.path == "/watch":
            vid = (parse_qs(u.query).get("v") or [None])[0]
        else:
            m = re.match(r"^/(?:shorts|embed)/([\w-]{11})", u.path)
            vid = m.group(1) if m else None
    if not vid or not _ID_RE.match(vid):
        raise errors.invalid_url()
    return vid


def fetch_transcript(video_id: str) -> list[Segment]:
    api = YouTubeTranscriptApi()
    try:
        transcripts = api.list(video_id)
        try:
            t = transcripts.find_transcript(["en", "en-US", "en-GB"])
        except NoTranscriptFound:
            t = next(iter(transcripts))  # fall back to the video's original/first language
        fetched = t.fetch()
        segments = [Segment(s.text, float(s.start), float(s.duration)) for s in fetched]
    except (CouldNotRetrieveTranscript, StopIteration):
        raise errors.transcript_unavailable()
    except Exception:
        log.exception("Unexpected transcript error")
        raise errors.transcript_unavailable()
    if not segments:
        raise errors.transcript_unavailable()
    return segments


def fetch_metadata(video_id: str) -> dict:
    """Title/channel via YouTube oEmbed (no API key). Non-fatal if it fails."""
    try:
        r = httpx.get(
            "https://www.youtube.com/oembed",
            params={"url": f"https://www.youtube.com/watch?v={video_id}", "format": "json"},
            timeout=10,
        )
        r.raise_for_status()
        d = r.json()
        return {"title": d.get("title", "Unknown title"), "channel": d.get("author_name", "Unknown channel")}
    except Exception:
        log.warning("oEmbed lookup failed for %s", video_id)
        return {"title": "Unknown title", "channel": "Unknown channel"}
