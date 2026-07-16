from __future__ import annotations

from abc import ABC, abstractmethod

from community.app.dtos.detective_watson_watcher_dto import InboundEvent


class EscalationPolicyPort(ABC):
    """이벤트를 ontology(페이커)로 에스컬레이션할지 판단하는 교체 가능한 정책."""

    @abstractmethod
    def should_escalate(self, event: InboundEvent) -> bool:
        pass
