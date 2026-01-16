from dishka import Provider, Scope, provide
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.config.db import DB_CONFIG


class SyncDBProvider(Provider):
    @provide(scope=Scope.APP)
    def engine(self) -> Engine:
        return create_engine(
            url=DB_CONFIG.url(),
            echo=False,
        )

    @provide(scope=Scope.APP)
    def session_maker(self, engine: Engine) -> sessionmaker[Session]:
        return sessionmaker(engine)
