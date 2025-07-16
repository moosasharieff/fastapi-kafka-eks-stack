import logging
from sqlmodel import create_engine, Session
from order.app.core.config import settings
from opentelemetry import trace

tracer = trace.get_tracer(__name__)
logger = logging.getLogger("db-session")

engine = create_engine(settings.postgres_dsn, echo=True)


def get_session() -> Session:
    """
    Create a new SQLModel session with OpenTelemetry tracing.

    Returns:
        Session: A new database session.
    """
    with tracer.start_as_current_span("db.session.create") as span:
        span.set_attribute("db.system", "postgresql")
        span.set_attribute("db.engine.echo", str(engine.echo))
        logger.debug("Creating new DB session")
        return Session(engine)
