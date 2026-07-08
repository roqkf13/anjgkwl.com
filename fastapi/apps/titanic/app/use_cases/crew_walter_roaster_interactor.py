from typing import Any

from titanic.adapter.inbound.api.schemas.crew_walter_roaster_schema import WalterRoasterSchema
from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterQuery, WalterRoasterResponse
from titanic.app.ports.input.crew_walter_roaster_use_case import WalterRoasterUseCase
from titanic.app.ports.output.crew_walter_roaster_port import WalterRoasterPort


class WalterQuery:
    def __init__(self, repository) -> None:
        self.repository = repository

    async def list_paginated(self, page: int, page_size: int) -> dict[str, Any]:
        total, items = await self.repository.list_paginated(page, page_size)
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": items,
        }


class WalterRoasterInteractor(WalterRoasterUseCase):

    def __init__(self, repository: WalterRoasterPort) -> None:
        self.repository = repository
        self._train_set = None
        self._test_set = None

    async def introduce_myself(self, schema: WalterRoasterSchema) -> WalterRoasterResponse:
        return await self.repository.introduce_myself(WalterRoasterQuery(
            id=schema.id,
            name=schema.name,
        ))

    async def load(self) -> None:
        self._train_set = await self.repository.get_train_set()
        self._test_set = await self.repository.get_test_set()

    def get_train_set(self):
        return self._train_set

    def get_test_set(self):
        return self._test_set