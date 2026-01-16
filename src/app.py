from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.dependencies.container import async_container
from src.routers.initialization import include_routers


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:  # noqa: RUF029, ARG001
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        debug=False,
        lifespan=lifespan,
    )
    setup_dishka(container=async_container, app=app)

    include_routers(app)

    return app
