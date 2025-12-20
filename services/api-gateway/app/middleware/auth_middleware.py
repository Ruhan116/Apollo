"""Authentication Middleware for API Gateway"""
import httpx
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware to validate JWT tokens and extract user information"""

    async def dispatch(self, request: Request, call_next):
        # Skip authentication for public routes
        if self._is_public_route(request.url.path):
            return await call_next(request)

        # Extract JWT token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid authorization header",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = auth_header.split("Bearer ")[1]

        # Validate token with Auth Service
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.AUTH_SERVICE_URL}/auth/verify",
                    params={"token": token},
                    headers={"X-Service-Key": settings.AUTH_SERVICE_API_KEY},
                    timeout=5.0
                )

                if response.status_code != 200:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid or expired token",
                        headers={"WWW-Authenticate": "Bearer"},
                    )

                # Extract user info from response
                user_data = response.json()
                user_id = user_data.get("user_id")
                email = user_data.get("email")

                # Add user info to request state for downstream use
                request.state.user_id = user_id
                request.state.email = email

                logger.info(
                    f"Authenticated user: {email} (ID: {user_id})",
                    extra={"extra_fields": {"user_id": user_id, "email": email}}
                )

        except httpx.TimeoutException:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Authentication service unavailable",
            )
        except httpx.RequestError as e:
            logger.error(f"Failed to validate token: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Authentication service error",
            )

        return await call_next(request)

    def _is_public_route(self, path: str) -> bool:
        """Check if the route is public (no auth required)"""
        return any(path.startswith(route) for route in settings.PUBLIC_ROUTES)
