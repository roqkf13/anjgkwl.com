from dataclasses import dataclass


@dataclass(frozen=True)
class ContentModerationQuery:
    subject: str | None
    body: str | None


@dataclass(frozen=True)
class ContentModerationResult:
    is_clean: bool
    label: str
    score: float
