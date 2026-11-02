"""A deliberately tiny RAG pipeline: an in-memory store + keyword-overlap retrieval.

Real projects swap this for embeddings + a vector database. The *endpoints don't change*
when you do — that is the point of keeping retrieval behind a small interface.
"""

import re
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Protocol

_WORD = re.compile(r"[a-z0-9]+")
_STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "of", "to", "in", "on", "for", "and", "or",
    "do", "does", "i", "my", "me", "how", "what", "many", "much", "get", "can", "you",
}  # fmt: skip


def tokenize(text: str) -> set[str]:
    return {w for w in _WORD.findall(text.lower()) if w not in _STOPWORDS}


class Turn(Protocol):
    """Anything with a role and content, e.g. the ChatMessage schema."""

    role: str
    content: str


@dataclass
class Document:
    id: int
    title: str
    content: str


@dataclass
class Hit:
    doc: Document
    score: float


@dataclass
class DocumentStore:
    _docs: dict[int, Document] = field(default_factory=dict)
    _next_id: int = 1

    def add(self, title: str, content: str) -> Document:
        doc = Document(id=self._next_id, title=title, content=content)
        self._docs[doc.id] = doc
        self._next_id += 1
        return doc

    def count(self) -> int:
        return len(self._docs)

    def search(self, query: str, k: int) -> list[Hit]:
        q = tokenize(query)
        if not q:
            return []
        hits = []
        for doc in self._docs.values():
            overlap = q & tokenize(doc.title + " " + doc.content)
            if overlap:
                hits.append(Hit(doc=doc, score=round(len(overlap) / len(q), 3)))
        hits.sort(key=lambda h: h.score, reverse=True)
        return hits[:k]


def build_prompt(question: str, hits: list[Hit], history: Sequence[Turn]) -> str:
    context = "\n\n".join(f"[{h.doc.id}] {h.doc.title}\n{h.doc.content}" for h in hits)
    past = "\n".join(f"{m.role}: {m.content}" for m in history)
    return (
        "Answer the question using ONLY the context below. "
        "If the answer is not in the context, say you don't know.\n\n"
        f"Context:\n{context or '(no documents found)'}\n\n"
        f"Conversation so far:\n{past or '(none)'}\n\n"
        f"Question: {question}"
    )
