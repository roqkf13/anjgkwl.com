from __future__ import annotations

from scout.adapter.outbound.orm.scout_patch_note_orm import ScoutPatchNoteOrm
from scout.adapter.outbound.orm.scout_patch_translation_orm import ScoutPatchTranslationOrm
from scout.adapter.outbound.orm.scout_patch_content_block_orm import ScoutPatchContentBlockOrm
from scout.domain.entities.scout_patch_note_entity import ScoutPatchNoteEntity
from scout.domain.entities.scout_patch_translation_entity import ScoutPatchTranslationEntity, ContentBlock
from scout.domain.value_objects.scout_patch_note_vo import ExternalNoteId, Locale, BlockType


class ScoutPatchNoteMapper:
    @staticmethod
    def to_entity(orm: ScoutPatchNoteOrm) -> ScoutPatchNoteEntity:
        return ScoutPatchNoteEntity(
            id=orm.id,
            game_id=orm.game_id,
            external_note_id=ExternalNoteId(orm.external_note_id),
            source_title=orm.source_title,
            source_summary=orm.source_summary,
            source_body=orm.source_body,
            image_urls=orm.image_urls or [],
            published_at=orm.published_at,
            source_url=orm.source_url,
        )

    @staticmethod
    def to_orm(entity: ScoutPatchNoteEntity, game_id: int) -> ScoutPatchNoteOrm:
        return ScoutPatchNoteOrm(
            game_id=game_id,
            external_note_id=entity.external_note_id.value,
            source_title=entity.source_title,
            source_summary=entity.source_summary,
            source_body=entity.source_body,
            image_urls=entity.image_urls or None,
            published_at=entity.published_at,
            source_url=entity.source_url,
        )

    @staticmethod
    def to_translation_entity(
        orm: ScoutPatchTranslationOrm,
        blocks_list: list[ScoutPatchContentBlockOrm],
    ) -> ScoutPatchTranslationEntity:
        sorted_blocks = sorted(blocks_list, key=lambda b: b.sort_order)
        content_blocks = [
            ContentBlock(
                block_type=BlockType(b.block_type),
                text=b.text,
                url=b.url,
            )
            for b in sorted_blocks
        ]
        return ScoutPatchTranslationEntity(
            id=orm.id,
            patch_note_id=orm.patch_note_id,
            locale=Locale(orm.locale),
            translated_title=orm.translated_title,
            translated_summary=orm.translated_summary,
            translated_body=orm.translated_body,
            image_urls=orm.image_urls or [],
            content_blocks=content_blocks,
            translated_at=orm.translated_at,
        )

    @staticmethod
    def to_translation_orm(entity: ScoutPatchTranslationEntity) -> ScoutPatchTranslationOrm:
        return ScoutPatchTranslationOrm(
            patch_note_id=entity.patch_note_id,
            locale=entity.locale.value,
            translated_title=entity.translated_title,
            translated_summary=entity.translated_summary,
            translated_body=entity.translated_body,
            image_urls=entity.image_urls or None,
            translated_at=entity.translated_at,
        )

    @staticmethod
    def to_content_block_orms(
        entity: ScoutPatchTranslationEntity,
        translation_id: int,
    ) -> list[ScoutPatchContentBlockOrm]:
        return [
            ScoutPatchContentBlockOrm(
                translation_id=translation_id,
                sort_order=i,
                block_type=block.block_type.value,
                text=block.text,
                url=block.url,
            )
            for i, block in enumerate(entity.content_blocks)
        ]
