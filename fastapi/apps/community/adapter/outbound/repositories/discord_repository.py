from community.app.dtos.discord_dto import DiscordQuery, DiscordResponse
from community.app.ports.output.discord_port import DiscordPort


class DiscordMemoryRepository(DiscordPort):

    async def introduce_myself(self, query: DiscordQuery) -> DiscordResponse:
        return DiscordResponse(id=query.id, name=query.name)
