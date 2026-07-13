from __future__ import annotations

from community.app.dtos.discord_dto import DiscordQuery, DiscordResponse
from community.app.ports.input.discord_use_case import DiscordUseCase
from community.app.ports.output.discord_port import DiscordPort


class DiscordInteractor(DiscordUseCase):

    def __init__(self, repository: DiscordPort):
        self.repository = repository

    async def introduce_myself(self, query: DiscordQuery) -> DiscordResponse:
        return await self.repository.introduce_myself(query)
