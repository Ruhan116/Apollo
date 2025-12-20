"""Shared metrics utilities"""
from prometheus_client import Counter, Histogram, Gauge
from prometheus_fastapi_instrumentator import Instrumentator


def create_service_metrics(service_name: str):
    """Create standard metrics for a service"""

    metrics = {
        "request_count": Counter(
            f'{service_name}_http_requests_total',
            'Total HTTP requests',
            ['method', 'endpoint', 'status']
        ),
        "request_duration": Histogram(
            f'{service_name}_http_request_duration_seconds',
            'HTTP request duration in seconds',
            ['method', 'endpoint']
        ),
        "error_count": Counter(
            f'{service_name}_errors_total',
            'Total errors',
            ['error_type', 'endpoint']
        ),
        "active_requests": Gauge(
            f'{service_name}_http_requests_active',
            'Number of active HTTP requests'
        ),
    }

    return metrics


def setup_metrics(app, service_name: str):
    """Setup Prometheus metrics for FastAPI app"""

    instrumentator = Instrumentator(
        should_group_status_codes=False,
        should_ignore_untemplated=False,
        should_respect_env_var=True,
        should_instrument_requests_inprogress=True,
        excluded_handlers=["/metrics"],
        env_var_name="ENABLE_METRICS",
        inprogress_name=f"{service_name}_http_requests_inprogress",
        inprogress_labels=True,
    )

    instrumentator.instrument(app)
    instrumentator.expose(app, endpoint="/metrics", include_in_schema=False)

    return instrumentator
