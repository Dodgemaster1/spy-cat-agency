from fastapi import FastAPI

from src.routers.cats import cats_router
from src.routers.healthcheck import healthcheck_router
from src.routers.missions import missions_router
from src.routers.root import root_router


def include_routers(app: FastAPI) -> None:
    app.include_router(root_router)
    app.include_router(cats_router)
    app.include_router(missions_router)
    app.include_router(healthcheck_router)
