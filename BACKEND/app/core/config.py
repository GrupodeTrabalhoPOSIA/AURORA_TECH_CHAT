"""Configuração tipada da aplicação a partir do ambiente."""

from functools import lru_cache
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
    openrouter_max_tokens: int = Field(default=500, ge=50, le=4000)
    openrouter_temperature: float = Field(default=0.1, ge=0, le=2)
    openrouter_referer: str = "http://localhost:5173"
    openrouter_app_title: str = "Aurora Tech Chatbot"

    supabase_url: str | None = None
    supabase_secret_key: SecretStr | None = None
    supabase_service_role_key: SecretStr | None = None
    embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    retrieval_top_k: int = Field(default=5, ge=1, le=20)
    retrieval_min_relevance: float = Field(default=0.35, ge=0, le=1)
    max_context_characters: int = Field(default=6000, ge=500, le=30000)
    chunk_size: int = Field(default=700, ge=100, le=4000)
    chunk_overlap: int = Field(default=100, ge=0, le=1000)

    max_message_length: int = Field(default=2000, ge=100, le=20000)
    max_history_messages: int = Field(default=10, ge=0, le=50)
    max_upload_size_mb: int = Field(default=10, ge=1, le=100)

    @field_validator(
        "openrouter_api_key",
        "supabase_url",
        "supabase_secret_key",
        "supabase_service_role_key",
        mode="before",
    )
    @classmethod
    def empty_configuration_is_none(cls, value: object) -> object:
        """Trata valores vazios do arquivo de exemplo como ausentes."""
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

    def require_supabase_credentials(self) -> tuple[str, str]:
        """Retorna URL e chave secreta apenas quando o banco for utilizado."""
        key = self.supabase_secret_key or self.supabase_service_role_key
        if self.supabase_url is None or key is None:
            raise ValueError(
                "SUPABASE_URL e SUPABASE_SECRET_KEY não foram configuradas."
            )
        return self.supabase_url, key.get_secret_value()


@lru_cache
def get_settings() -> Settings:
    """Retorna uma instância compartilhada e imutável durante a execução."""
    return Settings()
