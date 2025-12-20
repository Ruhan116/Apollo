"""Goals Service - Main Application"""
import sys
from pathlib import Path
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

# Add shared library to path
shared_path = Path(__file__).resolve().parent.parent.parent.parent / 'shared'
sys.path.insert(0, str(shared_path))

from shared.database import create_database_engine, create_session_factory, Base
from shared.logging_config import setup_logging
from shared.tracing import setup_tracing, instrument_app
from shared.metrics import setup_metrics
from shared.health import check_database_health, determine_overall_health, HealthStatus
from app.config import settings
from app.routers.goals import router as goals_router
from app.models.goals import Goal, SubGoal, Actions

# Initialize observability
logger = setup_logging(settings.SERVICE_NAME, settings.DEBUG)
setup_tracing(settings.SERVICE_NAME, settings.ENVIRONMENT)

# Create database engine and session factory
engine = create_database_engine(settings.DATABASE_URL, echo=settings.DEBUG)
session_factory = create_session_factory(engine)


async def check_gemini_api_health() -> dict:
    """Check Gemini API availability"""
    try:
        if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "your-gemini-api-key-here":
            return {
                "status": HealthStatus.DEGRADED,
                "message": "Gemini API key not configured",
                "details": {"configured": False}
            }

        return {
            "status": HealthStatus.HEALTHY,
            "message": f"Gemini API configured ({settings.GEMINI_MODEL})",
            "details": {"configured": True, "model": settings.GEMINI_MODEL}
        }
    except Exception as e:
        return {
            "status": HealthStatus.DEGRADED,
            "message": f"Gemini API check failed: {str(e)}",
            "details": {"error": str(e)}
        }


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan"""
    logger.info(f"Starting {settings.SERVICE_NAME}")

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created successfully")

    yield

    logger.info(f"Shutting down {settings.SERVICE_NAME}")


# Create FastAPI app
app = FastAPI(
    title="Goals Service",
    description="AI-Powered Goal Management Service with Gemini 2.5 Flash",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Instrument with observability
instrument_app(app)
setup_metrics(app, settings.SERVICE_NAME)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Database dependency
async def get_db():
    async with session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


# Health check endpoints
@app.get("/health/live")
async def liveness_check():
    """Liveness probe"""
    return {
        "status": "healthy",
        "service": settings.SERVICE_NAME,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.get("/health/ready")
async def readiness_check(db: AsyncSession = Depends(get_db)):
    """Readiness probe"""
    checks = {
        "database": await check_database_health(db),
        "gemini_api": await check_gemini_api_health()
    }

    overall_status = determine_overall_health(checks)

    return {
        "status": overall_status,
        "service": settings.SERVICE_NAME,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "checks": checks
    }


@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """Legacy health check"""
    return await readiness_check(db)


# Include routers
app.include_router(goals_router, prefix="/goals", tags=["Goals"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": settings.SERVICE_NAME,
        "version": "1.0.0",
        "status": "running",
        "ai_model": settings.GEMINI_MODEL
    }
