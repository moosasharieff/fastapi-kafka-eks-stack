import logging
from sqlmodel import SQLModel
from opentelemetry import trace
from opentelemetry.trace import StatusCode

from order.app.db.session import engine

logger = logging.getLogger("db-init")
tracer = trace.get_tracer(__name__)


async def create_db() -> None:
    """
    Asynchronously create all database tables based on SQLModel metadata.
    This should be called once during application startup or migrations.
    """
    with tracer.start_as_current_span("db.create_all") as span:
        try:
            async with engine.begin() as conn:
                await conn.run_sync(SQLModel.metadata.create_all)
            logger.info("Database tables created successfully.")
        except Exception as e:
            logger.error("Failed to create database tables.", exc_info=True)
            span.set_status(StatusCode.ERROR, str(e))
            raise
