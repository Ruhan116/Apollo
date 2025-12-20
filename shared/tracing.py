"""Shared tracing utilities"""
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
try:
    from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
except Exception:
    SQLAlchemyInstrumentor = None
try:
    from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
except Exception:
    HTTPXClientInstrumentor = None


def setup_tracing(service_name: str, environment: str = "development"):
    """Configure OpenTelemetry tracing"""

    # Create resource with service name
    resource = Resource(attributes={
        SERVICE_NAME: service_name,
        "environment": environment,
    })

    # Create tracer provider
    provider = TracerProvider(resource=resource)

    # Add console exporter for MVP
    console_exporter = ConsoleSpanExporter()
    processor = BatchSpanProcessor(console_exporter)
    provider.add_span_processor(processor)

    # Set global tracer provider
    trace.set_tracer_provider(provider)


def instrument_app(app):
    """Instrument FastAPI application"""
    # Instrument FastAPI if available
    try:
        FastAPIInstrumentor.instrument_app(app)
    except Exception:
        pass

    # Instrument SQLAlchemy if the instrumentor is available
    if SQLAlchemyInstrumentor is not None:
        try:
            SQLAlchemyInstrumentor().instrument()
        except Exception:
            pass

    # Instrument HTTPX if available
    if HTTPXClientInstrumentor is not None:
        try:
            HTTPXClientInstrumentor().instrument()
        except Exception:
            pass


def get_tracer(name: str):
    """Get tracer instance"""
    return trace.get_tracer(name)
