"""Goals repositories"""
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.goals import Goal, SubGoal, Actions
from app.repositories.base import BaseRepository


class GoalRepository(BaseRepository[Goal]):
    def __init__(self, db: AsyncSession):
        super().__init__(Goal, db)


class SubgoalRepository(BaseRepository[SubGoal]):
    def __init__(self, db: AsyncSession):
        super().__init__(SubGoal, db)


class ActionRepository(BaseRepository[Actions]):
    def __init__(self, db: AsyncSession):
        super().__init__(Actions, db)
