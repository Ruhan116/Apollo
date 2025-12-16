from fastapi import APIRouter
from app.schemas.auth import UserCreate, UserLogin

router = APIRouter()

@router.post("/register")
async def register(user_data: UserCreate):
    pass 

@router.post("/login")
async def login(user_data: UserLogin):
    pass 
