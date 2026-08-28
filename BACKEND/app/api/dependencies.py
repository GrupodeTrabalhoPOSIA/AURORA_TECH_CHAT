"""Construção compartilhada das dependências da API."""

from functools import lru_cache

from app.core.config import get_settings
from app.services.documents import DocumentProcessor, DocumentService
from app.services.embeddings import SentenceTransformerEmbeddingService
from app.services.vector_store import ChromaVectorStore


@lru_cache
def get_document_service() -> DocumentService:
    """Cria o serviço real de documentos uma vez por processo."""
    settings = get_settings()
    return DocumentService(
        processor=DocumentProcessor(settings),
        embedding_service=SentenceTransformerEmbeddingService(settings.embedding_model),
        vector_store=ChromaVectorStore(settings.chroma_persist_directory),
    )

