from __future__ import annotations

from abc import ABC, abstractmethod

from scout.app.dtos.game_detail_dto import ModDto


class ModRepository(ABC):
    @abstractmethod
    async def fetch_mods_for_game(
        self, steam_app_id: int, *, limit_per_kind: int = 8
    ) -> tuple[list[ModDto], list[ModDto]]:
        """게임별 모드를 (appearance, functional) 로 반환한다."""
