"""Simplified OpenTelemetry setup for API Gateway (no database)"""
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


def setup_tracing(service_name: str, environment: str):
    """Setup OpenTelemetry tracing"""
    resource = Resource(attributes={
        "service.name": service_name,
        "environment": environment
    })

    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(ConsoleSpanExporter())
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)


def instrument_app(app):
    """Instrument FastAPI app with OpenTelemetry"""
    FastAPIInstrumentor.instrument_app(app)
