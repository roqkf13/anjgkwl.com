"""왓슨(Watson) — 인바운드 이벤트 1차 분류(Triage) 및 라우팅 허브.

police_lestrade_telegram, police_anderson_discord 등 채널 어댑터로부터 이벤트를
낚아채어(Watch & Hook), 주입된 EscalationPolicyPort 목록으로 판단해
홈즈(자체 처리) 또는 star_craft 온톨로지 버스(페이커 에스컬레이션)로 라우팅한다.

정책(EscalationPolicyPort)을 교체·추가하는 것만으로 판단 기준을 확장할 수 있어
(예: 욕설/스팸 필터링 정책 추가) 트리아지 로직 자체는 수정하지 않아도 된다.
"""
from __future__ import annotations

from community.app.dtos.detective_watson_watcher_dto import InboundEvent, RoutingDecision
from community.app.ports.input.detective_watson_watcher_use_case import WatsonWatcherUseCase
from community.app.ports.output.detective_watson_watcher_escalation_policy_port import EscalationPolicyPort


class WatsonWatcherInteractor(WatsonWatcherUseCase):
    """Triage Nurse — 주입된 정책들을 순회하며 라우팅 결정을 내린다."""

    def __init__(self, escalation_policies: list[EscalationPolicyPort]) -> None:
        self._escalation_policies = escalation_policies

    def triage(self, event: InboundEvent) -> RoutingDecision:
        if any(policy.should_escalate(event) for policy in self._escalation_policies):
            return RoutingDecision.STAR_CRAFT_ESCALATION
        return RoutingDecision.HOLMES
