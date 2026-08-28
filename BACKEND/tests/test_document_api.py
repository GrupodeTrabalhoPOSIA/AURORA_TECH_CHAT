"""Testes integrados dos endpoints e da persistência vetorial."""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_document_service
from app.core.config import Settings
from app.main import app
from app.services.documents import DocumentProcessor, DocumentService
from app.services.vector_store import ChromaVectorStore
from tests.fakes import FakeEmbeddingService


def make_service(path: Path) -> DocumentService:
    settings = Settings(_env_file=None, chroma_persist_directory=path)
    return DocumentService(
        processor=DocumentProcessor(settings),
        embedding_service=FakeEmbeddingService(),
        vector_store=ChromaVectorStore(path),
    )


@pytest.fixture
def client(tmp_path: Path) -> TestClient:
    service = make_service(tmp_path / "chroma")
    app.dependency_overrides[get_document_service] = lambda: service
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_document_lifecycle(client: TestClient) -> None:
    upload = client.post(
        "/api/v1/documents",
        files={"file": ("aurora.txt", b"Aurora Tech oferece solucoes digitais.", "text/plain")},
    )

    assert upload.status_code == 201
    document = upload.json()
    assert document["name"] == "aurora.txt"
    assert document["chunk_count"] == 1

    listed = client.get("/api/v1/documents")
    assert listed.status_code == 200
    assert listed.json() == [document]

    duplicate = client.post(
        "/api/v1/documents",
        files={"file": ("copia.txt", b"Aurora Tech oferece solucoes digitais.", "text/plain")},
    )
    assert duplicate.status_code == 409
    assert duplicate.json()["detail"]["code"] == "DUPLICATE_DOCUMENT"

    deleted = client.delete(f"/api/v1/documents/{document['id']}")
    assert deleted.status_code == 204
    assert client.get("/api/v1/documents").json() == []


def test_delete_unknown_document_returns_404(client: TestClient) -> None:
    response = client.delete("/api/v1/documents/inexistente")

    assert response.status_code == 404
    assert response.json()["detail"]["code"] == "DOCUMENT_NOT_FOUND"


def test_vectors_persist_after_store_is_reopened(tmp_path: Path) -> None:
    persist_directory = tmp_path / "persistent-chroma"
    service = make_service(persist_directory)
    indexed = service.index_document(
        filename="aurora.md",
        content=b"# Aurora Tech\n\nConhecimento persistente.",
        content_type="text/markdown",
    )

    reopened = make_service(persist_directory)
    documents = reopened.list_documents()

    assert len(documents) == 1
    assert documents[0].id == indexed.id
    assert reopened.vector_store.collection.count() == indexed.chunk_count

