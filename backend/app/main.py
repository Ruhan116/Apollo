"""
Apollo Backend - FastAPI Application Entry Point
"""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from app.database import create_tables, get_db
from app.core.config import settings
from app.routers import auth
from app.middleware.correlation import CorrelationIDMiddleware
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.trace_middleware import TraceMiddleware
from app.middleware.metrics_middleware import MetricsMiddleware
from app.middleware.rate_limit import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.logging import logger, setup_logging
from app.core.tracing import setup_tracing, instrument_app
from app.core.metrics import setup_metrics

# Initialize observability
setup_logging()
setup_tracing()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    logger.info(f"Starting {app.title}")
    await create_tables()
    logger.info("Database tables created successfully")
    yield
    # Shutdown
    logger.info("Shutting down application")

app = FastAPI(
    title="Apollo API",
    description="AI-Powered Socratic Goal Mentor Platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# Instrument app with OpenTelemetry
instrument_app(app)

# Setup Prometheus metrics
setup_metrics(app)

# Setup rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Middleware Stack (order matters - first added is executed last)
# Add Correlation ID middleware first (executed first in chain)
app.add_middleware(CorrelationIDMiddleware)

# Add Metrics middleware
app.add_middleware(MetricsMiddleware)

# Add Trace middleware
app.add_middleware(TraceMiddleware)

# Add Logging middleware
app.add_middleware(LoggingMiddleware)

# CORS Configuration
# TODO: Update origins for production deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js development server
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "Apollo API is running",
        "version": "1.0.0",
        "status": "healthy"
    }


@app.get("/health/live")
async def liveness_check():
    """Liveness probe - is the service running?"""
    return {
        "status": "healthy",
        "service": settings.SERVICE_NAME,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.get("/health/ready")
async def readiness_check(db: AsyncSession = Depends(get_db)):
    """Readiness probe - can the service accept traffic?"""
    from app.core.health import (
        check_database_health,
        check_gemini_api_health,
        determine_overall_health,
        HealthStatus
    )

    # Run health checks
    checks = {
        "database": await check_database_health(db),
        "gemini_api": await check_gemini_api_health()
    }

    # Determine overall health
    overall_status = determine_overall_health(checks)

    return {
        "status": overall_status,
        "service": settings.SERVICE_NAME,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "checks": checks
    }


@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """Legacy health check endpoint (redirects to readiness)"""
    return await readiness_check(db)


# TODO: Register routers when implemented
from app.routers import auth, goals
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(goals.router, prefix="/api/goals", tags=["Goals"])
# app.include_router(ai.router, prefix="/api/chat", tags=["AI Mentor"])
# app.include_router(community.router, prefix="/api/forums", tags=["Community"])
# app.include_router(notes.router, prefix="/api/notes", tags=["Notes"])
