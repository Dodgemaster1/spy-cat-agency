from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import Base


class MissionOrmModel(Base):
    __tablename__ = "mission"

    id: Mapped[int] = mapped_column(primary_key=True)
    cat_id: Mapped[int | None] = mapped_column(ForeignKey("spy_cat.id"), nullable=True)
    is_complete: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    targets: Mapped[list["TargetOrmModel"]] = relationship(back_populates="mission", cascade="all, delete-orphan")

    # Optional: Relationship back to cat
    # cat: Mapped["SpyCatOrmModel"] = relationship()

    def to_dict(self) -> dict[str, object]:
        d = super()._to_dict()
        d["targets"] = [t.to_dict() for t in self.targets]
        return d


class TargetOrmModel(Base):
    __tablename__ = "target"

    id: Mapped[int] = mapped_column(primary_key=True)
    mission_id: Mapped[int] = mapped_column(ForeignKey("mission.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_complete: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    mission: Mapped["MissionOrmModel"] = relationship(back_populates="targets")

    def to_dict(self) -> dict[str, object]:
        return super()._to_dict()
