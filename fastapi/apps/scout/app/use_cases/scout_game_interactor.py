from __future__ import annotations

from scout.app.dtos.scout_game_dto import ScoutGameDto
from scout.app.ports.input.scout_game_use_case import ScoutGameUseCase
from scout.app.ports.output.scout_game_db_repository import ScoutGameDbRepository
from scout.domain.entities.scout_game_entity import ScoutGameEntity


def _to_dto(entity: ScoutGameEntity) -> ScoutGameDto:
    return ScoutGameDto(
        id=entity.id,
        steam_app_id=entity.steam_app_id.value,
        title=entity.title.value,
        summary=entity.summary,
        genre_id=entity.genre_id,
        official_site_url=entity.official_site_url,
    )


class ScoutGameInteractor(ScoutGameUseCase):
    def __init__(self, repository: ScoutGameDbRepository) -> None:
        self._repository = repository

    async def get_game(self, steam_app_id: int) -> ScoutGameDto | None:
        entity = await self._repository.find_by_steam_app_id(steam_app_id)
        return _to_dto(entity) if entity else None

    async def list_games_by_genre(self, genre_id: int) -> list[ScoutGameDto]:
        return [_to_dto(e) for e in await self._repository.find_by_genre_id(genre_id)]
