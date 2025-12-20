"""Service-to-service authentication utilities"""
from fastapi import Header, HTTPException, status
from typing import Optional


class ServiceAuthError(Exception):
    """Service authentication error"""
    pass


def verify_service_key(expected_key: str, provided_key: Optional[str]) -> bool:
    """Verify service API key"""
    if not expected_key:
        return True  # If no key configured, skip validation (dev mode)

    if not provided_key:
        return False

    return provided_key == expected_key


async def require_service_auth(
    x_service_key: Optional[str] = Header(None),
    expected_key: str = ""
):
    """Dependency to require service authentication"""
    if not verify_service_key(expected_key, x_service_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid service credentials",
            headers={"WWW-Authenticate": "ServiceKey"},
        )
    return True
