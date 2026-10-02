"""Single place that talks to Gemini (generation). Embeddings use the same client."""
import logging

from google import genai
from google.genai import types

from app.config.settings import settings
from app.models import errors

log = logging.getLogger(__name__)
_client = None


def get_client():
    global _client
    if _client is None:
        if not settings.GEMINI_API_KEY:
            log.error("GEMINI_API_KEY is not set")
            raise errors.ai_failed()
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _client


def to_app_error(exc: Exception) -> errors.AppError:
    if isinstance(exc, errors.AppError):
        return exc
    log.exception("Gemini call failed")  # details stay in server logs only
    if getattr(exc, "code", None) == 429:
        return errors.rate_limited()
    return errors.ai_failed()


def generate_text(prompt: str, system: str | None = None, json_mode: bool = False,
                  temperature: float = 0.2) -> str:
    cfg = types.GenerateContentConfig(
        system_instruction=system,
        temperature=temperature,
        response_mime_type="application/json" if json_mode else None,
    )
    try:
        resp = get_client().models.generate_content(
            model=settings.CHAT_MODEL, contents=prompt, config=cfg
        )
        text = (resp.text or "").strip()
    except Exception as exc:
        raise to_app_error(exc)
    if not text:
        raise errors.ai_failed()
    return text
