# DOC-101 — Health check and add-document endpoint

**Type:** Story · **Points:** 2 · **Sprint:** 8.1

## User story
As a client app, I want to check that the API is alive and add text documents to it,
so that later I can ask questions about them.

## Acceptance criteria
- [ ] `GET /health` returns 200 `{"status": "ok", "version": "...", "documents": <count>}`. No API key needed.
- [ ] `POST /documents` with `{"title", "content"}` returns **201** `{"id", "title", "chars"}`.
- [ ] `title`: 1–200 chars. `content`: 1–20,000 chars. Whitespace-only counts as empty.
- [ ] Unknown fields in the body → 422.
- [ ] Documents are kept in memory (a database comes later).
- [ ] Settings (version, etc.) come from `app/config.py`, not hardcoded in routes.

## Definition of done
- Tests for happy path + every validation rule, all passing (`pytest -q`).
- Visible and usable in `/docs` (Swagger UI) with example values.
- PR reviewed against `docs/REVIEW_CHECKLIST.md`.
