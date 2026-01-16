from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException, status
from loguru import logger

from src.models.mission import (
    AssignCatModel,
    CreateMissionModel,
    MissionModel,
    TargetModel,
    UpdateTargetModel,
)
from src.services.mission import MissionService

missions_router = APIRouter(prefix="/missions", tags=["missions"], route_class=DishkaRoute)


@missions_router.get("", status_code=status.HTTP_200_OK)
def read_missions(service: FromDishka[MissionService]) -> list[MissionModel]:
    try:
        return service.read_all_missions()
    except Exception as e:
        logger.exception("Error reading all missions")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e


@missions_router.get("/{mission_id}", status_code=status.HTTP_200_OK)
def read_mission(mission_id: int, service: FromDishka[MissionService]) -> MissionModel:
    try:
        mission = service.read_mission(mission_id)
    except Exception as e:
        logger.exception("Error reading mission: id={}", mission_id)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e

    if not mission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mission not found")
    return mission


@missions_router.post("", status_code=status.HTTP_201_CREATED)
def create_mission(mission: CreateMissionModel, service: FromDishka[MissionService]) -> MissionModel:
    try:
        return service.create_mission(mission)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception as e:
        logger.exception("Error creating mission")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e


@missions_router.delete("/{mission_id}", status_code=status.HTTP_200_OK)
def delete_mission(mission_id: int, service: FromDishka[MissionService]) -> None:
    try:
        service.delete_mission(mission_id)
    except ValueError as e:
        if "not found" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mission not found") from e
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception as e:
        logger.exception("Error deleting mission: id={}", mission_id)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e


@missions_router.patch("/targets", status_code=status.HTTP_200_OK)
def update_target(target: UpdateTargetModel, service: FromDishka[MissionService]) -> TargetModel:
    try:
        return service.update_target(target)
    except ValueError as e:
        # Check specific messages for 400 vs 404 if needed
        if "Target not found" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Target not found") from e
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception as e:
        logger.exception("Error updating target")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e


@missions_router.post("/assign", status_code=status.HTTP_200_OK)
def assign_cat(data: AssignCatModel, service: FromDishka[MissionService]) -> MissionModel:
    try:
        return service.assign_cat(data)
    except ValueError as e:
        if "Mission not found" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mission not found") from e
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    except Exception as e:
        logger.exception("Error assigning cat")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e
