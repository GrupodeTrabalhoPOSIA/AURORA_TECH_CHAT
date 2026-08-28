"""Testes do adaptador Supabase sem acessar a rede."""

from types import SimpleNamespace
from unittest.mock import Mock

from postgrest import APIError
import pytest

from app.core.config import Settings
from app.core.errors import AppError
from app.services.documents import DocumentProcessor
from app.services.vector_store import SupabaseVectorStore
from tests.fakes import FakeEmbeddingService


def make_document():
    settings = Settings(_env_file=None)
    return DocumentProcessor(settings).process(
        filename="aurora.txt",
        content=b"A Aurora Tech oferece solucoes digitais.",
        content_type="text/plain",
    )


def test_indexes_document_atomically_through_rpc() -> None:
    document = make_document()
    embeddings = FakeEmbeddingService().embed_documents(
        [chunk.content for chunk in document.chunks]
    )
    client = Mock()
    client.rpc.return_value.execute.return_value = SimpleNamespace(
        data=[
            {
                "id": document.id,
                "name": document.name,
                "document_type": document.document_type,
                "chunk_count": 1,
                "file_size": document.file_size,
                "created_at": "2026-08-28T12:00:00Z",
            }
        ]
    )
    store = SupabaseVectorStore("https://project.supabase.co", "secret", client=client)

    indexed = store.add_document(document, embeddings)

    function_name, payload = client.rpc.call_args.args
    assert function_name == "index_aurora_document"
    assert payload["p_content_hash"] == document.content_hash
    assert payload["p_chunks"][0]["embedding"] == embeddings[0]
    assert indexed.id == document.id
    assert indexed.chunk_count == 1


def test_search_passes_threshold_to_pgvector_and_maps_source() -> None:
    client = Mock()
    client.rpc.return_value.execute.return_value = SimpleNamespace(
        data=[
            {
                "document_id": "5d5d6b09-9444-4cf6-b3da-b3e663983dfa",
                "document_name": "servicos.txt",
                "content": "Consultoria em transformação digital.",
                "chunk_index": 0,
                "page": None,
                "similarity": 0.87,
            }
        ]
    )
    store = SupabaseVectorStore("https://project.supabase.co", "secret", client=client)

    chunks = store.search([0.1, 0.2, 0.3], limit=5, min_relevance=0.35)

    function_name, payload = client.rpc.call_args.args
    assert function_name == "match_aurora_chunks"
    assert payload["match_count"] == 5
    assert payload["match_threshold"] == 0.35
    assert chunks[0].document_name == "servicos.txt"
    assert chunks[0].relevance == 0.87


def test_lists_documents_from_supabase() -> None:
    client = Mock()
    query = client.table.return_value.select.return_value.order.return_value
    query.execute.return_value = SimpleNamespace(
        data=[
            {
                "id": "5d5d6b09-9444-4cf6-b3da-b3e663983dfa",
                "name": "empresa.md",
                "document_type": "md",
                "chunk_count": 2,
                "file_size": 321,
                "created_at": "2026-08-28T12:00:00+00:00",
            }
        ]
    )
    store = SupabaseVectorStore("https://project.supabase.co", "secret", client=client)

    documents = store.list_documents()

    client.table.assert_called_once_with("aurora_documents")
    assert documents[0].name == "empresa.md"
    assert documents[0].chunk_count == 2


def test_duplicate_constraint_is_exposed_as_domain_error() -> None:
    document = make_document()
    embeddings = FakeEmbeddingService().embed_documents(
        [chunk.content for chunk in document.chunks]
    )
    client = Mock()
    client.rpc.return_value.execute.side_effect = APIError(
        {"message": "duplicate", "code": "23505", "hint": None, "details": None}
    )
    store = SupabaseVectorStore("https://project.supabase.co", "secret", client=client)

    with pytest.raises(AppError) as captured:
        store.add_document(document, embeddings)

    assert captured.value.status_code == 409
    assert captured.value.code == "DUPLICATE_DOCUMENT"
