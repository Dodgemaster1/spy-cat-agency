from pydantic import Field, field_validator

from src.models.base import BaseEntityModel


class CreateTargetModel(BaseEntityModel):
    name: str
    country: str
    notes: str | None = None
    is_complete: bool = False


class TargetModel(CreateTargetModel):
    id: int
    mission_id: int


class CreateMissionModel(BaseEntityModel):
    cat_id: int | None = None
    targets: list[CreateTargetModel] = Field(..., min_length=1, max_length=3)
    is_complete: bool = False

    @field_validator("targets")
    @classmethod
    def validate_targets_length(cls, v: list[CreateTargetModel]) -> list[CreateTargetModel]:
        max_targets_count = 3
        if not (1 <= len(v) <= max_targets_count):
            raise ValueError("A mission must have between 1 and 3 targets")
        return v


class MissionModel(BaseEntityModel):
    id: int
    cat_id: int | None
    is_complete: bool
    targets: list[TargetModel]


class UpdateTargetModel(BaseEntityModel):
    id: int  # target id
    notes: str | None = None
    is_complete: bool | None = None


class AssignCatModel(BaseEntityModel):
    mission_id: int
    cat_id: int
