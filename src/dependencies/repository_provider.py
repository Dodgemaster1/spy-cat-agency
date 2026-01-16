from dishka import Provider, Scope, provide
from sqlalchemy.orm import Session, sessionmaker

from src.repository.cat import SpyCatRepository
from src.repository.mission import MissionRepository


class RepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def spy_cat_repository(self, session_maker: sessionmaker[Session]) -> SpyCatRepository:
        return SpyCatRepository(session_maker)

    @provide(scope=Scope.REQUEST)
    def mission_repository(self, session_maker: sessionmaker[Session]) -> MissionRepository:
        return MissionRepository(session_maker)
