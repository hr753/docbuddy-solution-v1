import json
import time
from collections.abc import AsyncIterator

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.deps import LLMDep, StoreDep
from app.rag import build_prompt
from app.schemas import ChatRequest, ChatResponse, Source
from app.security import require_api_key

router = APIRouter(prefix="/chat", tags=["chat"], dependencies=[Depends(require_api_key)])


@router.post("", response_model=ChatResponse)
async def chat(
    body: ChatRequest,
    store: StoreDep,
    llm: LLMDep,
) -> ChatResponse:
    started = time.perf_counter()
    hits = store.search(body.message, k=body.top_k)  # 1. Retrieve
    prompt = build_prompt(body.message, hits, body.history)  # 2. Augment
    answer = await llm.complete(prompt, hits, body.message)  # 3. Generate
    return ChatResponse(
        answer=answer,
        sources=[Source(id=h.doc.id, title=h.doc.title, score=h.score) for h in hits],
        model=llm.name,
        latency_ms=int((time.perf_counter() - started) * 1000),
    )


def sse(data: dict, event: str | None = None) -> str:
    """Format one Server-Sent Event. The blank line at the end is required."""
    prefix = f"event: {event}\n" if event else ""
    return f"{prefix}data: {json.dumps(data)}\n\n"


@router.post("/stream")
async def chat_stream(
    body: ChatRequest,
    store: StoreDep,
    llm: LLMDep,
) -> StreamingResponse:
    hits = store.search(body.message, k=body.top_k)
    prompt = build_prompt(body.message, hits, body.history)

    async def events() -> AsyncIterator[str]:
        started = time.perf_counter()
        async for token in llm.stream(prompt, hits, body.message):
            yield sse({"token": token})  # send each token as soon as it exists
        yield sse(
            {
                "sources": [{"id": h.doc.id, "title": h.doc.title, "score": h.score} for h in hits],
                "model": llm.name,
                "latency_ms": int((time.perf_counter() - started) * 1000),
            },
            event="done",
        )

    return StreamingResponse(events(), media_type="text/event-stream")
