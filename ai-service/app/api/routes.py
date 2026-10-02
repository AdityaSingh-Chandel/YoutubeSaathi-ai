from fastapi import APIRouter

from app.models import errors
from app.models.schemas import (AnalyzeRequest, AnalyzeResponse, QuestionRequest,
                                QuestionResponse, VideoInfo)
from app.services.analysis_pipeline import analyze_video
from app.services.qa.answerer import answer_question
from app.services.session_store import store

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    s = analyze_video(req.youtube_url)
    return AnalyzeResponse(
        session_id=s.session_id,
        video=VideoInfo(id=s.video_id, title=s.title, channel=s.channel,
                        duration_seconds=s.duration_seconds),
        summary=s.summary,
        transcript=s.transcript,
    )


@router.post("/question", response_model=QuestionResponse)
def question(req: QuestionRequest):
    q = req.question.strip()
    if not q:
        raise errors.empty_question()
    session = store.get(req.session_id)
    return QuestionResponse(**answer_question(session, q))


@router.delete("/session/{session_id}")
def delete_session(session_id: str):
    store.delete(session_id)
    return {"deleted": True}
