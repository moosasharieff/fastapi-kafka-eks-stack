import logging
from fastapi import APIRouter, Depends
from sqlmodel import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from order.app.db.session import get_session

router = APIRouter()
logger = logging.getLogger("db-health")


@router.get("/db_health", tags=["Health"])
async def db_health_check(session: AsyncSession = Depends(get_session)):
    """
    Health check endpoint to verify PostgreSQL connectivity.

    Returns:
        dict: {'status': 'ok'} if the DB is reachable, else {'status': 'db_unreachable'}
    """
    try:
        await session.execute(text("SELECT 1"))
        logger.info("DB health check passed.")
        return {"status": "ok"}
    except SQLAlchemyError as e:
        logger.error(f"DB health check failed: {e}", exc_info=True)
        return {"status": "db_unreachable"}
