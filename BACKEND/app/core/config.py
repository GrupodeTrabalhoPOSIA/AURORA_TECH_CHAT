"""Configuração tipada da aplicação a partir do ambiente."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações do backend, carregadas de variáveis de ambiente ou `.env`."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "Aurora Tech Chatbot API"
    app_version: str = "0.1.0"
    frontend_origin: str = "http://localhost:5173"
    log_level: str = "INFO"

    openrouter_api_key: SecretStr | None = None
    openrouter_model: str = "openai/gpt-4o-mini"
    openrouter_timeout_seconds: float = Field(default=30.0, gt=0, le=120)

    chroma_persist_directory: Path = Path("data/chroma")
    embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    retrieval_top_k: int = Field(default=5, ge=1, le=20)
    retrieval_min_relevance: float = Field(default=0.35, ge=0, le=1)
    chunk_size: int = Field(default=700, ge=100, le=4000)
    chunk_overlap: int = Field(default=100, ge=0, le=1000)

    max_message_length: int = Field(default=2000, ge=100, le=20000)
    max_history_messages: int = Field(default=10, ge=0, le=50)
    max_upload_size_mb: int = Field(default=10, ge=1, le=100)

    @field_validator("openrouter_api_key", mode="before")
    @classmethod
    def empty_api_key_is_none(cls, value: object) -> object:
        """Trata chave vazia do arquivo de exemplo como ausente."""
        if isinstance(value, str) and not value.strip():
            return None
        return value

    @model_validator(mode="after")
    def validate_chunk_configuration(self) -> "Settings":
        """Garante que a sobreposição seja menor que o trecho."""
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("CHUNK_OVERLAP deve ser menor que CHUNK_SIZE.")
        return self

    def require_openrouter_api_key(self) -> str:
        """Retorna a chave ou falha apenas quando a integração for utilizada."""
        if self.openrouter_api_key is None:
            raise ValueError("OPENROUTER_API_KEY não foi configurada.")
        return self.openrouter_api_key.get_secret_value()


@lru_cache
def get_settings() -> Settings:
    """Retorna uma instância compartilhada e imutável durante a execução."""
    return Settings()

