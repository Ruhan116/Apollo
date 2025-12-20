"""Structured JSON logging configuration"""
import logging
import json
import sys
from datetime import datetime
from typing import Any
from contextvars import ContextVar

from app.core.config import settings

# Context variable for correlation ID
correlation_id_var: ContextVar[str] = ContextVar('correlation_id', default='')


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging"""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "service": settings.SERVICE_NAME,
            "correlation_id": correlation_id_var.get() or "N/A",
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add extra fields
        if hasattr(record, "extra_fields"):
            log_data.update(record.extra_fields)

        return json.dumps(log_data)


def setup_logging() -> logging.Logger:
    """Configure and return application logger"""

    # Create logger
    logger = logging.getLogger("apollo")
    logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

    # Remove existing handlers
    logger.handlers.clear()

    # Create console handler with JSON formatter
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(JSONFormatter())
    logger.addHandler(console_handler)

    # Prevent propagation to root logger
    logger.propagate = False

    return logger


def get_logger(name: str = "apollo") -> logging.Logger:
    """Get logger instance"""
    return logging.getLogger(name)


def log_with_context(logger: logging.Logger, level: str, message: str, **kwargs: Any) -> None:
    """Log message with additional context"""
    extra_fields = kwargs
    getattr(logger, level.lower())(message, extra={"extra_fields": extra_fields})


# Initialize logger
logger = setup_logging()
