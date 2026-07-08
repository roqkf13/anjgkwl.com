from __future__ import annotations

import logging
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.orm.passenger_jack_trainer_orm import JackTrainerOrm as PersonOrm
from titanic.adapter.outbound.orm.passenger_rose_model_strategies import RoseModelOrm as BookingOrm
from titanic.app.dtos.passenger_cal_tester_dto import CalTesterQuery, CalTesterResponse

logger = logging.getLogger(__name__)


class CalTesterRepository:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: CalTesterQuery) -> CalTesterResponse:
        '''칼 테스터의 자기 소개 레포지토리 구현 메소드'''
        logger.info(f"[CalTesterRepository] introduce_myself 진입 | request_data={query}")
        return CalTesterResponse(
            id=query.id * 10000,
            name=query.name + "가 레포지토리에 다녀옴",
        )

    async def get_scoring_data(self) -> list[dict[str, Any]]:
        """교차검증 채점에 사용할 전체 승객 피처 데이터 조회."""
        rows = (
            await self.session.execute(
                select(PersonOrm, BookingOrm)
                .outerjoin(BookingOrm, BookingOrm.passenger_id == PersonOrm.passenger_id)
                .order_by(PersonOrm.passenger_id)
            )
        ).all()
        return [
            {
                "pclass":   booking.pclass if booking else None,
                "gender":   person.gender,
                "age":      person.age,
                "sibsp":    person.sib_sp,
                "parch":    person.parch,
                "fare":     booking.fare if booking else None,
                "survived": person.survived,
            }
            for person, booking in rows
        ]