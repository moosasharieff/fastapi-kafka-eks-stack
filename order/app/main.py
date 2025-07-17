import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator

from order.app.core.config import settings
from order.app.core.logging import init_logger
from order.app.core.tracing import init_tracer
from order.app.db.session import engine
from order.app.kafka.producer import kafka_producer
from order.app.db.init_db import create_db
from order.app.api.routes import router
from order.app.api.db_health import router as db_health_router

# Initialize logging
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
        create_db()

        await kafka_producer.start()
        logger.info("Kafka producer started.")

        Instrumentator().instrument(app).expose(app)
        logger.info("Prometheus metrics registers at /metrics")

        yield

    except Exception as e:
        logger.error(f"Error during startup: {e}", exc_info=True)
        raise
    finally:
        await kafka_producer.stop()
        logger.info("Kafka producer stopped. Order Service shutting down.")

        engine.dispose()
        logger.info("Database engine disposed. Order Service shutting down.")


# Initialize FastAPI app
app = FastAPI(
    title="Order Service",
    description="Handles order placement and event publishing to Kafka.",
    version="1.0.0",
    lifespan=lifespan,
)

# Register API routes
app.include_router(router)
app.include_route(db_health_router)
