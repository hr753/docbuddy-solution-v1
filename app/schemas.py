"""Every request and response model lives here.

Notice the pattern: every string has min/max length, every number has bounds,
every list has a max length, and unknown fields are rejected (extra="forbid").
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    """Base for request bodies: trims whitespace and rejects unknown fields."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")


# ---------- Health ----------
class HealthOut(BaseModel):
    status: Literal["ok"]
    version: str
    documents: int


# ---------- Documents ----------
class DocumentIn(StrictModel):
    title: str = Field(min_length=1, max_length=200, examples=["Leave policy"])
    content: str = Field(
        min_length=1,
        max_length=20_000,
        description="Plain text of the document",
        examples=["Employees get 24 days of paid leave per year."],
    )


class DocumentOut(BaseModel):
    id: int
    title: str
    chars: int


# ---------- Chat ----------
class ChatMessage(StrictModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=4_000)


class ChatRequest(StrictModel):
    message: str = Field(
        min_length=1,
        max_length=4_000,
        description="The user's question",
        examples=["How many days of paid leave do I get?"],
    )
    top_k: int = Field(default=3, ge=1, le=5, description="How many documents to retrieve")
    history: list[ChatMessage] = Field(default_factory=list, max_length=20)


class Source(BaseModel):
    id: int
    title: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]
    model: str
    latency_ms: int
