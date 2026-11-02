# DOC-105 (stretch) — Plug in a real LLM provider

**Type:** Story · **Points:** 3 · **Sprint:** 8.1 stretch / homework

## User story
As a developer, I want to switch from `FakeLLM` to a real model by changing one
environment variable, without touching any route code.

## Acceptance criteria
- [ ] New class in `app/llm.py` implementing the same `LLMClient` interface
      (`complete` and `stream`) for one provider of your choice.
- [ ] Selected with `LLM_PROVIDER=<name>`; the provider's key comes from its own env var.
- [ ] `stream()` uses the provider's real streaming API (not "get the full answer, then split it").
- [ ] Routes in `app/routers/` are **unchanged**.
- [ ] Tests still run with `FakeLLM` and no network. Add one test for `build_llm`
      choosing the right class.

## Review focus
- Did the agent invent SDK parameters? Check every call against the provider's official docs.
- Is the key read from settings, never hardcoded or logged?
