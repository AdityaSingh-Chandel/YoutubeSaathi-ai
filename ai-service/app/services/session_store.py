"""Session storage interface. V1 = in-memory. V2 can add a Redis/Mongo implementation with the same methods."""
import threading
import time

from app.config.settings import settings
from app.models import errors
from app.models.session import AnalysisSession


class InMemorySessionStore:
    def __init__(self, ttl_seconds: int):
        self._ttl = ttl_seconds
        self._data: dict[str, AnalysisSession] = {}
        self._lock = threading.Lock()

    def _purge(self):
        now = time.time()
        for sid in [k for k, s in self._data.items() if now - s.created_at > self._ttl]:
            del self._data[sid]

    def put(self, session: AnalysisSession) -> None:
        with self._lock:
            self._purge()
            self._data[session.session_id] = session

    def get(self, session_id: str) -> AnalysisSession:
        with self._lock:
            self._purge()
            s = self._data.get(session_id)
        if s is None:
            raise errors.session_expired()
        return s

    def delete(self, session_id: str) -> None:
        with self._lock:
            self._data.pop(session_id, None)


store = InMemorySessionStore(settings.SESSION_TTL_SECONDS)
