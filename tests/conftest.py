"""Shared test fixtures. Test keys are set here once, never inside test files."""

import os

import pytest
from fastapi.testclient import TestClient

TEST_KEY = "test-key-only-for-pytest"
os.environ["API_KEYS"] = TEST_KEY
os.environ["CORS_ORIGINS"] = "http://localhost:8501"
os.environ["LLM_PROVIDER"] = "fake"
os.environ["STREAM_DELAY_SECONDS"] = "0"


@pytest.fixture
def client():
    from app.config import get_settings
    from app.main import create_app

    get_settings.cache_clear()  # re-read env so every test gets a fresh app and empty store
    with TestClient(create_app()) as c:
        yield c


@pytest.fixture
def auth_headers() -> dict[str, str]:
    return {"X-API-Key": TEST_KEY}


@pytest.fixture
def leave_policy(client, auth_headers):
    r = client.post(
        "/documents",
        json={
            "title": "Leave policy",
            "content": "Employees get 24 days of paid leave per year. "
            "Unused leave can be carried over up to 10 days.",
        },
        headers=auth_headers,
    )
    assert r.status_code == 201
    return r.json()
