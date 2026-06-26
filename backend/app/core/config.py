"""Application configuration loaded from environment (AD-2: secrets server-side only)."""
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Single source of truth: the repo-root .env, resolved from this file's location so it
# is found regardless of the working directory the process is started from.
# config.py → core → app → backend → <repo root>
ROOT_ENV = Path(__file__).resolve().parents[3] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT_ENV,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Secrets / connections — no defaults, must come from the environment.
    database_url: str
    jwt_secret: str
    openai_api_key: str
    supabase_url: str
    supabase_service_key: str

    # Non-secret operational config.
    cors_origin: str = "http://localhost:5173"
    app_name: str = "book-tv API"


@lru_cache
def get_settings() -> Settings:
    return Settings()
