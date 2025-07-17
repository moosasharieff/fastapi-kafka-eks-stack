"""Tracing initialization using OpenTelemetry for FastAPI and aiokafka."""

from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.trace import set_tracer_provider


def init_tracer(app: FastAPI) -> None:
    """
    Initialize OpenTelemetry tracing with OTLP HTTP exporter.

    This sets up the TracerProvider with a BatchSpanProcessor and
    configures automatic instrumentation for FastAPI and aiokafka.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    tracer_provider = TracerProvider()
    span_processor = BatchSpanProcessor(OTLPSpanExporter())
    tracer_provider.add_span_processor(span_processor)
    set_tracer_provider(tracer_provider)

    FastAPIInstrumentor.instrument_app(app)
