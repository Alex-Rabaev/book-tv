"""User repository — the only layer that touches the DB session for users (AD-1)."""
from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def exists_email(self, email: str) -> bool:
        result = await self.session.execute(select(User.id).where(User.email == email))
        return result.first() is not None

    async def exists_nickname(self, nickname: str) -> bool:
        result = await self.session.execute(select(User.id).where(User.nickname == nickname))
        return result.first() is not None

    async def add(
        self,
        *,
        email: str,
        nickname: str,
        name: str,
        date_of_birth: date,
        password_hash: str,
    ) -> User:
        user = User(
            email=email,
            nickname=nickname,
            name=name,
            date_of_birth=date_of_birth,
            password_hash=password_hash,
        )
        self.session.add(user)
        await self.session.flush()
        return user
