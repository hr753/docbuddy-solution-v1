def preflight(client, origin: str):
    return client.options(
        "/chat",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "X-API-Key, Content-Type",
        },
    )


def test_cors_allowed_origin_gets_header(client):
    r = preflight(client, "http://localhost:8501")
    assert r.status_code == 200
    assert r.headers["access-control-allow-origin"] == "http://localhost:8501"


def test_cors_unknown_origin_is_not_allowed(client):
    r = preflight(client, "https://evil.example.com")
    assert "access-control-allow-origin" not in r.headers
