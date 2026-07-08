from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from scout.adapter.outbound.orm.scout_related_video_orm import ScoutRelatedVideoOrm
from scout.adapter.outbound.mappers.scout_related_video_mapper import ScoutRelatedVideoMapper
from scout.app.ports.output.scout_related_video_db_repository import ScoutRelatedVideoDbRepository
from scout.domain.entities.scout_related_video_entity import ScoutRelatedVideoEntity


class ScoutRelatedVideoPgRepository(ScoutRelatedVideoDbRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_game_id(self, game_id: int) -> list[ScoutRelatedVideoEntity]:
        result = await self._session.execute(
            select(ScoutRelatedVideoOrm).where(ScoutRelatedVideoOrm.game_id == game_id)
        )
        return [ScoutRelatedVideoMapper.to_entity(o) for o in result.scalars().all()]

    async def upsert(self, entity: ScoutRelatedVideoEntity) -> ScoutRelatedVideoEntity:
        result = await self._session.execute(
            select(ScoutRelatedVideoOrm).where(
                ScoutRelatedVideoOrm.game_id == entity.game_id,
                ScoutRelatedVideoOrm.watch_url == entity.watch_url,
            )
        )
        existing = result.scalar_one_or_none()
        if existing:
            existing.title = entity.title
            existing.channel = entity.channel
            existing.published_at = entity.published_at
        else:
            orm = ScoutRelatedVideoMapper.to_orm(entity, entity.game_id)
            self._session.add(orm)
        await self._session.commit()
        result2 = await self._session.execute(
            select(ScoutRelatedVideoOrm).where(
                ScoutRelatedVideoOrm.game_id == entity.game_id,
                ScoutRelatedVideoOrm.watch_url == entity.watch_url,
            )
        )
        return ScoutRelatedVideoMapper.to_entity(result2.scalar_one())
