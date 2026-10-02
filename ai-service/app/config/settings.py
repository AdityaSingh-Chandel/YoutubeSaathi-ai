import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    CHAT_MODEL: str = os.getenv("GEMINI_CHAT_MODEL", "gemini-2.5-flash")
    EMBEDDING_MODEL: str = os.getenv("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001")
    EMBEDDING_DIM: int = int(os.getenv("EMBEDDING_DIM", "768"))
    CHUNK_TOKENS: int = int(os.getenv("CHUNK_TOKENS", "700"))
    CHUNK_OVERLAP_RATIO: float = float(os.getenv("CHUNK_OVERLAP_RATIO", "0.15"))
    TOP_K: int = int(os.getenv("TOP_K", "4"))
    SESSION_TTL_SECONDS: int = int(os.getenv("SESSION_TTL_SECONDS", "3600"))
    SUMMARY_DIRECT_TOKEN_LIMIT: int = int(os.getenv("SUMMARY_DIRECT_TOKEN_LIMIT", "60000"))
    EMBED_BATCH_SIZE: int = 100  # Gemini batch limit


settings = Settings()
