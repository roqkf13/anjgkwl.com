"""홈즈(Holmes) — Case A(일반 업무)를 자체적으로 소화해 처리·종결한다."""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def handle_general_inquiry(*, sender: str, message: str) -> str:
    logger.info("[HOLMES] %s 로부터의 일반 문의 자체 처리: %s", sender, message)
    return f"{sender}님, 문의 주신 내용 확인했습니다. 홈즈가 직접 응대하여 처리를 종결합니다."
