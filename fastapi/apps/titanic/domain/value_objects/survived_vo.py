from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class SurvivalStatus:
    survived: Optional[bool]

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "SurvivalStatus":
        if raw is None or raw == "":
            return cls(survived=None)
        if raw == "1":
            return cls(survived=True)
        if raw == "0":
            return cls(survived=False)
        raise ValueError(f"파싱 실패: {raw!r}")

    @property
    def is_unknown(self) -> bool:
        return self.survived is None
