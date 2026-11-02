from html import escape
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

README_PATH = Path(__file__).resolve().parents[2] / "README.md"

router = APIRouter(tags=["root"])


def render_readme_page(readme: str) -> str:
    return (
        "<!doctype html>"
        '<html lang="en">'
        '<head><meta charset="utf-8"><title>DocBuddy</title></head>'
        f'<body><pre style="white-space: pre-wrap">{escape(readme)}</pre></body>'
        "</html>"
    )


# Read once at import so the async handler never does blocking file I/O.
README_PAGE = render_readme_page(README_PATH.read_text(encoding="utf-8"))


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root() -> HTMLResponse:
    """Public: browsers can't send X-API-Key when opening a URL directly."""
    return HTMLResponse(README_PAGE)
