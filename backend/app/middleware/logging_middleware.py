"""Request/Response logging middleware"""
import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging import get_logger, log_with_context

logger = get_logger("apollo.requests")


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all HTTP requests and responses"""

    async def dispatch(self, request: Request, call_next):
        """Log request and response details"""

        # Start timer
        start_time = time.time()

        # Log incoming request
        log_with_context(
            logger,
            "INFO",
            f"Incoming request: {request.method} {request.url.path}",
            method=request.method,
            path=request.url.path,
            query_params=str(request.query_params),
            client_ip=request.client.host if request.client else "unknown",
        )

        # Process request
        try:
            response: Response = await call_next(request)

            # Calculate duration
            duration_ms = round((time.time() - start_time) * 1000, 2)

            # Log response
            log_level = "INFO" if response.status_code < 400 else "WARNING" if response.status_code < 500 else "ERROR"
            log_with_context(
                logger,
                log_level,
                f"Request completed: {request.method} {request.url.path} - {response.status_code}",
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration_ms=duration_ms,
            )

            return response

        except Exception as exc:
            # Calculate duration
            duration_ms = round((time.time() - start_time) * 1000, 2)

            # Log error
            log_with_context(
                logger,
                "ERROR",
                f"Request failed: {request.method} {request.url.path}",
                method=request.method,
                path=request.url.path,
                duration_ms=duration_ms,
                error=str(exc),
            )
            raise
