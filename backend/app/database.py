from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os
from pathlib import Path

# Load environment variables
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file")

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  
    future=True,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Create async session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Dependency for FastAPI
async def get_db() -> AsyncSession:
    """Dependency to get database session"""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()

# Function to create tables
async def create_tables():
    """Create all tables in the database"""
    from app.models.base import Base
    from app.models.user import User  
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Function to drop tables 
async def drop_tables():
    """Drop all tables in the database"""
    from app.models.base import Base
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
