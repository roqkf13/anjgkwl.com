from __future__ import annotations

from abc import ABC, abstractmethod

from scout.app.dtos.game_detail_dto import PatchNoteDto


class SteamNewsRepository(ABC):
    @abstractmethod
    async def fetch_patch_notes(
        self, steam_app_id: int, *, count: int = 5
    ) -> list[PatchNoteDto]:
        ...
