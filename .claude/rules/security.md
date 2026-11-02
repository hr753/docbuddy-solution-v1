# Security rules (always loaded)

- Secrets come only from environment variables via `app/config.py`.
  No default value for `API_KEYS` in code — the app must fail to start without it.
- Compare API keys with `secrets.compare_digest`, never with `==`.
- Never log API keys, `Authorization`/`X-API-Key` headers, or full user documents.
  Log ids, lengths, and timings instead.
- CORS origins come from `CORS_ORIGINS` in settings. Never `"*"`, and never `"*"` together
  with `allow_credentials=True`.
- Do not read or write `.env`. If a new variable is needed, add it to `.env.example`
  with a fake placeholder value and mention it in your summary.
