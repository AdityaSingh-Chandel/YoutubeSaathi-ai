from app.config.settings import settings
from app.prompts.summary import COMBINE_PROMPT, PART_SUMMARY_PROMPT, SUMMARY_PROMPT
from app.services.chunking.chunker import WORDS_PER_TOKEN
from app.services.llm_client import generate_text


def summarize(transcript: str) -> str:
    """One Gemini call normally. Hierarchical (parts -> combine) only for very long transcripts."""
    words = transcript.split()
    limit_words = int(settings.SUMMARY_DIRECT_TOKEN_LIMIT * WORDS_PER_TOKEN)
    if len(words) <= limit_words:
        return generate_text(SUMMARY_PROMPT.format(transcript=transcript))

    parts = [" ".join(words[i:i + limit_words]) for i in range(0, len(words), limit_words)]
    partials = [generate_text(PART_SUMMARY_PROMPT.format(transcript=p)) for p in parts]
    joined = "\n\n".join(f"Part {i + 1}:\n{s}" for i, s in enumerate(partials))
    return generate_text(COMBINE_PROMPT.format(summaries=joined))
