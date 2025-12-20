"""Health check utilities"""
from enum import Enum
from typing import Dict, Any
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
from app.core.config import settings


class HealthStatus(str, Enum):
    """Health status enum"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


async def check_database_health(db: AsyncSession) -> Dict[str, Any]:
    """Check database connectivity"""
    try:
        # Simple query to check connection
        result = await db.execute(text("SELECT 1"))
        result.scalar()

        return {
            "status": HealthStatus.HEALTHY,
            "message": "Database connection is healthy",
            "details": {
                "connected": True
            }
        }
    except Exception as e:
        return {
            "status": HealthStatus.UNHEALTHY,
            "message": f"Database connection failed: {str(e)}",
            "details": {
                "connected": False,
                "error": str(e)
            }
        }


async def check_gemini_api_health() -> Dict[str, Any]:
    """Check Gemini API availability"""
    try:
        # Simple check - verify API key is configured
        if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "your-gemini-api-key-here":
            return {
                "status": HealthStatus.DEGRADED,
                "message": "Gemini API key not configured",
                "details": {
                    "configured": False
                }
            }

        # For MVP, just check if key is set
        # In production, could make actual API call with timeout
        return {
            "status": HealthStatus.HEALTHY,
            "message": "Gemini API is configured",
            "details": {
                "configured": True
            }
        }

    except Exception as e:
        return {
            "status": HealthStatus.DEGRADED,
            "message": f"Gemini API check failed: {str(e)}",
            "details": {
                "error": str(e)
            }
        }


def determine_overall_health(checks: Dict[str, Dict[str, Any]]) -> HealthStatus:
    """Determine overall health from individual checks"""
    statuses = [check["status"] for check in checks.values()]

    # If any check is unhealthy, overall is unhealthy
    if HealthStatus.UNHEALTHY in statuses:
        return HealthStatus.UNHEALTHY

    # If any check is degraded, overall is degraded
    if HealthStatus.DEGRADED in statuses:
        return HealthStatus.DEGRADED

    # All checks are healthy
    return HealthStatus.HEALTHY
