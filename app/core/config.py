"""Configuração central do BulaClara via ``pydantic-settings``.

Valores de ambiente esperados (documentados em ``.env.example``):
- ``BULACLARA_API_HOST`` / ``BULACLARA_API_PORT`` — endereço da API local
- ``DATABASE_URL_REMOTE`` — PostgreSQL remoto (Fase 2)
- ``BULACLARA_DB_LOCAL_PATH`` — SQLite local de cache (Fase 2)
- ``ANVISA_BASE_URL`` — Bulário Eletrônico (Fase 3)
- ``LLM_API_KEY`` / ``LLM_BASE_URL`` / ``LLM_MODEL`` — IA generativa (Fase 4)
- ``CORS_ORIGINS`` — origens autorizadas (JSON list)
"""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuração central do backend. Zero segredos hardcoded."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = Field(
        default="BulaClara API",
        validation_alias="BULACLARA_APP_NAME",
    )
    api_host: str = Field(
        default="127.0.0.1",
        validation_alias="BULACLARA_API_HOST",
    )
    api_port: int = Field(
        default=8000,
        validation_alias="BULACLARA_API_PORT",
    )

    # --- Fase 2: bancos de dados ---
    remote_database_url: str | None = Field(
        default=None,
        validation_alias="DATABASE_URL_REMOTE",
    )
    local_db_path: Path = Field(
        default=Path("data/bulaclara_local.db"),
        validation_alias="BULACLARA_DB_LOCAL_PATH",
    )

    # --- Fase 3: ANVISA / Bulário Eletrônico ---
    anvisa_base_url: str = Field(
        default="https://consultas.anvisa.gov.br/api/v1",
        validation_alias="ANVISA_BASE_URL",
    )

    # --- Fase 4: IA generativa (LLM) ---
    llm_api_key: str | None = Field(
        default=None,
        validation_alias="LLM_API_KEY",
    )
    llm_base_url: str | None = Field(
        default=None,
        validation_alias="LLM_BASE_URL",
    )
    llm_model: str = Field(
        default="gpt-4o-mini",
        validation_alias="LLM_MODEL",
    )

    # --- CORS: origens permitidas (dev Next.js + Electron/file) ---
    cors_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:3000", "null"],
        validation_alias="CORS_ORIGINS",
    )


@lru_cache
def get_settings() -> Settings:
    """Singleton com cache — evita re-leitura do `.env` a cada request."""
    return Settings()