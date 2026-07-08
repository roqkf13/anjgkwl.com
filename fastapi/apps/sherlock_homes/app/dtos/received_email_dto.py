from dataclasses import dataclass


@dataclass
class ReceivedEmailCommand:
    gmail_id: str
    thread_id: str | None
    from_: str | None
    to: str | None
    subject: str | None
    snippet: str | None


@dataclass
class ReceivedEmailResult:
    id: str
    gmail_id: str
    thread_id: str | None
    from_: str | None
    to: str | None
    subject: str | None
    snippet: str | None


@dataclass
class ReceivedEmailListResult:
    total: int
    emails: list[ReceivedEmailResult]
