"""Checks that the /health endpoint works."""

from fastapi.testclient import TestClient

from app.main import app

# A fake browser that sends requests straight to our app (no server needed)
client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200  # 200 means "success"
    assert response.json() == {"status": "ok"}
