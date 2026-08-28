"""Testes dos contratos iniciais do chat."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_chat_rejects_blank_message_with_standard_error() -> None:
    response = client.post("/api/v1/chat", json={"message": "   ", "history": []})

    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "VALIDATION_ERROR"


def test_chat_rejects_message_above_limit() -> None:
    response = client.post("/api/v1/chat", json={"message": "a" * 2001, "history": []})

    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "VALIDATION_ERROR"


def test_chat_rejects_history_above_limit() -> None:
    history = [{"role": "user", "content": f"Mensagem {index}"} for index in range(11)]

    response = client.post("/api/v1/chat", json={"message": "Pergunta", "history": history})

    assert response.status_code == 422


def test_valid_chat_contract_is_published_but_not_implemented() -> None:
    response = client.post("/api/v1/chat", json={"message": "Pergunta", "history": []})

    assert response.status_code == 501
    assert response.json() == {
        "detail": {
            "code": "CHAT_NOT_IMPLEMENTED",
            "message": "O chat será habilitado no Ciclo 09.",
        }
    }


def test_chat_contract_is_available_in_openapi() -> None:
    openapi = client.get("/openapi.json").json()

    assert "/api/v1/chat" in openapi["paths"]
    assert "ChatRequest" in openapi["components"]["schemas"]
    assert "ChatResponse" in openapi["components"]["schemas"]

