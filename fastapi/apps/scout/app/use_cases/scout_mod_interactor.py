from __future__ import annotations

from scout.app.dtos.scout_mod_dto import ScoutModDto
from scout.app.ports.input.scout_mod_use_case import ScoutModUseCase
from scout.app.ports.output.scout_mod_db_repository import ScoutModDbRepository
from scout.domain.entities.scout_mod_entity import ScoutModEntity


def _to_dto(entity: ScoutModEntity) -> ScoutModDto:
    return ScoutModDto(
        id=entity.id,
        game_id=entity.game_id,
        mod_kind=entity.mod_kind.value,
        name=entity.name,
        author=entity.author,
        summary=entity.summary,
        characters=[c.value for c in entity.characters],
        source=entity.source.value if entity.source else None,
        source_url=entity.source_url,
        external_mod_id=entity.external_mod_id.value if entity.external_mod_id else None,
    )


class ScoutModInteractor(ScoutModUseCase):
    def __init__(self, repository: ScoutModDbRepository) -> None:
        self._repository = repository

    async def list_mods_by_game(self, game_id: int) -> list[ScoutModDto]:
        return [_to_dto(e) for e in await self._repository.find_by_game_id(game_id)]
