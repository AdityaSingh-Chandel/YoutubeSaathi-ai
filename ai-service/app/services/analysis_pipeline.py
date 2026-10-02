"""The whole 'Analyze' flow. Framework-free so it can later run in a worker or CLI."""
from app.config.settings import settings
from app.models import errors
from app.models.session import AnalysisSession
from app.services.chunking.chunker import chunk_segments
from app.services.embeddings.gemini_embedder import embed_documents
from app.services.session_store import store
from app.services.summarization.summarizer import summarize
from app.services.transcript import youtube
from app.services.transcript.cleaner import clean_segments, to_text
from app.services.vector_store.faiss_index import VectorIndex


def analyze_video(url: str) -> AnalysisSession:
    video_id = youtube.extract_video_id(url)
    segments = clean_segments(youtube.fetch_transcript(video_id))
    if not segments:
        raise errors.transcript_unavailable()

    meta = youtube.fetch_metadata(video_id)
    transcript = to_text(segments)
    duration = int(segments[-1].start + segments[-1].duration)

    chunks = chunk_segments(segments, settings.CHUNK_TOKENS, settings.CHUNK_OVERLAP_RATIO)
    vectors = embed_documents([c.text for c in chunks])   # once per analysis
    index = VectorIndex(vectors)
    summary = summarize(transcript)                        # once per analysis

    session = AnalysisSession(
        video_id=video_id, title=meta["title"], channel=meta["channel"],
        duration_seconds=duration, transcript=transcript,
        chunks=chunks, index=index, summary=summary,
    )
    store.put(session)
    return session
