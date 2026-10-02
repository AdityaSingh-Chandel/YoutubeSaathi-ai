"""Run from ai-service/:  python scripts/check_gemini.py
Tests the key, chat model and embedding model separately and prints the REAL error."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config.settings import settings
from google import genai
from google.genai import types

key = settings.GEMINI_API_KEY
print(f"Key loaded: {'YES (' + key[:4] + '...' + key[-3:] + ')' if key else 'NO  <-- .env not found/empty. It must be ai-service/.env'}")
print(f"Chat model: {settings.CHAT_MODEL} | Embedding model: {settings.EMBEDDING_MODEL} | dim: {settings.EMBEDDING_DIM}")
if not key:
    sys.exit(1)

client = genai.Client(api_key=key)

def step(name, fn):
    try:
        print(f"[OK]   {name}: {fn()}")
    except Exception as e:
        print(f"[FAIL] {name}: {type(e).__name__}: {e}")

step("chat", lambda: client.models.generate_content(model=settings.CHAT_MODEL, contents="Say hi").text.strip()[:40])
step("embedding", lambda: len(client.models.embed_content(
    model=settings.EMBEDDING_MODEL, contents=["hello world"],
    config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT", output_dimensionality=settings.EMBEDDING_DIM),
).embeddings[0].values))
