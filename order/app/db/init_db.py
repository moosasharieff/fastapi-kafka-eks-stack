import logging
from sqlmodel import SQLModel
from opentelemetry import trace

from order.app.db.session import engine

logger = logging.getLogger("db-init")
tracer = trace.get_tracer(__name__)


def create_db() -> None:
    """
    Create all database tables based on SQLModel metadata.

    This should be called once during application setup or migrations.
    """
    with tracer.start_as_current_span("db.create_all") as span:
        try:
            SQLModel.metadata.create_all(engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error("Failed to create database tables.", exc_info=True)
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
            raise
