from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException, status
from loguru import logger
from sqlalchemy import text
from sqlalchemy.orm import Session, sessionmaker

from src.utils.typedicts import HealthcheckTypeDict

healthcheck_router = APIRouter(prefix="/healthcheck", tags=["healthcheck"], route_class=DishkaRoute)


@healthcheck_router.get("/app", status_code=status.HTTP_200_OK)
async def health_app() -> HealthcheckTypeDict:
    try:
        return {"status": "ok", "msg": "Application is healthy"}
    except Exception as e:
        logger.exception("Error in application health check")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE) from e


@healthcheck_router.get("/db", status_code=status.HTTP_200_OK)
async def health_db(session_maker: FromDishka[sessionmaker[Session]]) -> HealthcheckTypeDict:
    try:
        with session_maker() as session:
            session.execute(text("SELECT 1"))
        return {"status": "ok", "msg": "Database connection is healthy"}
    except Exception as e:
        logger.exception("Error in db health check")
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE) from e
