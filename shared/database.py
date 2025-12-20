"""Shared database utilities"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base


def create_database_engine(database_url: str, echo: bool = True):
    """Create async database engine"""
    engine = create_async_engine(
        database_url,
        echo=echo,
        future=True,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20
    )
    return engine


def create_session_factory(engine):
    """Create async session factory"""
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False
    )


async def get_db_session(session_factory):
    """Dependency to get database session"""
    async with session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


# Base class for models
Base = declarative_base()
