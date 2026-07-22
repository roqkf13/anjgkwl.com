from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class JasonUseCase(ABC):
    @abstractmethod
    async def login(self, email: str, password: str) -> dict[str, Any]:
        """이메일·비밀번호로 로그인합니다."""
