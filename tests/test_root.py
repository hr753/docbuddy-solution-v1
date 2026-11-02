from html import escape

from app.routers.root import README_PATH, render_readme_page


def test_root_no_key_needed_returns_200(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.headers["content-type"] == "text/html; charset=utf-8"


def test_root_returns_readme_content(client):
    title = README_PATH.read_text(encoding="utf-8").splitlines()[0]
    assert escape(title) in client.get("/").text


def test_root_escapes_html():
    page = render_readme_page("<script>alert(1)</script>")
    assert "<script>" not in page
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in page
