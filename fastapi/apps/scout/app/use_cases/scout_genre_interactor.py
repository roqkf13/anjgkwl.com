from __future__ import annotations

from scout.app.dtos.scout_genre_dto import ScoutGenreDto
from scout.app.ports.input.scout_genre_use_case import ScoutGenreUseCase
from scout.app.ports.output.scout_genre_db_repository import ScoutGenreDbRepository
from scout.domain.entities.scout_genre_entity import ScoutGenreEntity


def _to_dto(entity: ScoutGenreEntity) -> ScoutGenreDto:
    return ScoutGenreDto(
        id=entity.id,
        slug=entity.slug.value,
        label=entity.label.value,
        description=entity.description,
        traits=entity.traits,
        representative_game_id=entity.representative_game_id,
    )


class ScoutGenreInteractor(ScoutGenreUseCase):
    def __init__(self, repository: ScoutGenreDbRepository) -> None:
        self._repository = repository

    async def list_genres(self) -> list[ScoutGenreDto]:
        return [_to_dto(e) for e in await self._repository.find_all()]

    async def get_genre(self, slug: str) -> ScoutGenreDto | None:
        entity = await self._repository.find_by_slug(slug)
        return _to_dto(entity) if entity else None
