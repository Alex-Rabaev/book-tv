"""Auth request/response schemas (Pydantic, never raw ORM models)."""
from datetime import date

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    name: str = Field(min_length=1, max_length=200)
    date_of_birth: date
    nickname: str = Field(min_length=3, max_length=50)


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
