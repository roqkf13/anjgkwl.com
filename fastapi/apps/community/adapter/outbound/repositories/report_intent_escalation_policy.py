from __future__ import annotations

from community.app.dtos.detective_watson_watcher_dto import InboundEvent
from community.app.ports.output.detective_watson_watcher_escalation_policy_port import EscalationPolicyPort

_REPORT_INTENT_KEYWORDS = ("보고서", "실적", "report")


class ReportIntentEscalationPolicy(EscalationPolicyPort):
    """중요 거래처 + 보고서/실적 요청 의도가 감지되면 에스컬레이션 대상으로 판단."""

    def should_escalate(self, event: InboundEvent) -> bool:
        wants_report = any(kw in event.message for kw in _REPORT_INTENT_KEYWORDS)
        return event.important_client and wants_report
