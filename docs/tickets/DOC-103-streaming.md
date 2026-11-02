# DOC-103 — Streaming chat (token by token)

**Type:** Story · **Points:** 3 · **Sprint:** 8.1 · **Depends on:** DOC-102

## User story
As a user, I want to see the answer appear word by word,
so the app feels fast even when the full answer takes several seconds.

## Acceptance criteria
- [ ] `POST /chat/stream` accepts the same body as `/chat` (same validation).
- [ ] Returns `text/event-stream` (Server-Sent Events).
- [ ] Each token is sent as `data: {"token": "..."}` **as soon as it is produced**.
- [ ] Ends with `event: done` and `data: {"sources": [...], "model": "...", "latency_ms": ...}`.
- [ ] No blocking calls inside the async generator (`time.sleep` is not allowed).

## How to check it by hand
```bash
curl -N -X POST http://127.0.0.1:8000/chat/stream \
  -H "X-API-Key: $API_KEY" -H "Content-Type: application/json" \
  -d '{"message": "how many paid leave days?"}'
```
Words should appear one at a time, not all at once.

## Definition of done
- Test parses the SSE stream and checks: many tokens, joined text correct, last event is `done`.
- `pytest -q` green, reviewed against the checklist.
