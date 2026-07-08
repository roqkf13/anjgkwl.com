from sqlalchemy.ext.asyncio import AsyncSession

from silicon_valley.app.dtos.piper_handrick_ceo_dto import HandrickCeoQuery, HandrickCeoResponse
from silicon_valley.app.ports.output.piper_handrick_ceo_port import HandrickCeoPort


class HandrickCeoRepository(HandrickCeoPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def introduce_myself(self, query: HandrickCeoQuery) -> HandrickCeoResponse:
        return HandrickCeoResponse(id=query.id, name=query.name)
