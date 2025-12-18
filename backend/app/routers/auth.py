from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import UserCreate, UserLogin
from app.services.auth import AuthService
from app.database import get_db

router = APIRouter()

@router.post("/register")
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.register_user(user_data)

@router.post("/login")
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.login(user_data)
