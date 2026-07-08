from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SteamAppId:
    value: int

    def __post_init__(self) -> None:
        if self.value <= 0:
            raise ValueError(f"SteamAppId는 양수여야 합니다: {self.value}")

    def steam_store_url(self) -> str:
        return f"https://store.steampowered.com/app/{self.value}"


@dataclass(frozen=True, slots=True)
class GameTitle:
    value: str

    def __post_init__(self) -> None:
        cleaned = (self.value or "").strip()
        if not cleaned:
            raise ValueError("GameTitle은 비어 있을 수 없습니다.")
        object.__setattr__(self, "value", cleaned)
