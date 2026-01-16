from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    def __repr__(self) -> str:
        columns = [f"{column}={getattr(self, column.name)}" for column in self.__table__.columns]
        return f"<{self.__class__.__name__} {', '.join(columns)}>"

    def _to_dict(self) -> dict[str, object]:
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
