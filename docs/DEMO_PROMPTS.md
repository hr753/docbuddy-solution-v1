# Live demo — prompts to type into Claude Code (session 8.1)

Run from the `docbuddy-starter` folder. Each step = one ticket = one branch = one commit.
After every step: **stop, read the diff with the class, run the checklist.**

---

## Step 0 — Show the agent what it knows about the project
```
claude
/context
```
Point at **Memory files**: `CLAUDE.md` and the rules in `.claude/rules/` are loaded.
Then ask:
```
In 5 bullet points, what are the rules you must follow in this project?
```
> Teaching point: if it can't repeat the rules, the rules are too vague or too long.

---

## Step 1 — DOC-101 (plan first, then build)
```
git checkout -b DOC-101
```
Switch to **plan mode** (Shift+Tab until it says plan mode), then:
```
Read docs/tickets/DOC-101-health-and-documents.md.
Make a plan: which files you will create, the Pydantic models with every field
constraint, the endpoints, and the list of tests. Don't write code yet.
```
**Critique the plan out loud with the class.** Typical things to push back on:
- "Where is the max_length on content?"
- "You listed only a happy-path test. What about whitespace-only titles?"

Then approve and let it implement. When it says it's done:
```
Run pytest -q and show me the output.
```
Review with `git diff` → checklist sections 1–3 and 6 → commit.

---

## Step 2 — DOC-102 (RAG chat)
```
git checkout -b DOC-102
Read docs/tickets/DOC-102-chat-rag.md and plan it. Keep retrieval in app/rag.py
and generation in app/llm.py; the route must stay thin.
```
Review focus: is the handler thin? Is `role: "system"` rejected? Is there a no-documents test?

---

## Step 3 — DOC-103 (streaming)
```
git checkout -b DOC-103
Read docs/tickets/DOC-103-streaming.md and plan it. Explain how you'll make sure
tokens are sent as they're produced and not after the whole answer is ready.
```
After it builds, **prove it by hand** in a second terminal:
```
uvicorn app.main:app --reload
curl -N -X POST http://127.0.0.1:8000/chat/stream -H "X-API-Key: <your key>" \
  -H "Content-Type: application/json" -d '{"message":"how many paid leave days?"}'
```

---

## Step 4 — DOC-104 (auth + CORS)
```
git checkout -b DOC-104
Read docs/tickets/DOC-104-auth-cors.md and plan it.
```
Live security checks with the class:
- `grep -rn "dev-key\|test-key\|API_KEYS =" app/` → should find nothing hardcoded.
- Ask Claude: `Read the .env file` → the deny rule in `.claude/settings.json` blocks it. Show the class.
- Remove `API_KEYS` from `.env` and restart → app must refuse to start.

---

## Step 5 — Teach the "break-it" test
```
Comment out the line in app/security.py that rejects a wrong key, run pytest,
and tell me which tests fail.
```
If **no** test fails, the tests were weak. Restore the line afterwards.

---

## Step 6 — When the agent gets something wrong (it will)
Use these instead of "fix it":
- `The ticket says X, your code does Y at app/routers/chat.py line 30. Change it to match the ticket.`
- `This test accepts both 200 and 422, so it can never fail. Rewrite it to assert exactly 422.`
- `Add this to CLAUDE.md so you don't repeat it: <rule>.` ← this is how CLAUDE.md grows.
