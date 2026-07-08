from __future__ import annotations

from scout.app.ports.input.scout_mod_db_use_case import ScoutModDbUseCase
from scout.app.ports.output.scout_mod_db_repository import ScoutModDbRepository
from scout.domain.entities.scout_mod_entity import ScoutModEntity


class ScoutModDbInteractor(ScoutModDbUseCase):
    def __init__(self, repository: ScoutModDbRepository) -> None:
        self._repository = repository

    async def get_mods_by_game(self, game_id: int) -> list[ScoutModEntity]:
        return await self._repository.find_by_game_id(game_id)

    async def sync_mod(self, entity: ScoutModEntity) -> ScoutModEntity:
        return await self._repository.upsert(entity)
