"""Watson Test Harness — 멀티 에이전트 라우팅(Watson→Holmes / Watson→StarCraft→Faker) 검증 진입점."""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[4]
_APPS = _ROOT / "apps"
for _p in (_ROOT, _APPS):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from sherlock_homes.app.dtos.detective_watson_watcher_dto import RoutingDecision
from sherlock_homes.app.use_cases.holmes_general_inquiry_interactor import handle_general_inquiry
from sherlock_homes.dependencies.detective_watson_watcher_provider import get_watson_watcher_interactor
from sherlock_homes.tests.harness import narrative_logger as log
from sherlock_homes.tests.harness.mock_event_generator import generate_mock_events
from star_craft.app.use_cases.faker_escalation_interactor import escalate_to_faker


def run() -> None:
    watson = get_watson_watcher_interactor()
    events = generate_mock_events()

    for i, event in enumerate(events, start=1):
        log.log_journey_start(i, event)
        decision = watson.triage(event)
        log.log_watson_triage(decision)

        if decision is RoutingDecision.HOLMES:
            result = handle_general_inquiry(sender=event.sender, message=event.message)
            log.log_holmes_result(result)
        else:
            result = escalate_to_faker(sender=event.sender, message=event.message)
            log.log_escalation_result(result)

        log.log_journey_end()


if __name__ == "__main__":
    run()
