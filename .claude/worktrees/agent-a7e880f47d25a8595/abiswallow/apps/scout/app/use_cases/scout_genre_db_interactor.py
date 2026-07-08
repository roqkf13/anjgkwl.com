from __future__ import annotations

from scout.app.ports.input.scout_genre_db_use_case import ScoutGenreDbUseCase
from scout.app.ports.output.scout_genre_db_repository import ScoutGenreDbRepository
from scout.domain.entities.scout_genre_entity import ScoutGenreEntity


class ScoutGenreDbInteractor(ScoutGenreDbUseCase):
    def __init__(self, repository: ScoutGenreDbRepository) -> None:
        self._repository = repository

    async def get_all_genres(self) -> list[ScoutGenreEntity]:
        return await self._repository.find_all()

    async def sync_genre(self, entity: ScoutGenreEntity) -> ScoutGenreEntity:
        return await self._repository.upsert(entity)
