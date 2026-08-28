"""Ponto de entrada da API FastAPI."""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router


def create_app() -> FastAPI:
    """Cria e configura a aplicação FastAPI."""
    application = FastAPI(
        title="Aurora Tech Chatbot API",
        description="API acadêmica para o chatbot RAG da Aurora Tech.",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[frontend_origin],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(api_router, prefix="/api/v1")
    return application


app = create_app()

