from __future__ import annotations

from typing import Any

from titanic.adapter.inbound.api.schemas.james_director_schema import (
    JamesDirectorRecordSchema,
)
from titanic.app.ports.input.james_director_use_case import JamesDirectorUseCase
from titanic.app.ports.output.james_director_repository import JamesDirectorRepository


class JamesDirectorInteractor(JamesDirectorUseCase):
    """업로드·조회 유스케이스."""

    def __init__(self, repository: JamesDirectorRepository) -> None:
        self._repository = repository

    async def receive_uploaded_records(
        self, records: list[dict[str, Any]]
    ) -> dict[str, Any]:
        schema_rows = [JamesDirectorRecordSchema(**record) for record in records]
        persist_rows = [row.model_dump() for row in schema_rows]

        saved = await self._repository.save_all(persist_rows)
        return {
            "count": len(schema_rows),
            "records": schema_rows[:5],
            "stored_count": saved,
            "message": f"{saved}건을 저장했습니다.",
        }

    async def list_passengers(self, page: int, page_size: int) -> dict[str, Any]:
        total, items = await self._repository.list_paginated(page, page_size)
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": items,
        }
