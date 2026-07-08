from sherlock_homes.app.dtos.telegram_dto import TelegramQuery, TelegramResponse
from sherlock_homes.app.ports.output.telegram_port import TelegramPort


class TelegramMemoryRepository(TelegramPort):

    async def introduce_myself(self, query: TelegramQuery) -> TelegramResponse:
        return TelegramResponse(id=query.id, name=query.name)
