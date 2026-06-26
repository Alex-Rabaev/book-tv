"""Alembic environment — async engine, URL from DATABASE_URL or the repo-root .env (AD-11)."""
import asyncio
import os
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.db import Base

# Import models so their tables register on Base.metadata as they are added in later stories.
import app.models  # noqa: F401


class _MigrationSettings(BaseSettings):
    """Only the DB URL — migrations must not require the app's other secrets.

    Reads the repo-root .env so `alembic upgrade head` works without manually exporting
    DATABASE_URL.  env.py → alembic → backend → <repo root>
    """

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str | None = None

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def _database_url() -> str:
    url = os.getenv("DATABASE_URL") or _MigrationSettings().database_url
    if not url:
        raise RuntimeError(
            "DATABASE_URL is required to run migrations "
            "(set it in the environment or the repo-root .env)."
        )
    return url


def run_migrations_offline() -> None:
    context.configure(
        url=_database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def _do_run_migrations(connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    engine = create_async_engine(_database_url(), future=True)
    async with engine.connect() as connection:
        await connection.run_sync(_do_run_migrations)
    await engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
