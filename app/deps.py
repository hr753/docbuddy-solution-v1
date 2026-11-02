"""Shared dependencies: hand the store, LLM and settings to routes without global variables.

Routes ask for these with type aliases like `store: StoreDep`. Because FastAPI builds them
per request, tests can give every test a fresh app and an empty store.
"""

from typing import Annotated

from fastapi import Depends, Request

from app.config import Settings, get_settings
from app.llm import LLMClient
from app.rag import DocumentStore


def get_store(request: Request) -> DocumentStore:
    return request.app.state.store


def get_llm(request: Request) -> LLMClient:
    return request.app.state.llm


StoreDep = Annotated[DocumentStore, Depends(get_store)]
LLMDep = Annotated[LLMClient, Depends(get_llm)]
SettingsDep = Annotated[Settings, Depends(get_settings)]
