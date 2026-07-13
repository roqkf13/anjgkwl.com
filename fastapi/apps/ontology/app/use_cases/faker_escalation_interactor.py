"""온톨로지 버스 — Case B(에스컬레이션 업무)를 페이커(EXAONE)에게 격상 전달한다."""
from __future__ import annotations

import logging

from core.lol.t1_mid_faker_orchestrator import generate_reply_exaone

logger = logging.getLogger(__name__)

_FAKER_SYSTEM_PROMPT = (
    "당신은 전사 ERP 데이터를 취합해 최종 보고서를 작성하는 최고 관리자 AI, 페이커입니다. "
    "간결하게 한국어로 답하세요."
)


def escalate_to_faker(*, sender: str, message: str) -> str:
    logger.info("[STAR_CRAFT] 온톨로지 버스 이벤트 발행 → 페이커 웨이크업 (sender=%s)", sender)
    try:
        return generate_reply_exaone(message=message, system=_FAKER_SYSTEM_PROMPT)
    except Exception as e:
        logger.warning("[FAKER] EXAONE 호출 실패, 모의 응답으로 대체: %s", e)
        return f"[MOCK] {sender}님의 요청에 대한 분기 실적 보고서를 생성했습니다 (EXAONE 모델 미가동으로 모의 응답)."
