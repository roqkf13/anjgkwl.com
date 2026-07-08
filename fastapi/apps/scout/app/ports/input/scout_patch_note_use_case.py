from __future__ import annotations

from abc import ABC, abstractmethod

from scout.app.dtos.scout_patch_note_dto import ScoutPatchNoteDto


class ScoutPatchNoteUseCase(ABC):
    @abstractmethod
    async def get_patch_note(self, external_note_id: str) -> ScoutPatchNoteDto | None: ...
