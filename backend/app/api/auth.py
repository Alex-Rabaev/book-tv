"""Auth router (AD-1: HTTP boundary; AD-9: consistent error envelope)."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.core.security import create_access_token, create_refresh_token
from app.schemas.auth import RegisterRequest, TokenPair
from app.services.auth import AuthService, UniquenessError

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenPair, status_code=status.HTTP_201_CREATED)
async def register(
    payload: RegisterRequest,
    session: AsyncSession = Depends(get_session),
) -> TokenPair:
    service = AuthService(session)
    try:
        user = await service.register(payload)
    except UniquenessError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"field": exc.field, "message": str(exc)},
        ) from exc
    return TokenPair(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )
