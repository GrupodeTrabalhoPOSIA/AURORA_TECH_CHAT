"""Modelos internos do processamento de documentos."""

from pydantic import BaseModel, Field


class ExtractedSection(BaseModel):
    """Parte textual extraída com sua localização original."""

    content: str
    page: int | None = None


class DocumentChunk(BaseModel):
    """Trecho normalizado pronto para indexação vetorial."""

    id: str
    document_id: str
    document_name: str
    document_type: str
    content: str
    chunk_index: int = Field(ge=0)
    page: int | None = None


class ProcessedDocument(BaseModel):
    """Resultado completo e determinístico do pipeline de ingestão."""

    id: str
    name: str
    document_type: str
    content_hash: str
    chunks: list[DocumentChunk]

