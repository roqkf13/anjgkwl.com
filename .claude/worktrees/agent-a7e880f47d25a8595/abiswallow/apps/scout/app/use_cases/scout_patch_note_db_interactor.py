from __future__ import annotations

from scout.app.ports.input.scout_patch_note_db_use_case import ScoutPatchNoteDbUseCase
from scout.app.ports.output.scout_patch_note_db_repository import ScoutPatchNoteDbRepository
from scout.domain.entities.scout_patch_note_entity import ScoutPatchNoteEntity
from scout.domain.entities.scout_patch_translation_entity import ScoutPatchTranslationEntity


class ScoutPatchNoteDbInteractor(ScoutPatchNoteDbUseCase):
    def __init__(self, repository: ScoutPatchNoteDbRepository) -> None:
        self._repository = repository

    async def sync_patch_note(self, entity: ScoutPatchNoteEntity) -> ScoutPatchNoteEntity:
        return await self._repository.upsert_note(entity)

    async def sync_translation(self, entity: ScoutPatchTranslationEntity) -> ScoutPatchTranslationEntity:
        return await self._repository.upsert_translation(entity)
