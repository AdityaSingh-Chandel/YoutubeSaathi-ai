import json
import logging

from app.config.settings import settings
from app.models.session import AnalysisSession
from app.prompts.qa import QA_SYSTEM, QA_USER
from app.services.embeddings.gemini_embedder import embed_query
from app.services.llm_client import generate_text

log = logging.getLogger(__name__)


def answer_question(session: AnalysisSession, question: str) -> dict:
    """Embed question -> FAISS top-k -> Gemini with only those chunks. Nothing else is recomputed."""
    hits = session.index.search(embed_query(question), settings.TOP_K)
    hits.sort(key=lambda h: h[0])  # keep transcript order for readability
    context = "\n\n".join(
        f"[Excerpt {n + 1}]\n{session.chunks[i].text}" for n, (i, _score) in enumerate(hits)
    )
    raw = generate_text(
        QA_USER.format(context=context, question=question),
        system=QA_SYSTEM,
        json_mode=True,
    )
    try:
        data = json.loads(raw)
        return {"answer": str(data["answer"]).strip(), "grounded": bool(data["grounded"])}
    except (json.JSONDecodeError, KeyError, TypeError):
        log.warning("Model returned non-JSON answer")
        return {"answer": raw, "grounded": False}  # be conservative if we can't verify
