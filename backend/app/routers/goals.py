from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.goals import GoalService
from app.schemas.goal import GoalCreate
from app.database import get_db

router = APIRouter()

@router.post("/create")
async def create(data: GoalCreate, db: AsyncSession = Depends(get_db)):
    service = GoalService(db)
    return await service.create_goal(data.prompt, data.user_id)

