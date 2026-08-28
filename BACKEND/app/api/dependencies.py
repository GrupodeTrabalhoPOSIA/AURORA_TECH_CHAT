"""Construção compartilhada das dependências da API."""

from functools import lru_cache

from app.core.config import get_settings
from app.services.documents import DocumentProcessor, DocumentService
from app.services.embeddings import SentenceTransformerEmbeddingService
from app.services.llm import OpenRouterClient
from app.services.rag import ChatService, RetrievalService
from app.services.vector_store import ChromaVectorStore


@lru_cache
def get_embedding_service() -> SentenceTransformerEmbeddingService:
    settings = get_settings()
    return SentenceTransformerEmbeddingService(settings.embedding_model)


@lru_cache
def get_vector_store() -> ChromaVectorStore:
    settings = get_settings()
    return ChromaVectorStore(settings.chroma_persist_directory)


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
