from __future__ import annotations

from abc import ABC, abstractmethod

from sherlock_homes.app.dtos.detective_watson_watcher_dto import InboundEvent, RoutingDecision


class WatsonWatcherUseCase(ABC):

    @abstractmethod
    def triage(self, event: InboundEvent) -> RoutingDecision:
        pass
