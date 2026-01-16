from sqlalchemy import delete, update
from sqlalchemy.orm import Session, sessionmaker

from src.db.models.cat import SpyCatOrmModel
from src.models.cat import CreateSpyCatModel, SpyCatModel, UpdateSpyCatModel


class SpyCatRepository:
    def __init__(self, session_maker: sessionmaker[Session]) -> None:
        self.session_maker = session_maker

    def create(self, create_cat_model: CreateSpyCatModel) -> SpyCatModel:
        cat = SpyCatOrmModel(**create_cat_model.model_dump())
        with self.session_maker.begin() as session:
            session.add(cat)
            session.flush()
            session.refresh(cat)
            return SpyCatModel(**cat.to_dict())

    def read(self, cat_id: int) -> SpyCatModel | None:
        with self.session_maker.begin() as session:
            cat = session.get(SpyCatOrmModel, cat_id)
            if not cat:
                return None  # Service will handle not found
            return SpyCatModel(**cat.to_dict())

    def read_all(self) -> list[SpyCatModel]:
        with self.session_maker.begin() as session:
            cats = session.query(SpyCatOrmModel).all()
            return [SpyCatModel(**cat.to_dict()) for cat in cats]

    def update(self, update_cat_model: UpdateSpyCatModel) -> SpyCatModel | None:
        cat_id = update_cat_model.id
        update_data = update_cat_model.model_dump(exclude_unset=True, exclude={"id"})

        # Only salary can be updated as per requirements "Ability to update spy cats' information (Salary)"
        # But wait, usually UpdateModel only has allowed fields.
        # My UpdateSpyCatModel only has salary. So unsafe dump is fine if model is strict.

        stmt = update(SpyCatOrmModel).where(SpyCatOrmModel.id == cat_id).values(**update_data).returning(SpyCatOrmModel)
        with self.session_maker.begin() as session:
            result = session.execute(stmt)
            if (cat := result.scalar_one_or_none()) is None:
                return None
            return SpyCatModel(**cat.to_dict())

    def delete(self, cat_id: int) -> bool:
        stmt = delete(SpyCatOrmModel).where(SpyCatOrmModel.id == cat_id)
        with self.session_maker.begin() as session:
            result = session.execute(stmt)
            return result.rowcount > 0
