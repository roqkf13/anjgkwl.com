from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class JasonRepository(ABC):
    @abstractmethod
    async def find_by_email(self, email: str) -> dict[str, Any] | None:
        """이메일로 사용자를 조회합니다. 없으면 None."""
