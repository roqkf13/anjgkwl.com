from dataclasses import dataclass
from enum import Enum


class RoutingDecision(str, Enum):
    HOLMES = "holmes"
    ONTOLOGY_ESCALATION = "ontology_escalation"


@dataclass(frozen=True)
class InboundEvent:
    channel: str
    sender: str
    important_client: bool
    message: str
