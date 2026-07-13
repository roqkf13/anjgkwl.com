from __future__ import annotations

from abc import ABC, abstractmethod

from community.app.dtos.discord_dto import DiscordQuery, DiscordResponse


class DiscordUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, query: DiscordQuery) -> DiscordResponse:
        pass
