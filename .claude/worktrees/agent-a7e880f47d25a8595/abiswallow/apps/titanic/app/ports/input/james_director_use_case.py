from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class JamesDirectorUseCase(ABC):

    @abstractmethod
    async def receive_uploaded_records(
        self, records: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """CSV 업로드 후 저장."""
        ...

    @abstractmethod
    async def list_passengers(self, page: int, page_size: int) -> dict[str, Any]:
        """저장된 승객 목록 페이지 조회."""
        ...
