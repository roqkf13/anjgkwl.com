from dataclasses import dataclass


@dataclass(frozen=True)
class HandrickCeoQuery:

    id: int
    name: str


@dataclass(frozen=True)
class HandrickCeoResponse:

    id: int
    name: str
