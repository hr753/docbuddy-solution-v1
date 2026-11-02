import pytest


def test_documents_valid_returns_201_with_id(client, auth_headers):
    r = client.post("/documents", json={"title": "FAQ", "content": "Hello."}, headers=auth_headers)
    assert r.status_code == 201
    assert r.json() == {"id": 1, "title": "FAQ", "chars": 6}


def test_documents_missing_key_returns_401(client):
    r = client.post("/documents", json={"title": "FAQ", "content": "Hello."})
    assert r.status_code == 401
    assert r.json() == {"detail": "Invalid or missing API key"}


def test_documents_wrong_key_returns_401(client):
    r = client.post(
        "/documents", json={"title": "FAQ", "content": "Hello."}, headers={"X-API-Key": "nope"}
    )
    assert r.status_code == 401


@pytest.mark.parametrize(
    "body",
    [
        {"title": "", "content": "x"},  # empty title
        {"title": "   ", "content": "x"},  # whitespace only -> stripped -> empty
        {"title": "x" * 201, "content": "x"},  # title too long
        {"title": "x", "content": "x" * 20_001},  # content too long
        {"title": "x"},  # content missing
        {"title": "x", "content": "x", "owner": "me"},  # unknown field
    ],
)
def test_documents_invalid_body_returns_422(client, auth_headers, body):
    assert client.post("/documents", json=body, headers=auth_headers).status_code == 422
