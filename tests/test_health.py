def test_health_no_key_needed_returns_200(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok", "version": "0.1.0", "documents": 0}


def test_health_counts_documents(client, leave_policy):
    assert client.get("/health").json()["documents"] == 1
