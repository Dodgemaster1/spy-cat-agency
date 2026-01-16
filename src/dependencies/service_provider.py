from dishka import Provider, Scope, provide

from src.repository.cat import SpyCatRepository
from src.repository.mission import MissionRepository
from src.services.cat import SpyCatService
from src.services.mission import MissionService


class ServiceProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_spy_cat_service(self, repository: SpyCatRepository) -> SpyCatService:
        return SpyCatService(repository)

    @provide(scope=Scope.REQUEST)
    def get_mission_service(self, repository: MissionRepository) -> MissionService:
        return MissionService(repository)
