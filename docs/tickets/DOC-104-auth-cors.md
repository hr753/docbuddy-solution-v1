# DOC-104 — API keys and CORS

**Type:** Story · **Points:** 2 · **Sprint:** 8.1

## User story
As the owner of this API, I want only clients with a valid key to use it, and only
our own web UI to call it from a browser, so nobody else can run up our LLM bill.

## Acceptance criteria
- [ ] Every endpoint except `GET /health` requires header `X-API-Key`.
- [ ] Missing or wrong key → 401 `{"detail": "Invalid or missing API key"}`.
- [ ] Valid keys come from env var `API_KEYS` (comma-separated). **No default value in code.**
      The app must refuse to start if `API_KEYS` is not set.
- [ ] Keys compared with `secrets.compare_digest`.
- [ ] CORS allowed origins come from env var `CORS_ORIGINS` (default `http://localhost:8501`).
      Never `"*"`.
- [ ] Keys are never logged or returned in any response.

## Definition of done
- Tests: missing key, wrong key, correct key for each protected route;
  CORS preflight from allowed origin gets the header, unknown origin doesn't.
- `.env.example` documents both variables with fake values.
