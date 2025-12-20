"""Tracing middleware to propagate trace context"""
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from app.core.logging import correlation_id_var


class TraceMiddleware(BaseHTTPMiddleware):
    """Middleware to enhance tracing with custom attributes"""

    async def dispatch(self, request: Request, call_next):
        """Add custom attributes to trace spans"""

        # Get current span
        span = trace.get_current_span()

        # Add custom attributes
        if span.is_recording():
            span.set_attribute("http.route", request.url.path)
            span.set_attribute("http.method", request.method)
            span.set_attribute("correlation_id", correlation_id_var.get())

            if request.client:
                span.set_attribute("http.client_ip", request.client.host)

        try:
            # Process request
            response: Response = await call_next(request)

            # Add response status to span
            if span.is_recording():
                span.set_attribute("http.status_code", response.status_code)

                # Set span status based on HTTP status
                if response.status_code >= 500:
                    span.set_status(Status(StatusCode.ERROR))
                elif response.status_code >= 400:
                    span.set_status(Status(StatusCode.ERROR))
                else:
                    span.set_status(Status(StatusCode.OK))

            return response

        except Exception as exc:
            # Record exception in span
            if span.is_recording():
                span.set_status(Status(StatusCode.ERROR))
                span.record_exception(exc)
            raise
