"""Correlation ID middleware for request tracing"""
import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging import correlation_id_var


class CorrelationIDMiddleware(BaseHTTPMiddleware):
    """Middleware to add correlation ID to all requests"""

    async def dispatch(self, request: Request, call_next):
        """Add correlation ID to request and response headers"""

        # Get correlation ID from header or generate new one
        correlation_id = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())

        # Set correlation ID in context var (accessible throughout request lifecycle)
        correlation_id_var.set(correlation_id)

        # Process request
        response: Response = await call_next(request)

        # Add correlation ID to response headers
        response.headers["X-Correlation-ID"] = correlation_id

        return response
