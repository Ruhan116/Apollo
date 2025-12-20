from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.goals import GoalService
from app.schemas.goal import GoalCreate
from app.database import get_db
from app.middleware.rate_limit import limiter

router = APIRouter()

@router.post("/create")
@limiter.limit("20/hour")  # Rate limit for AI-powered goal creation
async def create(request: Request, data: GoalCreate, db: AsyncSession = Depends(get_db)):
    service = GoalService(db)
    return await service.create_goal(data.prompt, data.user_id)

