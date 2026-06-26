"""Integration tests for POST /auth/register (FR-1).

Runs against an in-memory SQLite (StaticPool) so the registration logic — uniqueness,
hashing, token issuance — is exercised without a live Postgres. The app and migrations
remain Postgres-targeted; the ORM types used are cross-dialect.
"""
import jwt
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

import app.models.user  # noqa: F401  (register the model on Base.metadata)
from app.core.config import get_settings
from app.core.db import Base, get_session
from app.core.security import ALGORITHM
from app.main import app

VALID = {
    "email": "maya@example.com",
    "password": "supersecret1",
    "name": "Maya",
    "date_of_birth": "1999-05-01",
    "nickname": "maya",
}


@pytest_asyncio.fixture
async def client():
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    test_session = async_sessionmaker(engine, expire_on_commit=False)

    async def override_session():
        async with test_session() as session:
            yield session

    app.dependency_overrides[get_session] = override_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as http_client:
        yield http_client
    app.dependency_overrides.clear()
    await engine.dispose()


async def test_register_success(client):
    resp = await client.post("/auth/register", json=VALID)
    assert resp.status_code == 201
    body = resp.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert body["refresh_token"]
    assert "password" not in body
    assert "password_hash" not in body
    decoded = jwt.decode(
        body["access_token"], get_settings().jwt_secret, algorithms=[ALGORITHM]
    )
    assert decoded["token_type"] == "access"


async def test_register_duplicate_email_409_names_email(client):
    await client.post("/auth/register", json=VALID)
    resp = await client.post("/auth/register", json={**VALID, "nickname": "maya2"})
    assert resp.status_code == 409
    assert resp.json()["detail"]["field"] == "email"


async def test_register_duplicate_nickname_409_names_nickname(client):
    await client.post("/auth/register", json=VALID)
    resp = await client.post("/auth/register", json={**VALID, "email": "other@example.com"})
    assert resp.status_code == 409
    assert resp.json()["detail"]["field"] == "nickname"


async def test_register_invalid_email_422(client):
    resp = await client.post("/auth/register", json={**VALID, "email": "not-an-email"})
    assert resp.status_code == 422


async def test_register_short_password_422(client):
    resp = await client.post("/auth/register", json={**VALID, "password": "short"})
    assert resp.status_code == 422
