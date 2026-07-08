from __future__ import annotations

from abc import ABC, abstractmethod

from scout.domain.entities.scout_patch_note_entity import ScoutPatchNoteEntity
from scout.domain.entities.scout_patch_translation_entity import ScoutPatchTranslationEntity


class ScoutPatchNoteDbRepository(ABC):
    @abstractmethod
    async def find_by_external_id(self, external_note_id: str) -> ScoutPatchNoteEntity | None: ...

    @abstractmethod
    async def find_translation(self, patch_note_id: int, locale: str) -> ScoutPatchTranslationEntity | None: ...

    @abstractmethod
    async def upsert_note(self, entity: ScoutPatchNoteEntity) -> ScoutPatchNoteEntity: ...

    @abstractmethod
    async def upsert_translation(self, entity: ScoutPatchTranslationEntity) -> ScoutPatchTranslationEntity: ...
