# DocBuddy — Module 8.1: FastAPI for LLM & RAG apps

A small API that answers questions about your documents. You'll build it with
Claude Code, one ticket at a time, and review every change yourself.

## Setup (once)
```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # then put your own random key in API_KEYS
git init && git add . && git commit -m "Starter"
```

## Run
```bash
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/docs, click **Authorize**, paste your key, and try the endpoints.

## Test
```bash
pytest -q
```

## How we work
1. Pick the next ticket in `docs/tickets/` (DOC-101 → DOC-104, DOC-105 is stretch).
2. `git checkout -b DOC-10x`
3. Ask Claude Code to **plan** first. Critique the plan. Then let it build.
4. Review the diff with `docs/REVIEW_CHECKLIST.md`. Run tests **yourself**.
5. Commit, open a PR, paste the checklist comment.

## What's in here
| Path | What it is |
|---|---|
| `CLAUDE.md` | Project instructions Claude Code reads at the start of every session |
| `.claude/rules/` | Focused rules: API & validation, testing, security |
| `.claude/settings.json` | Blocks the agent from reading `.env`; auto-formats code after every edit |
| `docs/tickets/` | What to build, with acceptance criteria |
| `docs/REVIEW_CHECKLIST.md` | How to review a PR — the most important file here |
| `docs/DEMO_PROMPTS.md` | The prompts used in the live demo |

The LLM is a `FakeLLM`: no API key, no cost, predictable output. A real model comes in DOC-105.
