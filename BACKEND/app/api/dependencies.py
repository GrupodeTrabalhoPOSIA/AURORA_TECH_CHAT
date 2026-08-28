"""Construção compartilhada das dependências da API."""

from functools import lru_cache

from app.core.config import get_settings
from app.core.errors import AppError
from app.services.documents import DocumentProcessor, DocumentService
from app.services.embeddings import SentenceTransformerEmbeddingService
from app.services.llm import OpenRouterClient
from app.services.rag import ChatService, RetrievalService
from app.services.vector_store import SupabaseVectorStore


@lru_cache
def get_embedding_service() -> SentenceTransformerEmbeddingService:
    settings = get_settings()
    return SentenceTransformerEmbeddingService(settings.embedding_model)


@lru_cache
def get_vector_store() -> SupabaseVectorStore:
    settings = get_settings()
    try:
        url, secret_key = settings.require_supabase_credentials()
    except ValueError as error:
        raise AppError(
            status_code=503,
            code="DATABASE_NOT_CONFIGURED",
            message="O banco Supabase ainda não foi configurado no backend.",
        ) from error
    return SupabaseVectorStore(url, secret_key)


@lru_cache
def get_document_service() -> DocumentService:
    """Cria o serviço real de documentos uma vez por processo."""
    settings = get_settings()
    return DocumentService(
        processor=DocumentProcessor(settings),
        embedding_service=get_embedding_service(),
        vector_store=get_vector_store(),
    )


@lru_cache
def get_chat_service() -> ChatService:
    """Compartilha embeddings e coleção entre ingestão e consulta."""
    settings = get_settings()
    retrieval_service = RetrievalService(
        settings=settings,
        embedding_service=get_embedding_service(),
        vector_store=get_vector_store(),
    )
    return ChatService(
        retrieval_service=retrieval_service,
        llm_client=OpenRouterClient(settings),
    )
