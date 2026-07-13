from community.app.dtos.received_email_dto import ReceivedEmailCommand, ReceivedEmailListResult, ReceivedEmailResult
from community.app.ports.input.received_email_use_case import ReceivedEmailUseCase
from community.app.ports.output.received_email_port import ReceivedEmailPort


class ReceivedEmailInteractor(ReceivedEmailUseCase):

    def __init__(self, repo: ReceivedEmailPort) -> None:
        self._repo = repo

    async def receive(self, command: ReceivedEmailCommand) -> ReceivedEmailResult:
        return await self._repo.save(command)

    async def list_all(self) -> ReceivedEmailListResult:
        return await self._repo.list_all()
