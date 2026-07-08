from __future__ import annotations

from abc import ABC, abstractmethod

from scout.app.dtos.game_detail_dto import GameDetailDto, PatchNoteDto


class GameDetailRepository(ABC):
    @abstractmethod
    async def get_detail(self, steam_app_id: int) -> GameDetailDto | None:
        ...

    @abstractmethod
    def resolve_title(self, steam_app_id: int) -> str | None:
        ...

    @abstractmethod
    def get_fallback_patch_notes(self, steam_app_id: int) -> list[PatchNoteDto]:
        ...
