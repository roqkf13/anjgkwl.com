from dataclasses import dataclass


@dataclass(frozen=True)
class RouteQueryCommand:
    text: str


@dataclass(frozen=True)
class RouteQueryResponse:
    route: str  # "rag" | "gemini"
    answer: str
    confidence: float
