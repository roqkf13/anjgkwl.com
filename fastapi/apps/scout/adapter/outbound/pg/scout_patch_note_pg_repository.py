from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from scout.adapter.outbound.orm.scout_patch_note_orm import ScoutPatchNoteOrm
from scout.adapter.outbound.orm.scout_patch_translation_orm import ScoutPatchTranslationOrm
from scout.adapter.outbound.orm.scout_patch_content_block_orm import ScoutPatchContentBlockOrm
from scout.adapter.outbound.mappers.scout_patch_note_mapper import ScoutPatchNoteMapper
from scout.app.ports.output.scout_patch_note_db_repository import ScoutPatchNoteDbRepository
from scout.domain.entities.scout_patch_note_entity import ScoutPatchNoteEntity
from scout.domain.entities.scout_patch_translation_entity import ScoutPatchTranslationEntity


class ScoutPatchNotePgRepository(ScoutPatchNoteDbRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_external_id(self, external_note_id: str) -> ScoutPatchNoteEntity | None:
        result = await self._session.execute(
            select(ScoutPatchNoteOrm).where(ScoutPatchNoteOrm.external_note_id == external_note_id)
        )
        orm = result.scalar_one_or_none()
        return ScoutPatchNoteMapper.to_entity(orm) if orm else None

    async def find_translation(self, patch_note_id: int, locale: str) -> ScoutPatchTranslationEntity | None:
        result = await self._session.execute(
            select(ScoutPatchTranslationOrm).where(
                ScoutPatchTranslationOrm.patch_note_id == patch_note_id,
                ScoutPatchTranslationOrm.locale == locale,
            )
        )
        t_orm = result.scalar_one_or_none()
        if not t_orm:
            return None
        blocks = await self._load_blocks(t_orm.id)
        return ScoutPatchNoteMapper.to_translation_entity(t_orm, blocks)

    async def upsert_note(self, entity: ScoutPatchNoteEntity) -> ScoutPatchNoteEntity:
        result = await self._session.execute(
            select(ScoutPatchNoteOrm).where(
                ScoutPatchNoteOrm.external_note_id == entity.external_note_id.value
            )
        )
        existing = result.scalar_one_or_none()
        if existing:
            existing.source_title = entity.source_title
            existing.source_summary = entity.source_summary
            existing.source_body = entity.source_body
            existing.image_urls = entity.image_urls or None
            existing.published_at = entity.published_at
            existing.source_url = entity.source_url
        else:
            orm = ScoutPatchNoteMapper.to_orm(entity, entity.game_id)
            self._session.add(orm)
        await self._session.commit()
        return await self.find_by_external_id(entity.external_note_id.value)

    async def upsert_translation(self, entity: ScoutPatchTranslationEntity) -> ScoutPatchTranslationEntity:
        result = await self._session.execute(
            select(ScoutPatchTranslationOrm).where(
                ScoutPatchTranslationOrm.patch_note_id == entity.patch_note_id,
                ScoutPatchTranslationOrm.locale == entity.locale.value,
            )
        )
        existing = result.scalar_one_or_none()
        if existing:
            existing.translated_title = entity.translated_title
            existing.translated_summary = entity.translated_summary
            existing.translated_body = entity.translated_body
            existing.image_urls = entity.image_urls or None
            existing.translated_at = entity.translated_at
            translation_id = existing.id
        else:
            t_orm = ScoutPatchNoteMapper.to_translation_orm(entity)
            self._session.add(t_orm)
            await self._session.flush()
            translation_id = t_orm.id
        await self._session.execute(
            delete(ScoutPatchContentBlockOrm).where(
                ScoutPatchContentBlockOrm.translation_id == translation_id
            )
        )
        block_orms = ScoutPatchNoteMapper.to_content_block_orms(entity, translation_id)
        self._session.add_all(block_orms)
        await self._session.commit()
        return await self.find_translation(entity.patch_note_id, entity.locale.value)

    async def _load_blocks(self, translation_id: int) -> list[ScoutPatchContentBlockOrm]:
        result = await self._session.execute(
            select(ScoutPatchContentBlockOrm)
            .where(ScoutPatchContentBlockOrm.translation_id == translation_id)
            .order_by(ScoutPatchContentBlockOrm.sort_order)
        )
        return list(result.scalars().all())
