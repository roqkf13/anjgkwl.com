from __future__ import annotations

from scout.app.ports.input.scout_game_db_use_case import ScoutGameDbUseCase
from scout.app.ports.output.scout_game_db_repository import ScoutGameDbRepository
from scout.domain.entities.scout_game_entity import ScoutGameEntity


class ScoutGameDbInteractor(ScoutGameDbUseCase):
    def __init__(self, repository: ScoutGameDbRepository) -> None:
        self._repository = repository

    async def get_game_by_steam_id(self, steam_app_id: int) -> ScoutGameEntity | None:
        return await self._repository.find_by_steam_app_id(steam_app_id)

    async def sync_game(self, entity: ScoutGameEntity) -> ScoutGameEntity:
        return await self._repository.upsert(entity)
