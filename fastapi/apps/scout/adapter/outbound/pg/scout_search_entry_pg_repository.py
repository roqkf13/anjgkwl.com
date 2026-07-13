from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert

from scout.adapter.outbound.orm.scout_search_entry_orm import ScoutSearchEntryOrm
from scout.adapter.outbound.mappers.scout_search_entry_mapper import (
    ScoutSearchEntryMapper,
)
from scout.app.ports.output.scout_search_entry_db_repository import (
    ScoutSearchEntryDbRepository,
)
from scout.domain.entities.scout_search_entry_entity import ScoutSearchEntryEntity


class ScoutSearchEntryPgRepository(ScoutSearchEntryDbRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_query_key(self, query_key: str) -> ScoutSearchEntryEntity | None:
        result = await self._session.execute(
            select(ScoutSearchEntryOrm).where(
                ScoutSearchEntryOrm.query_key == query_key
            )
        )
        orm = result.scalar_one_or_none()
        return ScoutSearchEntryMapper.to_entity(orm) if orm else None

    async def upsert(self, entity: ScoutSearchEntryEntity) -> ScoutSearchEntryEntity:
        stmt = pg_insert(ScoutSearchEntryOrm).values(
            query_key=entity.query_key,
            title=entity.title,
            platform=entity.platform,
            summary=entity.summary,
            official_site_url=entity.official_site_url,
            videos=entity.videos,
        ).on_conflict_do_update(
            index_elements=["query_key"],
            set_=dict(
                title=pg_insert(ScoutSearchEntryOrm).excluded.title,
                platform=pg_insert(ScoutSearchEntryOrm).excluded.platform,
                summary=pg_insert(ScoutSearchEntryOrm).excluded.summary,
                official_site_url=pg_insert(ScoutSearchEntryOrm).excluded.official_site_url,
                videos=pg_insert(ScoutSearchEntryOrm).excluded.videos,
            ),
        )
        await self._session.execute(stmt)
        await self._session.commit()
        return await self.find_by_query_key(entity.query_key)
