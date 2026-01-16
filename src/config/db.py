from typing import Annotated, Final

from pydantic import Field, PostgresDsn

from src.config.base import BaseApplicationConfig


class DbConfig(BaseApplicationConfig):
    username: Annotated[str, Field(alias="POSTGRES_USER")]
    password: Annotated[str, Field(alias="POSTGRES_PASSWORD")]
    db_name: Annotated[str, Field(alias="POSTGRES_DB")] = "postgres"
    host: Annotated[str, Field(alias="POSTGRES_HOST")] = "localhost"
    port: Annotated[int, Field(alias="POSTGRES_PORT")] = 5432

    def url(self) -> str:
        return self._build_dsn("postgresql+psycopg")

    def _build_dsn(self, scheme: str) -> str:
        return str(
            PostgresDsn.build(
                scheme=scheme,
                username=self.username,
                password=self.password,
                host=self.host,
                port=self.port,
                path=self.db_name,
            ),
        )


DB_CONFIG: Final = DbConfig()
