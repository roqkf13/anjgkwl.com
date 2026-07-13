from dataclasses import dataclass


@dataclass(frozen=True)
class DiscordQuery:
    id: int
    name: str


@dataclass(frozen=True)
class DiscordResponse:
    id: int
    name: str
