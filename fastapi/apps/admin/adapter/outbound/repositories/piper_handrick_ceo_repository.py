from sqlalchemy.ext.asyncio import AsyncSession

from admin.app.dtos.piper_handrick_ceo_dto import HandrickCeoQuery, HandrickCeoResponse
from admin.app.ports.output.piper_handrick_ceo_port import HandrickCeoPort


class HandrickCeoRepository(HandrickCeoPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def introduce_myself(self, query: HandrickCeoQuery) -> HandrickCeoResponse:
        return HandrickCeoResponse(id=query.id, name=query.name)
