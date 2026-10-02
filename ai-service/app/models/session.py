import time
import uuid
from dataclasses import dataclass, field
from typing import Any

from app.services.chunking.chunker import Chunk


@dataclass
class AnalysisSession:
    video_id: str
    title: str
    channel: str
    duration_seconds: int
    transcript: str
    chunks: list[Chunk]
    index: Any            # VectorIndex (FAISS)
    summary: str
    session_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    created_at: float = field(default_factory=time.time)
