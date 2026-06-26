"""Auth use cases (AD-7: mutations in the service within one transaction)."""
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.auth import RegisterRequest


class UniquenessError(Exception):
    """Raised when email or nickname is already taken; `field` names which one."""

    def __init__(self, field: str) -> None:
        super().__init__(f"{field} already in use")
        self.field = field


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.users = UserRepository(session)

    async def register(self, data: RegisterRequest) -> User:
        # Pre-check for friendly, attributed errors...
        if await self.users.exists_email(data.email):
            raise UniquenessError("email")
        if await self.users.exists_nickname(data.nickname):
            raise UniquenessError("nickname")

        user = await self.users.add(
            email=data.email,
            nickname=data.nickname,
            name=data.name,
            date_of_birth=data.date_of_birth,
            password_hash=hash_password(data.password),
        )
        try:
            await self.session.commit()
        except IntegrityError:
            # ...and the DB UNIQUE constraints as the source of truth on races (AD-9).
            await self.session.rollback()
            field = "email" if await self.users.exists_email(data.email) else "nickname"
            raise UniquenessError(field) from None
        return user
