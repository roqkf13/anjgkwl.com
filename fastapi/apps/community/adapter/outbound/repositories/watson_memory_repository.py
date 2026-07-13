from community.app.dtos.detective_watson_executor_dto import WatsonExecutorQuery, WatsonExecutorResponse
from community.app.ports.output.detective_watson_executor_port import WatsonExecutorPort


class WatsonMemoryRepository(WatsonExecutorPort):

    async def introduce_myself(self, query: WatsonExecutorQuery) -> WatsonExecutorResponse:
        return WatsonExecutorResponse(id=query.id, name=query.name)
