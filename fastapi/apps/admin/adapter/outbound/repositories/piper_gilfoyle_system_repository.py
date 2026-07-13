from sqlalchemy.ext.asyncio import AsyncSession

from admin.app.dtos.piper_gilfoyle_system_dto import GilfoyleSystemQuery, GilfoyleSystemResponse
from admin.app.ports.output.piper_gilfoyle_system_port import GilfoyleSystemPort


class GilfoyleSystemRepository(GilfoyleSystemPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def introduce_myself(self, query: GilfoyleSystemQuery) -> GilfoyleSystemResponse:
        return GilfoyleSystemResponse(id=query.id, name=query.name)
