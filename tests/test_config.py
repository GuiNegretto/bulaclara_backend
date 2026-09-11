"""Testes da configuração central (Fase 0)."""

from app.core.config import get_settings


def test_config_defaults():
    """Sem variáveis de ambiente, os defaults precisam ser os esperados."""
    settings = get_settings()
    assert settings.app_name == "BulaClara API"
    assert settings.api_host == "127.0.0.1"
    assert settings.api_port == 8000
    assert settings.local_db_path == __import__("pathlib").Path("data/bulaclara_local.db")