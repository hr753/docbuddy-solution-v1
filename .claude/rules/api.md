---
paths:
  - "app/**/*.py"
---

# API & validation rules

## Endpoints
- Every route has an explicit `response_model` and a correct `status_code`
  (201 for create, 200 for reads/actions).
- Every route except `GET /health` depends on `require_api_key`.
- Route handlers stay thin: validate input, call a function in `app/rag.py` or
  `app/llm.py`, return a model. No business logic in `main.py`.
- Use `async def` handlers. Never call blocking functions (`time.sleep`,
  sync HTTP clients) inside them; use `await asyncio.sleep` / async clients.

## Request validation (Pydantic v2)
- All request bodies are Pydantic models in `app/schemas.py`. Never accept a raw `dict`.
- Every `str` field has `min_length` and `max_length`. Unbounded text = unbounded LLM cost.
- Every numeric field has `ge` / `le` bounds.
- Every list field has `max_length`.
- Strip whitespace on user text (`str_strip_whitespace=True` in `model_config`),
  so `"   "` is rejected as empty.
- Use `extra="forbid"` so unknown fields return 422 instead of being silently ignored.
- Add a `Field(description=..., examples=[...])` so `/docs` is self-explaining.

## Responses & errors
- Invalid input → let FastAPI return 422. Do not catch and convert it to 200.
- Missing or wrong API key → 401 with `{"detail": "Invalid or missing API key"}`.
- Never return stack traces or internal exception text to the client.

## Streaming
- Streaming endpoints return `StreamingResponse` with `media_type="text/event-stream"`.
- Each token is sent as `data: {"token": "..."}\n\n` the moment it is produced —
  never build the full answer first and send it at the end.
- Finish with `event: done` followed by a JSON summary line.
