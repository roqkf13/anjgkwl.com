from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class PamelaRepository(ABC):
    @abstractmethod
    async def email_exists(self, email: str) -> bool:
        ...

    @abstractmethod
    async def create_user(
        self,
        *,
        name: str,
        email: str,
        password_hash: str,
        role: str,
    ) -> dict[str, Any]:
        ...
