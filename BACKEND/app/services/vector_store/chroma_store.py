"""Repositório vetorial persistente baseado em ChromaDB."""

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import chromadb

from app.core.errors import AppError
from app.models.documents import DocumentResponse, ProcessedDocument

COLLECTION_NAME = "aurora_tech_documents"


class ChromaVectorStore:
    """Armazena chunks e usa seus metadados como catálogo de documentos."""

    def __init__(self, persist_directory: Path) -> None:
        persist_directory.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=str(persist_directory))
        self.collection = self.client.get_or_create_collection(name=COLLECTION_NAME)

    def add_document(
        self,
        document: ProcessedDocument,
        embeddings: list[list[float]],
    ) -> DocumentResponse:
        if len(embeddings) != len(document.chunks):
            raise ValueError("Cada chunk deve possuir exatamente um embedding.")

        created_at = datetime.now(UTC)
        metadatas: list[dict[str, str | int | float | bool]] = []
        for chunk in document.chunks:
            metadata: dict[str, str | int | float | bool] = {
                "document_id": document.id,
                "document_name": document.name,
                "document_type": document.document_type,
                "content_hash": document.content_hash,
                "file_size": document.file_size,
                "chunk_index": chunk.chunk_index,
                "created_at": created_at.isoformat(),
            }
            if chunk.page is not None:
                metadata["page"] = chunk.page
            metadatas.append(metadata)

        self.collection.add(
            ids=[chunk.id for chunk in document.chunks],
            embeddings=embeddings,
            documents=[chunk.content for chunk in document.chunks],
            metadatas=metadatas,
        )
        return DocumentResponse(
            id=document.id,
            name=document.name,
            document_type=document.document_type,
            chunk_count=len(document.chunks),
            file_size=document.file_size,
            created_at=created_at,
        )

    def list_documents(self) -> list[DocumentResponse]:
        result = self.collection.get(include=["metadatas"])
        metadatas = result.get("metadatas") or []
        grouped: dict[str, dict[str, Any]] = {}
        for metadata in metadatas:
            if metadata is None:
                continue
            document_id = str(metadata["document_id"])
            if document_id not in grouped:
                grouped[document_id] = {**metadata, "chunk_count": 0}
            grouped[document_id]["chunk_count"] += 1

        documents = [
            DocumentResponse(
                id=document_id,
                name=str(metadata["document_name"]),
                document_type=str(metadata["document_type"]),
                chunk_count=int(metadata["chunk_count"]),
                file_size=int(metadata["file_size"]),
                created_at=datetime.fromisoformat(str(metadata["created_at"])),
            )
            for document_id, metadata in grouped.items()
        ]
        return sorted(documents, key=lambda item: item.created_at, reverse=True)

    def known_hashes(self) -> set[str]:
        result = self.collection.get(include=["metadatas"])
        return {
            str(metadata["content_hash"])
            for metadata in result.get("metadatas") or []
            if metadata and "content_hash" in metadata
        }

    def document_exists(self, document_id: str) -> bool:
        result = self.collection.get(where={"document_id": document_id}, limit=1)
        return bool(result["ids"])

    def delete_document(self, document_id: str) -> None:
        if not self.document_exists(document_id):
            raise AppError(
                status_code=404,
                code="DOCUMENT_NOT_FOUND",
                message="Documento não encontrado.",
            )
        self.collection.delete(where={"document_id": document_id})

