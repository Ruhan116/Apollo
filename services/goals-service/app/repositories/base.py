"""Base repository with generic CRUD operations"""
import sys
from pathlib import Path
from typing import Generic, TypeVar, Type, Optional

# Add shared library to path
shared_path = Path(__file__).resolve().parent.parent.parent.parent.parent / 'shared'
sys.path.insert(0, str(shared_path))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from shared.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def create(self, obj_in: ModelType) -> ModelType:
        """Adds a new record, commits it, and refreshes the object."""
        self.db.add(obj_in)
        await self.db.commit()
        await self.db.refresh(obj_in)
        return obj_in

    async def get_by_id(self, id: int) -> Optional[ModelType]:
        """Fetches a single record by ID."""
        query = select(self.model).where(self.model.id == id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def delete(self, id: int) -> bool:
        """Delete a record by ID."""
        obj = await self.get_by_id(id)
        if obj:
            await self.db.delete(obj)
            await self.db.commit()
            return True
        return False
