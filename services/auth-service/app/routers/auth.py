"""Auth router"""
import sys
from pathlib import Path
from fastapi import APIRouter, Depends, Request, Header
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

# Add shared library to path
shared_path = Path(__file__).resolve().parent.parent.parent.parent.parent / 'shared'
sys.path.insert(0, str(shared_path))

from app.schemas.auth import UserCreate, UserLogin
from app.services.auth import AuthService
from app.config import settings
from shared.service_auth import require_service_auth

router = APIRouter()

# Database dependency
async def get_db():
    from app.main import session_factory
    async with session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


@router.post("/register")
async def register(request: Request, user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user"""
    service = AuthService(db)
    return await service.register_user(user_data)


@router.post("/login")
async def login(request: Request, user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    """Login user"""
    service = AuthService(db)
    return await service.login(user_data)


@router.post("/verify")
async def verify_token(
    token: str,
    db: AsyncSession = Depends(get_db),
    x_service_key: Optional[str] = Header(None)
):
    """Verify JWT token (for other services)"""
    # Verify service auth
    await require_service_auth(x_service_key, settings.SERVICE_API_KEY)

    service = AuthService(db)
    return await service.verify_token(token)


@router.get("/user/{user_id}")
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    x_service_key: Optional[str] = Header(None)
):
    """Get user by ID (for other services)"""
    # Verify service auth
    await require_service_auth(x_service_key, settings.SERVICE_API_KEY)

    service = AuthService(db)
    return await service.get_user_by_id(user_id)
