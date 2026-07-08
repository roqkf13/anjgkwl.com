"""가상 이벤트 생성기 — police_lestrade_telegram / police_anderson_discord 인입을 모사한다."""
from __future__ import annotations

from sherlock_homes.app.dtos.detective_watson_watcher_dto import InboundEvent


def generate_mock_events() -> list[InboundEvent]:
    return [
        InboundEvent(
            channel="Telegram (police_lestrade_telegram_router)",
            sender="일반 거래처 홍길동",
            important_client=False,
            message="안녕하세요, 제품 배송 일정이 궁금해서 문의드립니다.",
        ),
        InboundEvent(
            channel="Discord (police_anderson_discord_router)",
            sender="VIP 거래처 어반테크",
            important_client=True,
            message="분기 실적 자동 보고서 발행 요망합니다.",
        ),
    ]
