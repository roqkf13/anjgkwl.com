from __future__ import annotations

from abc import ABC, abstractmethod

from scout.app.dtos.game_detail_dto import GameDetailDto, PatchNoteDto


class GameDetailUseCase(ABC):
    @abstractmethod
    async def get_game_detail(self, steam_app_id: int) -> GameDetailDto | None:
        ...

    @abstractmethod
    async def translate_patch_note(
        self, steam_app_id: int, note_id: str
    ) -> PatchNoteDto | None:
        ...
