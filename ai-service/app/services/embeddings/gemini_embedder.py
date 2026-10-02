import numpy as np
from google.genai import types

from app.config.settings import settings
from app.services.llm_client import get_client, to_app_error


def _normalize(m: np.ndarray) -> np.ndarray:
    # Reduced-dimension Gemini embeddings are not unit length; normalize for cosine via inner product.
    norms = np.linalg.norm(m, axis=1, keepdims=True)
    norms[norms == 0] = 1
    return (m / norms).astype("float32")


def _embed(texts: list[str], task_type: str) -> np.ndarray:
    cfg = types.EmbedContentConfig(task_type=task_type, output_dimensionality=settings.EMBEDDING_DIM)
    vectors: list[list[float]] = []
    try:
        for i in range(0, len(texts), settings.EMBED_BATCH_SIZE):
            batch = texts[i:i + settings.EMBED_BATCH_SIZE]
            resp = get_client().models.embed_content(
                model=settings.EMBEDDING_MODEL, contents=batch, config=cfg
            )
            vectors.extend(e.values for e in resp.embeddings)
    except Exception as exc:
        raise to_app_error(exc)
    return _normalize(np.array(vectors, dtype="float32"))


def embed_documents(texts: list[str]) -> np.ndarray:
    return _embed(texts, "RETRIEVAL_DOCUMENT")


def embed_query(text: str) -> np.ndarray:
    return _embed([text], "RETRIEVAL_QUERY")[0]
