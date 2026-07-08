from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from scout.adapter.outbound.orm.scout_genre_orm import ScoutGenreOrm
from scout.adapter.outbound.orm.scout_genre_trait_orm import ScoutGenreTraitOrm
from scout.adapter.outbound.mappers.scout_genre_mapper import ScoutGenreMapper
from scout.app.ports.output.scout_genre_db_repository import ScoutGenreDbRepository
from scout.domain.entities.scout_genre_entity import ScoutGenreEntity


class ScoutGenrePgRepository(ScoutGenreDbRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_slug(self, slug: str) -> ScoutGenreEntity | None:
        result = await self._session.execute(select(ScoutGenreOrm).where(ScoutGenreOrm.slug == slug))
        orm = result.scalar_one_or_none()
        if not orm:
            return None
        traits = await self._load_traits(orm.id)
        return ScoutGenreMapper.to_entity(orm, traits)

    async def find_all(self) -> list[ScoutGenreEntity]:
        result = await self._session.execute(select(ScoutGenreOrm))
        orms = result.scalars().all()
        entities = []
        for orm in orms:
            traits = await self._load_traits(orm.id)
            entities.append(ScoutGenreMapper.to_entity(orm, traits))
        return entities

    async def upsert(self, entity: ScoutGenreEntity) -> ScoutGenreEntity:
        result = await self._session.execute(
            select(ScoutGenreOrm).where(ScoutGenreOrm.slug == entity.slug.value)
        )
        existing = result.scalar_one_or_none()
        if existing:
            existing.label = entity.label.value
            existing.description = entity.description
            existing.representative_game_id = entity.representative_game_id
            genre_id = existing.id
        else:
            orm = ScoutGenreMapper.to_orm(entity)
            self._session.add(orm)
            await self._session.flush()
            genre_id = orm.id
        await self._session.execute(
            delete(ScoutGenreTraitOrm).where(ScoutGenreTraitOrm.genre_id == genre_id)
        )
        trait_orms = ScoutGenreMapper.to_trait_orms(entity, genre_id)
        self._session.add_all(trait_orms)
        await self._session.commit()
        return await self.find_by_slug(entity.slug.value)

    async def _load_traits(self, genre_id: int) -> list[ScoutGenreTraitOrm]:
        result = await self._session.execute(
            select(ScoutGenreTraitOrm).where(ScoutGenreTraitOrm.genre_id == genre_id)
        )
        return list(result.scalars().all())
