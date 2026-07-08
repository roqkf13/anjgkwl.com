from __future__ import annotations

from abc import ABC, abstractmethod

from scout.app.dtos.game_detail_dto import PatchNoteDto


class PatchNoteTranslator(ABC):
    @abstractmethod
    async def translate(self, note: PatchNoteDto, *, body_en: str) -> PatchNoteDto:
        ...
