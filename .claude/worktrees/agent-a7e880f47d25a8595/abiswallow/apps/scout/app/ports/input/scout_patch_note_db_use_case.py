from __future__ import annotations

from abc import ABC, abstractmethod

from scout.domain.entities.scout_patch_note_entity import ScoutPatchNoteEntity
from scout.domain.entities.scout_patch_translation_entity import ScoutPatchTranslationEntity


class ScoutPatchNoteDbUseCase(ABC):
    @abstractmethod
    async def sync_patch_note(self, entity: ScoutPatchNoteEntity) -> ScoutPatchNoteEntity: ...

    @abstractmethod
    async def sync_translation(self, entity: ScoutPatchTranslationEntity) -> ScoutPatchTranslationEntity: ...
