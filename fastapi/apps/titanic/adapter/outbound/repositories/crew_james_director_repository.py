from __future__ import annotations

import logging

logger = logging.getLogger(__name__)
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.orm.passenger_rose_model_strategies import RoseModelOrm as BookingOrm
from titanic.adapter.outbound.orm.passenger_jack_trainer_orm import JackTrainerOrm as PersonOrm
from titanic.app.dtos.crew_james_director_dto import BookingCommand, JamesDirectorQuery, JamesDirectorResponse, PassengerCommand
from titanic.app.ports.output.crew_james_director_port import JamesDirectorPort


class JamesDirectorRepository(JamesDirectorPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: JamesDirectorQuery) -> JamesDirectorResponse:
        logger.info(f"[JamesDirectorRepository] introduce_myself 진입 | request_data={query}")
        return JamesDirectorResponse(
            id=query.id * 10000,
            name= query.name + "가 레포지토리에 다녀옴"
        )

    async def receive_uploaded_records(
        self,
        person_commands: list[PassengerCommand],
        booking_commands: list[BookingCommand],
    ) -> int:
        # passengers upsert (중복 passenger_id 시 전체 필드 업데이트)
        person_values = [
            {
                "passenger_id": cmd.passenger_id,
                "name": cmd.name,
                "gender": cmd.gender,
                "age": cmd.age,
                "sib_sp": cmd.sib_sp,
                "parch": cmd.parch,
                "survived": cmd.survived,
            }
            for cmd in person_commands
        ]
        person_stmt = pg_insert(PersonOrm).values(person_values)
        person_stmt = person_stmt.on_conflict_do_update(
            index_elements=["passenger_id"],
            set_={
                "name": person_stmt.excluded.name,
                "gender": person_stmt.excluded.gender,
                "age": person_stmt.excluded.age,
                "sib_sp": person_stmt.excluded.sib_sp,
                "parch": person_stmt.excluded.parch,
                "survived": person_stmt.excluded.survived,
            },
        )
        await self.session.execute(person_stmt)
        await self.session.flush()

        # bookings upsert (중복 passenger_id 시 전체 필드 업데이트)
        booking_values = [
            {
                "passenger_id": cmd_p.passenger_id,
                "pclass": cmd_b.pclass,
                "ticket": cmd_b.ticket,
                "fare": cmd_b.fare,
                "cabin": cmd_b.cabin,
                "embarked": cmd_b.embarked,
            }
            for cmd_p, cmd_b in zip(person_commands, booking_commands)
        ]
        booking_stmt = pg_insert(BookingOrm).values(booking_values)
        booking_stmt = booking_stmt.on_conflict_do_update(
            index_elements=["passenger_id"],
            set_={
                "pclass": booking_stmt.excluded.pclass,
                "ticket": booking_stmt.excluded.ticket,
                "fare": booking_stmt.excluded.fare,
                "cabin": booking_stmt.excluded.cabin,
                "embarked": booking_stmt.excluded.embarked,
            },
        )
        await self.session.execute(booking_stmt)
        await self.session.commit()

        return len(booking_values)