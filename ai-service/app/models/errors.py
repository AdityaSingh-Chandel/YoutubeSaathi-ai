class AppError(Exception):
    """Safe, user-facing error. Never put internals in `message`."""

    def __init__(self, status: int, code: str, message: str):
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message


def invalid_url():
    return AppError(400, "INVALID_URL", "Please enter a valid YouTube URL.")

def transcript_unavailable():
    return AppError(422, "TRANSCRIPT_UNAVAILABLE",
                    "Transcript is unavailable for this video, so the AI analysis cannot be performed.")

def ai_failed():
    return AppError(502, "AI_FAILED", "AI processing temporarily failed. Please try again.")

def rate_limited():
    return AppError(429, "RATE_LIMITED", "The AI service is temporarily rate-limited. Please try again later.")

def empty_question():
    return AppError(400, "EMPTY_QUESTION", "Please enter a question.")

def session_expired():
    return AppError(404, "SESSION_EXPIRED", "This analysis session has expired. Please analyze the video again.")
