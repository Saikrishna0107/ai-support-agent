"""The FastAPI application: every URL the app answers is defined here."""

import psycopg
from fastapi import FastAPI, HTTPException

from app.config import settings
from app.db import check_database

app = FastAPI(
    title=settings.app_name,
    description="AI customer support agent",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict:
    """Liveness check: answer 'I'm alive' so we (and cloud hosts) know the server is running."""
    return {"status": "ok"}


@app.get("/ready")
def ready() -> dict:
    """Readiness check: can the app do its job? (database reachable, pgvector on)"""
    try:
        versions = check_database()
    except psycopg.Error as error:
        # 503 = "Service Unavailable": alive, but can't do its job right now
        raise HTTPException(status_code=503, detail="Database unavailable") from error

    if versions["pgvector"] is None:
        raise HTTPException(status_code=503, detail="pgvector extension is not installed")

    return {"status": "ready", "database": "connected", **versions}
