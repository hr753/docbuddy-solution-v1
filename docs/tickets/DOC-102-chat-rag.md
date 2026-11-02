# DOC-102 — Chat endpoint over documents (RAG)

**Type:** Story · **Points:** 3 · **Sprint:** 8.1 · **Depends on:** DOC-101

## User story
As a user, I want to ask a question and get an answer based on my documents,
with the sources shown, so that I can trust where the answer came from.

## Acceptance criteria
- [ ] `POST /chat` body: `message` (1–4,000 chars), `top_k` (1–5, default 3),
      `history` (optional list of `{role: "user"|"assistant", content}`, max 20).
- [ ] Pipeline: **retrieve** top_k documents → **build prompt** with context → **generate** answer.
- [ ] Response: `{"answer", "sources": [{"id","title","score"}], "model", "latency_ms"}`.
- [ ] If no document matches, answer says it couldn't find anything and `sources` is `[]`.
- [ ] Use the existing `FakeLLM` in `app/llm.py` (no API key needed).
- [ ] Route handler stays thin: retrieval in `app/rag.py`, generation in `app/llm.py`.

## Definition of done
- Tests: happy path with sources, no-documents case, top_k > number of docs,
  one 422 test per validation rule (including `role: "system"` rejected).
- `pytest -q` green, reviewed against the checklist.
