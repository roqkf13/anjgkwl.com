"""테스트 하네스 추적 서사 로그 — 멀티 에이전트 저니를 콘솔에 일목요연하게 출력한다."""
from __future__ import annotations

from community.app.dtos.detective_watson_watcher_dto import InboundEvent, RoutingDecision


def log_journey_start(index: int, event: InboundEvent) -> None:
    print(f"\n{'=' * 60}")
    print(f"[EVENT #{index}] {event.channel} 채널 인입 — 발신자: {event.sender}")
    print(f'  메시지: "{event.message}"')


def log_watson_triage(decision: RoutingDecision) -> None:
    print(f"[WATSON] 1차 분류 완료 → 라우팅 결정: {decision.value}")


def log_holmes_result(result: str) -> None:
    print(f"[HOLMES] 자체 처리 완료 → {result}")


def log_escalation_result(result: str) -> None:
    print(f"[STAR_CRAFT → FAKER] 에스컬레이션 처리 완료 → {result}")


def log_journey_end() -> None:
    print(f"{'=' * 60}")
