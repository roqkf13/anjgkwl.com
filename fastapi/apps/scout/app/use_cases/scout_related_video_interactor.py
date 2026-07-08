from __future__ import annotations

from scout.app.dtos.scout_related_video_dto import ScoutRelatedVideoDto
from scout.app.ports.input.scout_related_video_use_case import ScoutRelatedVideoUseCase
from scout.app.ports.output.scout_related_video_db_repository import ScoutRelatedVideoDbRepository
from scout.domain.entities.scout_related_video_entity import ScoutRelatedVideoEntity


def _to_dto(entity: ScoutRelatedVideoEntity) -> ScoutRelatedVideoDto:
    return ScoutRelatedVideoDto(
        id=entity.id,
        game_id=entity.game_id,
        title=entity.title,
        channel=entity.channel,
        watch_url=entity.watch_url,
        published_at=entity.published_at,
    )


class ScoutRelatedVideoInteractor(ScoutRelatedVideoUseCase):
    def __init__(self, repository: ScoutRelatedVideoDbRepository) -> None:
        self._repository = repository

    async def list_videos_by_game(self, game_id: int) -> list[ScoutRelatedVideoDto]:
        return [_to_dto(e) for e in await self._repository.find_by_game_id(game_id)]
