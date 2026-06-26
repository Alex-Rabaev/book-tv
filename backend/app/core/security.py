"""Password hashing (Argon2id via pwdlib) and JWT issuance (PyJWT) — AD-6.

NOT passlib / python-jose (both abandoned).
"""
import uuid
from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from app.core.config import get_settings

_hasher = PasswordHash.recommended()

ALGORITHM = "HS256"
ACCESS_TTL = timedelta(minutes=60)
REFRESH_TTL = timedelta(days=7)


def hash_password(password: str) -> str:
    return _hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return _hasher.verify(password, password_hash)


def _create_token(subject: uuid.UUID, token_type: str, ttl: timedelta) -> str:
    now = datetime.now(UTC)
    payload = {
        "sub": str(subject),
        "iat": now,
        "exp": now + ttl,
        "token_type": token_type,
    }
    return jwt.encode(payload, get_settings().jwt_secret, algorithm=ALGORITHM)


def create_access_token(subject: uuid.UUID) -> str:
    return _create_token(subject, "access", ACCESS_TTL)


def create_refresh_token(subject: uuid.UUID) -> str:
    return _create_token(subject, "refresh", REFRESH_TTL)
