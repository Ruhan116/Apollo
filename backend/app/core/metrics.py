"""Prometheus metrics configuration"""
from prometheus_client import Counter, Histogram, Gauge, REGISTRY
from prometheus_fastapi_instrumentator import Instrumentator
from app.core.config import settings

# Custom metrics
request_count = Counter(
    'apollo_http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'apollo_http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

error_count = Counter(
    'apollo_errors_total',
    'Total errors',
    ['error_type', 'endpoint']
)

active_requests = Gauge(
    'apollo_http_requests_active',
    'Number of active HTTP requests'
)

db_connection_pool_size = Gauge(
    'apollo_db_connection_pool_size',
    'Database connection pool size'
)

db_connection_pool_used = Gauge(
    'apollo_db_connection_pool_used',
    'Database connections currently in use'
)

# Gemini API metrics
gemini_api_calls = Counter(
    'apollo_gemini_api_calls_total',
    'Total Gemini API calls',
    ['status']
)

gemini_api_duration = Histogram(
    'apollo_gemini_api_duration_seconds',
    'Gemini API call duration in seconds'
)


def setup_metrics(app):
    """Setup Prometheus metrics for FastAPI app"""

    # Create instrumentator
    instrumentator = Instrumentator(
        should_group_status_codes=False,
        should_ignore_untemplated=False,
        should_respect_env_var=True,
        should_instrument_requests_inprogress=True,
        excluded_handlers=["/metrics"],
        env_var_name="ENABLE_METRICS",
        inprogress_name="apollo_http_requests_inprogress",
        inprogress_labels=True,
    )

    # Instrument the app
    instrumentator.instrument(app)

    # Expose metrics endpoint
    instrumentator.expose(app, endpoint="/metrics", include_in_schema=False)

    return instrumentator
