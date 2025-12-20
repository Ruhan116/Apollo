from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import UserCreate, UserLogin
from app.services.auth import AuthService
from app.database import get_db
from app.middleware.rate_limit import limiter

router = APIRouter()

@router.post("/register")
@limiter.limit("5/minute")  # Strict rate limit for registration
async def register(request: Request, user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.register_user(user_data)

@router.post("/login")
@limiter.limit("10/minute")  # Strict rate limit for login
async def login(request: Request, user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.login(user_data)
