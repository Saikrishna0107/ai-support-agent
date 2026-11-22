"""The FastAPI application: every URL the app answers is defined here."""

from fastapi import FastAPI

from app.config import settings

app = FastAPI(
    title=settings.app_name,
    description="AI customer support agent",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict:
    """Answer 'I'm alive' so we (and cloud hosts) can check the server is running."""
    return {"status": "ok"}
