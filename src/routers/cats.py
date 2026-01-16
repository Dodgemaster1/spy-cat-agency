from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException, status
from loguru import logger

from src.models.cat import CreateSpyCatModel, SpyCatModel, UpdateSpyCatModel
from src.services.cat import SpyCatService

cats_router = APIRouter(prefix="/cats", tags=["cats"], route_class=DishkaRoute)


@cats_router.get("", status_code=status.HTTP_200_OK)
def read_cats(service: FromDishka[SpyCatService]) -> list[SpyCatModel]:
    try:
        return service.read_all_cats()
    except Exception as e:
        logger.exception("Error reading all cats")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e


@cats_router.get("/{cat_id}", status_code=status.HTTP_200_OK)
def read_cat(cat_id: int, service: FromDishka[SpyCatService]) -> SpyCatModel:
    try:
        cat = service.read_cat(cat_id)
    except Exception as e:
        logger.exception("Error reading cat: id={}", cat_id)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e

    if not cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cat not found")
    return cat


@cats_router.post("", status_code=status.HTTP_201_CREATED)
def create_cat(cat: CreateSpyCatModel, service: FromDishka[SpyCatService]) -> SpyCatModel:
    try:
        return service.create_cat(cat)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception as e:
        logger.exception("Error creating cat")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e


@cats_router.patch("", status_code=status.HTTP_200_OK)
def update_cat(cat: UpdateSpyCatModel, service: FromDishka[SpyCatService]) -> SpyCatModel:
    try:
        updated_cat = service.update_cat(cat)
    except Exception as e:
        logger.exception("Error updating cat")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e

    if not updated_cat:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cat not found")
    return updated_cat


@cats_router.delete("/{cat_id}", status_code=status.HTTP_200_OK)
def delete_cat(cat_id: int, service: FromDishka[SpyCatService]) -> None:
    try:
        service.delete_cat(cat_id)
    except ValueError as e:
        if "not found" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cat not found") from e
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception as e:
        logger.exception("Error deleting cat: id={}", cat_id)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e
