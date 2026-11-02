"""App factory: wires settings, middleware and routers together. No business logic here."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.llm import build_llm
from app.rag import DocumentStore
from app.routers import chat, documents, health


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version=settings.version)

    app.state.store = DocumentStore()
    app.state.llm = build_llm(settings.llm_provider, settings.stream_delay_seconds)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,  # explicit list, never "*"
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type", "X-API-Key"],
    )

    app.include_router(health.router)
    app.include_router(documents.router)
    app.include_router(chat.router)
    return app


app = create_app()
