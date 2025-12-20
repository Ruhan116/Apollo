"""Circuit breaker implementation for fault tolerance"""
from circuitbreaker import circuit
from functools import wraps
from app.core.logging import get_logger
from app.core.metrics import error_count

logger = get_logger("apollo.circuit_breaker")


def gemini_circuit_breaker(func):
    """
    Circuit breaker decorator for Gemini API calls

    Thresholds:
    - Failure threshold: 5 failures
    - Recovery timeout: 30 seconds
    - Expected exception: Exception (catch all)
    """

    @circuit(failure_threshold=5, recovery_timeout=30, expected_exception=Exception)
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            # Log circuit breaker event
            logger.error(
                f"Circuit breaker triggered for {func.__name__}",
                extra={"extra_fields": {"function": func.__name__, "error": str(e)}}
            )

            # Record error metric
            error_count.labels(
                error_type="circuit_breaker_open",
                endpoint="gemini_api"
            ).inc()

            raise

    return wrapper


class CircuitBreakerOpen(Exception):
    """Exception raised when circuit breaker is open"""
    pass
