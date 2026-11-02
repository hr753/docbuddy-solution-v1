# DocBuddy — project instructions for Claude Code

DocBuddy is a teaching project: a small FastAPI backend that answers questions
about documents a user has added (a tiny RAG pipeline). It is built one Jira-style
ticket at a time. Tickets live in `docs/tickets/`.

## Stack
- Python 3.11+, FastAPI, Pydantic v2, pydantic-settings
- Tests: pytest + FastAPI `TestClient`
- Lint/format: ruff (a hook runs it after every edit)

## Commands
- Install: `pip install -r requirements.txt`
- Run the API: `uvicorn app.main:app --reload` then open http://127.0.0.1:8000/docs
- Run tests: `pytest -q`
- Lint: `ruff check . && ruff format --check .`

## Project layout
- `app/main.py` — creates the FastAPI app, middleware, includes routers. No business logic here.
- `app/config.py` — all settings, read from environment / `.env` via pydantic-settings.
- `app/schemas.py` — every Pydantic request/response model.
- `app/security.py` — API-key dependency.
- `app/llm.py` — LLM client interface + `FakeLLM` (no API key needed in class).
- `app/rag.py` — in-memory document store and retrieval.
- `app/routers/` — one file per area (`health.py`, `documents.py`, `chat.py`).
- `tests/` — mirrors `app/` (e.g. `tests/test_chat.py`).

## How we work (follow this every time)
1. Read the ticket in `docs/tickets/` first. Only build what the ticket asks for.
2. Before writing code, show a short plan: files you will touch, models, endpoints, tests.
   Wait for approval.
3. Write or update tests in the same change as the code.
4. Run `pytest -q` and show the result before saying a task is done.
5. Keep changes small: one ticket per branch, one logical change per commit.
6. If something in the ticket is unclear, ask. Do not guess requirements.

## Hard rules
- Never read, print, or create `.env`. Use `.env.example` for documenting variables.
- Never hardcode API keys, secrets, or default keys in code or tests.
- Never use `allow_origins=["*"]` in CORS.
- Do not add new dependencies without asking first.
- Detailed rules: see `.claude/rules/` (API, testing, security).
