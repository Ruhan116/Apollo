"""Goals router"""
import sys
from pathlib import Path
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

# Add shared library to path
shared_path = Path(__file__).resolve().parent.parent.parent.parent.parent / 'shared'
sys.path.insert(0, str(shared_path))

from app.services.goals import GoalService
from app.schemas.goal import GoalCreate
from fastapi import Header, HTTPException
from shared.service_auth import require_service_auth
from app.config import settings

router = APIRouter()


# Database dependency
async def get_db():
    from app.main import session_factory
    async with session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


@router.post("/create")
async def create(
    request: Request,
    data: GoalCreate,
    db: AsyncSession = Depends(get_db),
    x_service_key: str | None = Header(None),
):
    """Create a new goal with AI-powered breakdown"""
    # Verify request came through API Gateway (service key)
    await require_service_auth(x_service_key, settings.GOALS_SERVICE_API_KEY)

    # Only accept user id from the header (set by gateway)
    user_id = request.headers.get("X-User-ID")
    if not user_id:
        raise HTTPException(status_code=401, detail="Missing user identity")

    user_id = int(user_id)

    service = GoalService(db)
    return await service.create_goal(data.prompt, user_id)
