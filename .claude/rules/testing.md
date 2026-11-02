---
paths:
  - "tests/**/*.py"
---

# Testing rules

## What every endpoint needs
For each endpoint, write at least:
1. **Happy path** — valid request returns the right status code AND the right body shape.
2. **Validation** — one test per constraint: empty string, too long, out-of-range number,
   unknown extra field. Each must return 422.
3. **Auth** — missing key → 401, wrong key → 401 (skip only for `GET /health`).
4. **Edge case** — e.g. chat with no documents added yet, `top_k` larger than the number of docs.

## How to write them
- Use the `client` and `auth_headers` fixtures from `tests/conftest.py`.
  Never hardcode a key in a test file.
- One behaviour per test. Name tests `test_<endpoint>_<situation>_<expected>`,
  e.g. `test_chat_empty_message_returns_422`.
- Assert exact status codes: `assert r.status_code == 422`.
  Never `assert r.status_code in (200, 422)` — a test that accepts both outcomes tests nothing.
- Assert on the body, not just the status code.
- Do not mock the thing you are testing. Mock only external services (real LLM APIs).
- Tests must not depend on order or on each other; the store is reset per test.

## Before saying "done"
- Run `pytest -q` and paste the summary line.
- If a test fails, fix the code, not the test — unless the test is wrong, and then say why.
- Never delete or skip a failing test to make the suite green.
