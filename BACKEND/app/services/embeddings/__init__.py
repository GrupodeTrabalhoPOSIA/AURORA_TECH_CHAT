"""Serviços de geração de embeddings."""

from app.services.embeddings.base import EmbeddingService
from app.services.embeddings.sentence_transformer import SentenceTransformerEmbeddingService

__all__ = ["EmbeddingService", "SentenceTransformerEmbeddingService"]

