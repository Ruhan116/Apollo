"""User repository"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.repositories.base import BaseRepository
from app.schemas.auth import UserCreate


class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    async def get_by_email(self, email: str) -> User | None:
        """Find a user by email."""
        query = select(self.model).where(self.model.email == email)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def create(self, user_data: UserCreate) -> User:
        """Create a new user from UserCreate schema."""
        user = User(
            user_name=user_data.user_name,
            email=user_data.email,
            hashed_password=user_data.password
        )
        return await super().create(user)

    async def update_password(self, user: User, new_hashed_password: str) -> User:
        """Update a user's hashed password and persist to the DB."""
        user.hashed_password = new_hashed_password
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
