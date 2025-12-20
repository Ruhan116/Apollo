"""API Gateway - Main entry point"""
import sys
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging

# Add shared library to path
shared_path = Path(__file__).resolve().parent.parent.parent.parent / 'shared'
sys.path.insert(0, str(shared_path))

from app.config import settings
from app.middleware.auth_middleware import AuthMiddleware
from app.middleware.correlation_middleware import CorrelationIDMiddleware
from app.routers import proxy
from shared.logging_config import setup_logging
from app.tracing_simple import setup_tracing, instrument_app
from shared.metrics import setup_metrics

# Setup logging
logger = setup_logging(settings.SERVICE_NAME, settings.DEBUG)

# Setup tracing
setup_tracing(settings.SERVICE_NAME, settings.ENVIRONMENT)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan"""
    logger.info(f"Starting {settings.SERVICE_NAME}")
    logger.info(f"Routing to services:")
    logger.info(f"  - Auth Service: {settings.AUTH_SERVICE_URL}")
    logger.info(f"  - Goals Service: {settings.GOALS_SERVICE_URL}")

    yield

    logger.info(f"Shutting down {settings.SERVICE_NAME}")


# Create FastAPI app
app = FastAPI(
    title="Apollo API Gateway",
    description="API Gateway for Apollo microservices",
    version="1.0.0",
    lifespan=lifespan
)

# Add OpenTelemetry instrumentation
instrument_app(app)

# Add Prometheus metrics
setup_metrics(app, settings.SERVICE_NAME)

# Add CORS middleware
allowed_origins = settings.CORS_ORIGINS.split(",") if isinstance(settings.CORS_ORIGINS, str) else settings.CORS_ORIGINS
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware (order matters!)
app.add_middleware(CorrelationIDMiddleware)  # First: Add correlation IDs
app.add_middleware(AuthMiddleware)           # Second: Validate authentication

# Include routers
app.include_router(proxy.router)


# Health check endpoints
@app.get("/health/live")
async def liveness():
    """Liveness probe"""
    return {
        "status": "healthy",
        "service": settings.SERVICE_NAME,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@app.get("/health/ready")
async def readiness():
    """Readiness probe - checks if backend services are reachable"""
    import httpx

    checks = {}
    overall_status = "healthy"

    # Check Auth Service
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.AUTH_SERVICE_URL}/health/live",
                timeout=2.0
            )
            if response.status_code == 200:
                checks["auth_service"] = {
                    "status": "healthy",
                    "url": settings.AUTH_SERVICE_URL
                }
            else:
                checks["auth_service"] = {
                    "status": "unhealthy",
                    "url": settings.AUTH_SERVICE_URL,
                    "error": f"HTTP {response.status_code}"
                }
                overall_status = "degraded"
    except Exception as e:
        checks["auth_service"] = {
            "status": "unhealthy",
            "url": settings.AUTH_SERVICE_URL,
            "error": str(e)
        }
        overall_status = "degraded"

    # Check Goals Service
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.GOALS_SERVICE_URL}/health/live",
                timeout=2.0
            )
            if response.status_code == 200:
                checks["goals_service"] = {
                    "status": "healthy",
                    "url": settings.GOALS_SERVICE_URL
                }
            else:
                checks["goals_service"] = {
                    "status": "unhealthy",
                    "url": settings.GOALS_SERVICE_URL,
                    "error": f"HTTP {response.status_code}"
                }
                overall_status = "degraded"
    except Exception as e:
        checks["goals_service"] = {
            "status": "unhealthy",
            "url": settings.GOALS_SERVICE_URL,
            "error": str(e)
        }
        overall_status = "degraded"

    return {
        "status": overall_status,
        "service": settings.SERVICE_NAME,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "checks": checks
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Apollo API Gateway",
        "version": "1.0.0",
        "status": "running",
        "routes": {
            "auth": "/api/auth/*",
            "goals": "/api/goals/*",
            "health": "/health/*",
            "docs": "/docs"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
