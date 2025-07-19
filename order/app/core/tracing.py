from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.trace import set_tracer_provider


def init_tracer(app: FastAPI) -> None:
    """
    Initialize OpenTelemetry tracing for FastAPI with Jaeger OTLP (gRPC).
    """
    tracer_provider = TracerProvider(
        resource=Resource.create({SERVICE_NAME: "order-service"})
    )

    otlp_exporter = OTLPSpanExporter(
        endpoint="http://jaeger:4317",
        insecure=True,  # OTLP gRPC port
    )
    span_processor = BatchSpanProcessor(otlp_exporter)

    tracer_provider.add_span_processor(span_processor)
    set_tracer_provider(tracer_provider)

    FastAPIInstrumentor.instrument_app(app)
