"""Contrato inicial do endpoint de chat."""

from fastapi import APIRouter, status

from app.core.errors import AppError
from app.models.chat import ChatRequest, ChatResponse
from app.models.errors import ErrorResponse

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post(
    "",
    response_model=ChatResponse,
    responses={
        422: {"model": ErrorResponse, "description": "Dados de entrada inválidos."},
        501: {"model": ErrorResponse, "description": "RAG ainda não implementado."},
    },
    summary="Enviar uma pergunta ao assistente",
)
async def send_message(_: ChatRequest) -> ChatResponse:
    """Publica o contrato; o comportamento RAG será entregue no Ciclo 09."""
    raise AppError(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        code="CHAT_NOT_IMPLEMENTED",
        message="O chat será habilitado no Ciclo 09.",
    )

