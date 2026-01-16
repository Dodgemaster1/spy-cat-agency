from src.models.mission import (
    AssignCatModel,
    CreateMissionModel,
    MissionModel,
    TargetModel,
    UpdateTargetModel,
)
from src.repository.mission import MissionRepository


class MissionService:
    def __init__(self, repository: MissionRepository) -> None:
        self._repository = repository

    def create_mission(self, mission: CreateMissionModel) -> MissionModel:
        return self._repository.create(mission)

    def read_mission(self, mission_id: int) -> MissionModel | None:
        return self._repository.read(mission_id)

    def read_all_missions(self) -> list[MissionModel]:
        return self._repository.read_all()

    def delete_mission(self, mission_id: int) -> None:
        result = self._repository.delete(mission_id)
        if result is False:  # Explicitly check False for not found
            # If repository raises ValueError for assigned, it bubbles up.
            # If simple False (not found)
            raise ValueError("Mission not found")

    def update_target(self, target: UpdateTargetModel) -> TargetModel:
        result = self._repository.update_target(target)
        if result is None:
            raise ValueError("Target not found")
        return result

    def assign_cat(self, assign_data: AssignCatModel) -> MissionModel:
        result = self._repository.assign_cat(assign_data)
        if result is None:
            raise ValueError("Mission not found")
        return result
