import html
import re

from app.services.transcript.youtube import Segment

_TAGS = re.compile(r"\[[^\]]*\]")   # [Music], [Applause]
_WS = re.compile(r"\s+")


def clean_segments(segments: list[Segment]) -> list[Segment]:
    """Light cleanup only: keep the spoken words intact."""
    out: list[Segment] = []
    prev = None
    for s in segments:
        text = html.unescape(s.text)
        text = _TAGS.sub(" ", text).replace(">>", " ")
        text = _WS.sub(" ", text).strip()
        if not text or text == prev:   # drop empties and immediate repeats
            continue
        out.append(Segment(text, s.start, s.duration))
        prev = text
    return out


def to_text(segments: list[Segment]) -> str:
    return " ".join(s.text for s in segments)
