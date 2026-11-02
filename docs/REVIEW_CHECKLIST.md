# Manual review checklist (use on every PR, human or agent)

The agent wrote the code. **You** are responsible for it. Go through every item;
write the item number next to anything you flag in your PR comment.

## 1. Scope — did it build what the ticket asked?
- [ ] 1.1 Every acceptance criterion is met (tick them off in the ticket).
- [ ] 1.2 Nothing extra was added that the ticket didn't ask for (new endpoints, new dependencies, "helpful" refactors).
- [ ] 1.3 No files changed that have nothing to do with the ticket.

## 2. Read the diff, line by line
- [ ] 2.1 Can you explain what every changed line does? If not, ask the agent *and* verify the answer.
- [ ] 2.2 Every import, function, and parameter actually exists in the library version we use (agents invent APIs).
- [ ] 2.3 No leftover debug prints, commented-out code, or TODOs without a ticket.

## 3. Validation (Pydantic)
- [ ] 3.1 Every `str` has `min_length` and `max_length`.
- [ ] 3.2 Every number has `ge`/`le`; every list has `max_length`.
- [ ] 3.3 `extra="forbid"` and whitespace stripping are on for request models.
- [ ] 3.4 Request bodies are models, not raw `dict`.

## 4. Security
- [ ] 4.1 No secrets, keys, or "default keys" in code, tests, or committed files.
- [ ] 4.2 Protected routes depend on `require_api_key`; only `/health` is public.
- [ ] 4.3 Keys compared with `secrets.compare_digest`, not `==`.
- [ ] 4.4 Nothing logs keys, auth headers, or full documents.
- [ ] 4.5 CORS origins come from settings; no `"*"`.

## 5. Async & streaming
- [ ] 5.1 No `time.sleep` or blocking I/O inside `async def`.
- [ ] 5.2 Streaming really streams: tokens are yielded as produced, not collected first.
- [ ] 5.3 Check by hand with `curl -N` — do words appear one at a time?

## 6. Tests — do they prove anything?
- [ ] 6.1 Happy path, validation, auth, and an edge case exist for each endpoint.
- [ ] 6.2 Assertions are exact (`== 422`), never `in (200, 422)`.
- [ ] 6.3 Tests check the response **body**, not only the status code.
- [ ] 6.4 Nothing under test is mocked away.
- [ ] 6.5 **Break-it test:** comment out one line of the feature. Does at least one test fail? If not, the tests are too weak.
- [ ] 6.6 You ran `pytest -q` yourself and saw it pass. (Don't trust "all tests pass" in the agent's message.)

## 7. Run it yourself
- [ ] 7.1 `uvicorn app.main:app --reload` starts with your `.env`.
- [ ] 7.2 Try the endpoint in `/docs` with a good request and a bad one.
- [ ] 7.3 Remove `API_KEYS` from your env — does the app refuse to start?

## PR comment template
```
Ticket: DOC-___
Verdict: Approve / Request changes
Checked: all items / items skipped: ___
Issues found (item no. → what → suggested fix):
-
What I asked the agent to change, and how I verified the fix:
-
```
