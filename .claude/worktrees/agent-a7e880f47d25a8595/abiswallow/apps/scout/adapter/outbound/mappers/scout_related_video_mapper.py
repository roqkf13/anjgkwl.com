from __future__ import annotations

from scout.adapter.outbound.orm.scout_related_video_orm import ScoutRelatedVideoOrm
from scout.domain.entities.scout_related_video_entity import ScoutRelatedVideoEntity


class ScoutRelatedVideoMapper:
    @staticmethod
    def to_entity(orm: ScoutRelatedVideoOrm) -> ScoutRelatedVideoEntity:
        return ScoutRelatedVideoEntity(
            id=orm.id,
            game_id=orm.game_id,
            title=orm.title,
            channel=orm.channel,
            published_at=orm.published_at,
            watch_url=orm.watch_url,
        )

    @staticmethod
    def to_orm(entity: ScoutRelatedVideoEntity, game_id: int) -> ScoutRelatedVideoOrm:
        return ScoutRelatedVideoOrm(
            game_id=game_id,
            title=entity.title,
            channel=entity.channel,
            published_at=entity.published_at,
            watch_url=entity.watch_url,
        )
