from sqlalchemy.orm import Session, joinedload, sessionmaker

from src.db.models.mission import MissionOrmModel, TargetOrmModel
from src.models.mission import AssignCatModel, CreateMissionModel, MissionModel, TargetModel, UpdateTargetModel


class MissionRepository:
    def __init__(self, session_maker: sessionmaker[Session]) -> None:
        self.session_maker = session_maker

    def create(self, create_mission_model: CreateMissionModel) -> MissionModel:
        mission_data = create_mission_model.model_dump(exclude={"targets"})
        targets_data = create_mission_model.targets

        # Check if cat is assigned and available
        cat_id = mission_data.get("cat_id")

        with self.session_maker.begin() as session:
            if cat_id is not None:
                existing_mission = (
                    session.query(MissionOrmModel)
                    .filter(MissionOrmModel.cat_id == cat_id, ~MissionOrmModel.is_complete)
                    .first()
                )
                if existing_mission:
                    raise ValueError("Cat is already assigned to an active mission")

            mission = MissionOrmModel(**mission_data)
            # Create Target ORM objects
            mission.targets = [TargetOrmModel(**t.model_dump()) for t in targets_data]

            session.add(mission)
            session.flush()
            session.refresh(mission)
            return MissionModel(**mission.to_dict())

    def read(self, mission_id: int) -> MissionModel | None:
        # Need to join targets
        with self.session_maker.begin() as session:
            mission = (
                session.query(MissionOrmModel)
                .options(joinedload(MissionOrmModel.targets))
                .filter(MissionOrmModel.id == mission_id)
                .first()
            )
            if not mission:
                return None
            return MissionModel(**mission.to_dict())

    def read_all(self) -> list[MissionModel]:
        with self.session_maker.begin() as session:
            missions = session.query(MissionOrmModel).options(joinedload(MissionOrmModel.targets)).all()
            return [MissionModel(**mission.to_dict()) for mission in missions]

    def delete(self, mission_id: int) -> bool:
        # Restriction check "cannot be deleted if already assigned" should ideally be in Service,
        # but to run atomically we can check here.
        with self.session_maker.begin() as session:
            mission = session.get(MissionOrmModel, mission_id)
            if not mission:
                return False  # Or raise specific error error

            if mission.cat_id is not None:
                raise ValueError("Mission is assigned to a cat")

            session.delete(mission)
            return True

    def update_target(self, update_target_model: UpdateTargetModel) -> TargetModel | None:
        target_id = update_target_model.id
        update_data = update_target_model.model_dump(exclude_unset=True, exclude={"id"})

        with self.session_maker.begin() as session:
            # We need to check restrictions: "Notes cannot be updated if either the target or the mission is completed"
            # So we need to fetch target and its mission first.
            target = (
                session.query(TargetOrmModel)
                .options(joinedload(TargetOrmModel.mission))
                .filter(TargetOrmModel.id == target_id)
                .first()
            )
            if not target:
                return None

            if "notes" in update_data and (target.is_complete or target.mission.is_complete):
                raise ValueError("Cannot update notes if target or mission is completed")

            # Apply updates
            for key, value in update_data.items():
                setattr(target, key, value)

            session.flush()
            session.refresh(target)

            # Additional check: "After completing all of the targets, the mission is marked as completed."
            # If we updated is_complete to True
            if update_data.get("is_complete") is True:
                # Check if all other targets are complete
                # target.mission.targets might be lazy loaded or stale. Refresh mission?
                # Since we serve from exact object and session, let's check.
                # Re-query all targets of the mission to be safe
                all_targets = session.query(TargetOrmModel).filter(TargetOrmModel.mission_id == target.mission_id).all()
                if all(t.is_complete for t in all_targets):
                    target.mission.is_complete = True
                    session.add(target.mission)

            # Re-refresh to get updated IDs if any? no.
            return TargetModel(**target.to_dict())

    def assign_cat(self, assign_model: AssignCatModel) -> MissionModel | None:
        with self.session_maker.begin() as session:
            mission = session.get(MissionOrmModel, assign_model.mission_id)
            if not mission:
                return None

            # Helper logic: "One cat can only have one mission at a time"
            # Check if cat is already assigned to an incomplete mission?
            # Existing missions where cat_id == new_cat_id and is_complete == False
            existing_mission = (
                session.query(MissionOrmModel)
                .filter(MissionOrmModel.cat_id == assign_model.cat_id, ~MissionOrmModel.is_complete)
                .first()
            )

            if existing_mission:
                raise ValueError("Cat is already assigned to an active mission")

            mission.cat_id = assign_model.cat_id
            session.add(mission)
            session.flush()
            session.refresh(mission)  # Refresh to get targets if needed, but we return MissionModel

            # We need to reload targets for to_dict() if they are not loaded
            # Use explicit query with eager load to be safe for return
            mission = (
                session.query(MissionOrmModel)
                .options(joinedload(MissionOrmModel.targets))
                .filter(MissionOrmModel.id == assign_model.mission_id)
                .first()
            )
            if mission is None:
                return None
            return MissionModel(**mission.to_dict())
