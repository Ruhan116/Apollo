"""Shared health check utilities"""
from enum import Enum
from typing import Dict, Any
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class HealthStatus(str, Enum):
    """Health status enum"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


async def check_database_health(db: AsyncSession) -> Dict[str, Any]:
    """Check database connectivity"""
    try:
        result = await db.execute(text("SELECT 1"))
        result.scalar()

        return {
            "status": HealthStatus.HEALTHY,
            "message": "Database connection is healthy",
            "details": {"connected": True}
        }
    except Exception as e:
        return {
            "status": HealthStatus.UNHEALTHY,
            "message": f"Database connection failed: {str(e)}",
            "details": {"connected": False, "error": str(e)}
        }


def determine_overall_health(checks: Dict[str, Dict[str, Any]]) -> HealthStatus:
    """Determine overall health from individual checks"""
    statuses = [check["status"] for check in checks.values()]

    if HealthStatus.UNHEALTHY in statuses:
        return HealthStatus.UNHEALTHY
    if HealthStatus.DEGRADED in statuses:
        return HealthStatus.DEGRADED
    return HealthStatus.HEALTHY
