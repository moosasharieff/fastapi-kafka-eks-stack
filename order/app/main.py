from fastapi import FastAPI
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
import logging

from order.app.core.config import settings
from order.app.core.logging import init_logger
from order.app.core.tracing import init_tracer
from order.app.db.session import engine
from order.app.kafka.producer import kafka_producer
from order.app.db.init_db import create_db
from order.app.api.routes import router
from order.app.api.db_health import router as db_health_router

init_logger()
logger = logging.getLogger(settings.service_name)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle hook for app startup and shutdown.
    Initializes tracing, DB, and Kafka producer.
    """
    try:
        logger.info("Starting Order Service...")
        init_tracer(app)

        await create_db()
        await kafka_producer.start()
        logger.info("Kafka producer started.")

        yield

    except Exception as e:
        logger.error(f"Error during startup: {e}", exc_info=True)
        raise
    finally:
        await kafka_producer.stop()
        logger.info("Kafka producer stopped. Order Service shutting down.")
        await engine.dispose()
        logger.info("Database engine disposed. Order Service shutting down.")


# Initialize FastAPI app
app = FastAPI(
    title="Order Service",
    version="1.0.0",
    description="Handles order creation and publishes to Kafka.",
    lifespan=lifespan
)

# Register Prometheus instrumentation BEFORE app starts
Instrumentator().instrument(app).expose(app)
logger.info("Prometheus metrics registered at /metrics")

# Register routes
app.include_router(router)
app.include_router(db_health_router)
