"""Testes das configurações do backend."""

import pytest
from pydantic import SecretStr, ValidationError

from app.core.config import Settings


def test_settings_have_safe_academic_defaults() -> None:
    settings = Settings(_env_file=None)

    assert settings.frontend_origin == "http://localhost:5173"
    assert settings.retrieval_top_k == 5
    assert settings.max_upload_size_mb == 10
    assert settings.openrouter_api_key is None


def test_openrouter_key_is_masked() -> None:
    settings = Settings(_env_file=None, openrouter_api_key="segredo-de-teste")

    assert isinstance(settings.openrouter_api_key, SecretStr)
    assert "segredo-de-teste" not in repr(settings)
    assert settings.require_openrouter_api_key() == "segredo-de-teste"


def test_openrouter_key_is_validated_only_when_used() -> None:
    settings = Settings(_env_file=None)

    with pytest.raises(ValueError, match="OPENROUTER_API_KEY"):
        settings.require_openrouter_api_key()


def test_supabase_credentials_are_masked_and_required_together() -> None:
    settings = Settings(
        _env_file=None,
        supabase_url="https://project.supabase.co",
        supabase_secret_key="segredo-do-banco",
    )

    assert "segredo-do-banco" not in repr(settings)
    assert settings.require_supabase_credentials() == (
        "https://project.supabase.co",
        "segredo-do-banco",
    )


def test_legacy_supabase_service_role_key_remains_supported() -> None:
    settings = Settings(
        _env_file=None,
        supabase_url="https://project.supabase.co",
        supabase_service_role_key="chave-legada",
    )

    assert settings.require_supabase_credentials()[1] == "chave-legada"


def test_supabase_credentials_are_validated_only_when_used() -> None:
    settings = Settings(_env_file=None)

    with pytest.raises(ValueError, match="SUPABASE_URL"):
        settings.require_supabase_credentials()


def test_chunk_overlap_must_be_smaller_than_chunk_size() -> None:
    with pytest.raises(ValidationError, match="CHUNK_OVERLAP"):
        Settings(_env_file=None, chunk_size=500, chunk_overlap=500)
