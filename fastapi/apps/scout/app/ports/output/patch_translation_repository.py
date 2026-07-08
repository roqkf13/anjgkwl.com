from __future__ import annotations

from abc import ABC, abstractmethod

from scout.app.dtos.game_detail_dto import PatchNoteDto


class PatchTranslationRepository(ABC):
    @abstractmethod
    def load(self, note_id: str) -> PatchNoteDto | None:
        ...

    @abstractmethod
    def save(self, note: PatchNoteDto) -> None:
        ...
