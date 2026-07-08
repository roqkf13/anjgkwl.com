from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert

from scout.adapter.outbound.orm.scout_game_orm import ScoutGameOrm
from scout.adapter.outbound.mappers.scout_game_mapper import ScoutGameMapper
from scout.app.ports.output.scout_game_db_repository import ScoutGameDbRepository
from scout.domain.entities.scout_game_entity import ScoutGameEntity


class ScoutGamePgRepository(ScoutGameDbRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_steam_app_id(self, steam_app_id: int) -> ScoutGameEntity | None:
        result = await self._session.execute(
            select(ScoutGameOrm).where(ScoutGameOrm.steam_app_id == steam_app_id)
        )
        orm = result.scalar_one_or_none()
        return ScoutGameMapper.to_entity(orm) if orm else None

    async def find_by_genre_id(self, genre_id: int) -> list[ScoutGameEntity]:
        result = await self._session.execute(
            select(ScoutGameOrm).where(ScoutGameOrm.genre_id == genre_id)
        )
        return [ScoutGameMapper.to_entity(o) for o in result.scalars().all()]

    async def upsert(self, entity: ScoutGameEntity) -> ScoutGameEntity:
        stmt = pg_insert(ScoutGameOrm).values(
            steam_app_id=entity.steam_app_id.value,
            genre_id=entity.genre_id,
            title=entity.title.value,
            summary=entity.summary,
            official_site_url=entity.official_site_url,
        ).on_conflict_do_update(
            index_elements=["steam_app_id"],
            set_=dict(
                genre_id=pg_insert(ScoutGameOrm).excluded.genre_id,
                title=pg_insert(ScoutGameOrm).excluded.title,
                summary=pg_insert(ScoutGameOrm).excluded.summary,
                official_site_url=pg_insert(ScoutGameOrm).excluded.official_site_url,
            ),
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return await self.find_by_steam_app_id(entity.steam_app_id.value)
