"""Metrics middleware for custom metric collection"""
import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.metrics import (
    request_count,
    request_duration,
    error_count,
    active_requests
)


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware to collect custom metrics"""

    async def dispatch(self, request: Request, call_next):
        """Collect request metrics"""

        # Increment active requests
        active_requests.inc()

        # Start timer
        start_time = time.time()

        try:
            # Process request
            response: Response = await call_next(request)

            # Record metrics
            duration = time.time() - start_time
            endpoint = request.url.path
            method = request.method
            status = response.status_code

            # Record request count
            request_count.labels(
                method=method,
                endpoint=endpoint,
                status=status
            ).inc()

            # Record duration
            request_duration.labels(
                method=method,
                endpoint=endpoint
            ).observe(duration)

            # Decrement active requests
            active_requests.dec()

            return response

        except Exception as exc:
            # Record error
            error_count.labels(
                error_type=type(exc).__name__,
                endpoint=request.url.path
            ).inc()

            # Decrement active requests
            active_requests.dec()

            raise
