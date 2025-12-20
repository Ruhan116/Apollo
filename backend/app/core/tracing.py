"""Distributed tracing configuration with OpenTelemetry"""
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

from app.core.config import settings


def setup_tracing():
    """Configure OpenTelemetry tracing"""

    # Create resource with service name
    resource = Resource(attributes={
        SERVICE_NAME: settings.SERVICE_NAME,
        "environment": settings.ENVIRONMENT,
    })

    # Create tracer provider
    provider = TracerProvider(resource=resource)

    # Add console exporter for MVP (later: Jaeger/Zipkin)
    console_exporter = ConsoleSpanExporter()
    processor = BatchSpanProcessor(console_exporter)
    provider.add_span_processor(processor)

    # Set global tracer provider
    trace.set_tracer_provider(provider)


def instrument_app(app):
    """Instrument FastAPI application and dependencies"""

    # Instrument FastAPI
    FastAPIInstrumentor.instrument_app(app)

    # Instrument SQLAlchemy (will auto-instrument when engine is used)
    SQLAlchemyInstrumentor().instrument()

    # Instrument HTTPX (for service-to-service calls)
    HTTPXClientInstrumentor().instrument()


def get_tracer(name: str = "apollo"):
    """Get tracer instance"""
    return trace.get_tracer(name)
