from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class PamelaUseCase(ABC):
    @abstractmethod
    async def signup(
        self,
        *,
        name: str,
        email: str,
        password: str,
        password_confirm: str,
        role: str,
    ) -> dict[str, Any]:
        ...
