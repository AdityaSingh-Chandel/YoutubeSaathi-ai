from dataclasses import dataclass

from app.services.transcript.youtube import Segment

WORDS_PER_TOKEN = 0.75  # rough estimate; no tokenizer needed for V1


@dataclass
class Chunk:
    chunk_id: int
    text: str
    start: float  # seconds; kept for future timestamp support


def _make(chunk_id: int, segs: list[Segment]) -> Chunk:
    return Chunk(chunk_id, " ".join(s.text for s in segs), segs[0].start)


def chunk_segments(segments: list[Segment], chunk_tokens: int, overlap_ratio: float) -> list[Chunk]:
    max_words = max(50, int(chunk_tokens * WORDS_PER_TOKEN))
    overlap_words = int(max_words * overlap_ratio)
    chunks: list[Chunk] = []
    cur: list[Segment] = []
    cur_words = 0
    for seg in segments:
        w = len(seg.text.split())
        if cur and cur_words + w > max_words:
            chunks.append(_make(len(chunks), cur))
            keep: list[Segment] = []
            kw = 0
            for s in reversed(cur):          # carry the tail over as overlap
                sw = len(s.text.split())
                if kw + sw > overlap_words:
                    break
                keep.insert(0, s)
                kw += sw
            cur, cur_words = keep, kw
        cur.append(seg)
        cur_words += w
    if cur:
        chunks.append(_make(len(chunks), cur))
    return chunks
