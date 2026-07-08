from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from scout.adapter.outbound.orm.scout_mod_orm import ScoutModOrm
from scout.adapter.outbound.orm.scout_mod_character_orm import ScoutModCharacterOrm
from scout.adapter.outbound.mappers.scout_mod_mapper import ScoutModMapper
from scout.app.ports.output.scout_mod_db_repository import ScoutModDbRepository
from scout.domain.entities.scout_mod_entity import ScoutModEntity


class ScoutModPgRepository(ScoutModDbRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_game_id(self, game_id: int) -> list[ScoutModEntity]:
        result = await self._session.execute(
            select(ScoutModOrm).where(ScoutModOrm.game_id == game_id)
        )
        orms = result.scalars().all()
        entities = []
        for orm in orms:
            chars = await self._load_characters(orm.id)
            entities.append(ScoutModMapper.to_entity(orm, chars))
        return entities

    async def upsert(self, entity: ScoutModEntity) -> ScoutModEntity:
        result = await self._session.execute(
            select(ScoutModOrm).where(
                ScoutModOrm.game_id == entity.game_id,
                ScoutModOrm.external_mod_id == (entity.external_mod_id.value if entity.external_mod_id else None),
                ScoutModOrm.name == entity.name,
            )
        )
        existing = result.scalar_one_or_none()
        if existing:
            existing.mod_kind = entity.mod_kind.value
            existing.author = entity.author
            existing.summary = entity.summary
            existing.source = entity.source.value if entity.source else None
            existing.source_url = entity.source_url
            mod_id = existing.id
        else:
            orm = ScoutModMapper.to_orm(entity, entity.game_id)
            self._session.add(orm)
            await self._session.flush()
            mod_id = orm.id
        await self._session.execute(
            delete(ScoutModCharacterOrm).where(ScoutModCharacterOrm.mod_id == mod_id)
        )
        char_orms = ScoutModMapper.to_character_orms(entity, mod_id)
        self._session.add_all(char_orms)
        await self._session.commit()
        result2 = await self._session.execute(
            select(ScoutModOrm).where(ScoutModOrm.id == mod_id)
        )
        orm2 = result2.scalar_one()
        chars = await self._load_characters(mod_id)
        return ScoutModMapper.to_entity(orm2, chars)

    async def _load_characters(self, mod_id: int) -> list[ScoutModCharacterOrm]:
        result = await self._session.execute(
            select(ScoutModCharacterOrm).where(ScoutModCharacterOrm.mod_id == mod_id)
        )
        return list(result.scalars().all())
