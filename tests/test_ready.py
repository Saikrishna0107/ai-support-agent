"""Checks the /ready endpoint, with the database up and (pretend) down."""

import psycopg
import pytest
from fastapi.testclient import TestClient

from app.db import check_database
from app.main import app

client = TestClient(app)


def database_is_running() -> bool:
    try:
        check_database()
        return True
    except psycopg.Error:
        return False


# Skip (instead of fail) when the database container isn't started
requires_database = pytest.mark.skipif(
    not database_is_running(),
    reason="Database not running. Start it with: docker compose up -d",
)


@requires_database
def test_ready_when_database_is_up():
    response = client.get("/ready")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ready"
    assert body["pgvector"]  # e.g. "0.8.7"


def test_ready_returns_503_when_database_is_down(monkeypatch):
    # "monkeypatch" swaps the real database check for a fake one that fails,
    # so we can test the error path without actually stopping the database
    def broken_database():
        raise psycopg.OperationalError("connection refused")

    monkeypatch.setattr("app.main.check_database", broken_database)

    response = client.get("/ready")

    assert response.status_code == 503
    assert response.json()["detail"] == "Database unavailable"


def test_ready_returns_503_when_pgvector_is_missing(monkeypatch):
    monkeypatch.setattr(
        "app.main.check_database", lambda: {"postgres": "17.12", "pgvector": None}
    )

    response = client.get("/ready")

    assert response.status_code == 503
