import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.routes import router
from app.models.errors import AppError

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

app = FastAPI(title="YouTube AI Analyzer - AI Service")
app.include_router(router)


def _err(status: int, code: str, message: str):
    return JSONResponse(status_code=status, content={"error": {"code": code, "message": message}})


@app.exception_handler(AppError)
async def app_error_handler(_: Request, exc: AppError):
    return _err(exc.status, exc.code, exc.message)


@app.exception_handler(RequestValidationError)
async def validation_handler(_: Request, __: RequestValidationError):
    return _err(400, "INVALID_REQUEST", "Invalid request.")


@app.exception_handler(Exception)
async def unhandled_handler(_: Request, exc: Exception):
    log.exception("Unhandled error")  # stack trace stays in server logs
    return _err(500, "AI_FAILED", "AI processing temporarily failed. Please try again.")
