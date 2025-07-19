import logging
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from order.app.core.config import settings
from opentelemetry import trace

tracer = trace.get_tracer(__name__)
logger = logging.getLogger("db-session")

# Create async SQLAlchemy engine with asyncpg
engine = create_async_engine(settings.postgres_dsn, echo=True, future=True)

# Configure async session factory
SessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


# Dependency-injected session generator for FastAPI
async def get_session() -> AsyncSession:
    """
    Yields a new AsyncSession with OpenTelemetry tracing.
    """
    with tracer.start_as_current_span("db.session.create") as span:
        span.set_attribute("db.system", "postgresql")
        span.set_attribute("db.engine.echo", str(engine.echo))
        logger.debug("Creating async DB session")

    async with SessionLocal() as session:
        yield session
