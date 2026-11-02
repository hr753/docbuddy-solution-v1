"""LLM client interface.

`FakeLLM` lets the whole class run the API with no API key and no cost, and makes tests
deterministic. Ticket DOC-105 (stretch) adds a real provider behind the same interface.
"""

import asyncio
import re
from collections.abc import AsyncIterator
from typing import Protocol

from app.rag import Hit, tokenize


class LLMClient(Protocol):
    name: str

    async def complete(self, prompt: str, hits: list[Hit], question: str) -> str: ...

    def stream(self, prompt: str, hits: list[Hit], question: str) -> AsyncIterator[str]: ...


class FakeLLM:
    """Pretends to be an LLM: quotes the most relevant sentence from the best document."""

    name = "fake-llm"

    def __init__(self, delay_seconds: float = 0.05) -> None:
        self.delay_seconds = delay_seconds

    def _answer(self, hits: list[Hit], question: str) -> str:
        if not hits:
            return "I couldn't find anything about that in your documents."
        best = hits[0].doc
        q = tokenize(question)
        sentences = re.split(r"(?<=[.!?])\s+", best.content)
        sentence = max(sentences, key=lambda s: len(q & tokenize(s)))
        return f"According to '{best.title}': {sentence}"

    async def complete(self, prompt: str, hits: list[Hit], question: str) -> str:
        return self._answer(hits, question)

    async def stream(self, prompt: str, hits: list[Hit], question: str) -> AsyncIterator[str]:
        words = self._answer(hits, question).split(" ")
        for i, word in enumerate(words):
            await asyncio.sleep(self.delay_seconds)  # non-blocking, unlike time.sleep
            yield word if i == 0 else " " + word


def build_llm(provider: str, delay_seconds: float) -> LLMClient:
    if provider == "fake":
        return FakeLLM(delay_seconds=delay_seconds)
    raise ValueError(f"Unknown LLM_PROVIDER '{provider}'. See ticket DOC-105.")
