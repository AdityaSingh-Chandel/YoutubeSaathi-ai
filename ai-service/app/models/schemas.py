from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    youtube_url: str


class QuestionRequest(BaseModel):
    session_id: str
    question: str


class VideoInfo(BaseModel):
    id: str
    title: str
    channel: str
    duration_seconds: int


class AnalyzeResponse(BaseModel):
    session_id: str
    video: VideoInfo
    summary: str
    transcript: str


class QuestionResponse(BaseModel):
    answer: str
    grounded: bool
