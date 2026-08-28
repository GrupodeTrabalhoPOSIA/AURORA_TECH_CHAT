"""Armazenamento de documentos e embeddings no Supabase com pgvector."""

from datetime import datetime
from typing import Any

from postgrest import APIError
from supabase import Client, create_client

from app.core.errors import AppError
from app.models.documents import DocumentResponse, ProcessedDocument
from app.models.rag import RetrievedChunk

DOCUMENTS_TABLE = "aurora_documents"
INDEX_FUNCTION = "index_aurora_document"
MATCH_FUNCTION = "match_aurora_chunks"


class SupabaseVectorStore:
    """Acessa o banco remoto somente com credenciais do backend."""

    def __init__(
        self,
        url: str,
        secret_key: str,
        *,
        client: Client | Any | None = None,
    ) -> None:
        self.client = client or create_client(url, secret_key)

    def add_document(
        self,
        document: ProcessedDocument,
        embeddings: list[list[float]],
    ) -> DocumentResponse:
        if len(embeddings) != len(document.chunks):
            raise ValueError("Cada chunk deve possuir exatamente um embedding.")

        chunks = [
            {
                "id": chunk.id,
                "content": chunk.content,
                "chunk_index": chunk.chunk_index,
                "page": chunk.page,
                "embedding": embedding,
            }
            for chunk, embedding in zip(document.chunks, embeddings, strict=True)
        ]
        try:
            response = self.client.rpc(
                INDEX_FUNCTION,
                {
                    "p_id": document.id,
                    "p_name": document.name,
                    "p_document_type": document.document_type,
                    "p_content_hash": document.content_hash,
                    "p_file_size": document.file_size,
                    "p_chunks": chunks,
                },
            ).execute()
        except APIError as error:
            if str(getattr(error, "code", "")) == "23505":
                raise AppError(
                    status_code=409,
                    code="DUPLICATE_DOCUMENT",
                    message="Este documento já existe na base de conhecimento.",
                ) from error
            raise self._database_error() from error

        rows = response.data or []
        if not rows:
            raise self._database_error()
        return self._document_from_row(rows[0])

    def list_documents(self) -> list[DocumentResponse]:
        try:
            response = (
                self.client.table(DOCUMENTS_TABLE)
                .select("id,name,document_type,chunk_count,file_size,created_at")
                .order("created_at", desc=True)
                .execute()
            )
        except APIError as error:
            raise self._database_error() from error
        return [self._document_from_row(row) for row in response.data or []]

    def known_hashes(self) -> set[str]:
        try:
            response = self.client.table(DOCUMENTS_TABLE).select("content_hash").execute()
        except APIError as error:
            raise self._database_error() from error
        return {
            str(row["content_hash"])
            for row in response.data or []
            if row.get("content_hash")
        }

    def document_exists(self, document_id: str) -> bool:
        try:
            response = (
                self.client.table(DOCUMENTS_TABLE)
                .select("id")
                .eq("id", document_id)
                .limit(1)
                .execute()
            )
        except APIError as error:
            raise self._database_error() from error
        return bool(response.data)

    def delete_document(self, document_id: str) -> None:
        if not self.document_exists(document_id):
            raise AppError(
                status_code=404,
                code="DOCUMENT_NOT_FOUND",
                message="Documento não encontrado.",
            )
        try:
            self.client.table(DOCUMENTS_TABLE).delete().eq("id", document_id).execute()
        except APIError as error:
            raise self._database_error() from error

    def search(
        self,
        embedding: list[float],
        limit: int,
        min_relevance: float,
    ) -> list[RetrievedChunk]:
        try:
            response = self.client.rpc(
                MATCH_FUNCTION,
                {
                    "query_embedding": embedding,
                    "match_count": limit,
                    "match_threshold": min_relevance,
                },
            ).execute()
        except APIError as error:
            raise self._database_error() from error

        return [
            RetrievedChunk(
                document_id=str(row["document_id"]),
                document_name=str(row["document_name"]),
                content=str(row["content"]),
                chunk_index=int(row["chunk_index"]),
                page=int(row["page"]) if row.get("page") is not None else None,
                relevance=max(0.0, min(1.0, float(row["similarity"]))),
            )
            for row in response.data or []
        ]

    @staticmethod
    def _document_from_row(row: dict[str, Any]) -> DocumentResponse:
        return DocumentResponse(
            id=str(row["id"]),
            name=str(row["name"]),
            document_type=str(row["document_type"]),
            chunk_count=int(row["chunk_count"]),
            file_size=int(row["file_size"]),
            created_at=datetime.fromisoformat(str(row["created_at"]).replace("Z", "+00:00")),
        )

    @staticmethod
    def _database_error() -> AppError:
        return AppError(
            status_code=503,
            code="DATABASE_UNAVAILABLE",
            message="A base de conhecimento está temporariamente indisponível.",
        )
