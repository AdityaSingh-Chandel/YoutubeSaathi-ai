import faiss
import numpy as np


class VectorIndex:
    """Temporary per-session FAISS index (cosine similarity via normalized inner product)."""

    def __init__(self, vectors: np.ndarray):
        vectors = np.ascontiguousarray(vectors, dtype="float32")
        self._index = faiss.IndexFlatIP(vectors.shape[1])
        self._index.add(vectors)

    def search(self, query: np.ndarray, k: int) -> list[tuple[int, float]]:
        q = np.ascontiguousarray(query.reshape(1, -1), dtype="float32")
        scores, ids = self._index.search(q, min(k, self._index.ntotal))
        return [(int(i), float(s)) for i, s in zip(ids[0], scores[0]) if i >= 0]
