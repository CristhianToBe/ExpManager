from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Gestor de Expedientes API"
    app_version: str = "0.1.0"
    api_prefix: str = "/api/v1"
    default_sqlite_url: str = "sqlite:///./gestor-dev.db"
    workspace_config_name: str = "config.json"
    technical_dir_name: str = ".gestor"
    db_filename: str = "gestor.db"
    model_config = SettingsConfigDict(env_prefix="GESTOR_")


@lru_cache
def get_settings() -> Settings:
    return Settings()


def get_runtime_state_path() -> Path:
    return Path.home() / ".gestor-expedientes" / "runtime.json"
