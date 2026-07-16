from dataclasses import dataclass


@dataclass(frozen=True)
class RouteQueryCommand:
    text: str


@dataclass(frozen=True)
class RouteQueryResponse:
    route: str  # "auth" | "crud" | "rag" | "gemini"
    answer: str
    confidence: float
