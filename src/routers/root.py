from fastapi import APIRouter
from starlette import status
from starlette.responses import RedirectResponse

root_router = APIRouter()


@root_router.get("/", status_code=status.HTTP_307_TEMPORARY_REDIRECT, include_in_schema=False)
async def redirect_to_docs() -> RedirectResponse:
    return RedirectResponse("/docs", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
