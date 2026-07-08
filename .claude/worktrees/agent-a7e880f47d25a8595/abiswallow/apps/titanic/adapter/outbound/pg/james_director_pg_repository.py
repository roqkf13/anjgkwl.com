from __future__ import annotations

from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from titanic.adapter.outbound.orm.booking_orm import Booking
from titanic.adapter.outbound.orm.person_orm import Person
from titanic.app.dtos.james_director_dto import (
    BookingCommand,
    PersonCommand,
    commands_from_upload_record,
)
from titanic.app.ports.output.james_director_repository import JamesDirectorRepository


class JamesDirectorPgRepository(JamesDirectorRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save_all(self, records: list[dict[str, Any]]) -> int:
        rows: list[tuple[PersonCommand, BookingCommand]] = []
        for record in records:
            pair = commands_from_upload_record(record)
            if pair is not None:
                rows.append(pair)

        if not rows:
            return 0

        passenger_ids = [person_cmd.passenger_id for person_cmd, _ in rows]
        existing_result = await self._session.execute(
            select(Person).where(Person.passenger_id.in_(passenger_ids))
        )
        existing_by_id = {
            person.passenger_id: person for person in existing_result.scalars().all()
        }

        for person_cmd, _booking_cmd in rows:
            person = existing_by_id.get(person_cmd.passenger_id)
            if person is None:
                person = Person(
                    passenger_id=person_cmd.passenger_id,
                    name=person_cmd.name,
                    gender=person_cmd.gender,
                    age=person_cmd.age,
                    sib_sp=person_cmd.sib_sp,
                    parch=person_cmd.parch,
                    survived=person_cmd.survived,
                )
                self._session.add(person)
                existing_by_id[person_cmd.passenger_id] = person
            else:
                person.name = person_cmd.name
                person.gender = person_cmd.gender
                person.age = person_cmd.age
                person.sib_sp = person_cmd.sib_sp
                person.parch = person_cmd.parch
                person.survived = person_cmd.survived

        await self._session.flush()

        for person_cmd, booking_cmd in rows:
            self._session.add(
                Booking(
                    passenger_id=person_cmd.passenger_id,
                    pclass=booking_cmd.pclass,
                    ticket=booking_cmd.ticket,
                    fare=booking_cmd.fare,
                    cabin=booking_cmd.cabin,
                    embarked=booking_cmd.embarked,
                )
            )

        await self._session.commit()
        return len(rows)

    async def list_paginated(
        self, page: int, page_size: int
    ) -> tuple[int, list[dict[str, Any]]]:
        total_result = await self._session.execute(
            select(func.count()).select_from(Person)
        )
        total = int(total_result.scalar_one())

        rows_result = await self._session.execute(
            select(Person, Booking)
            .join(Booking, Booking.passenger_id == Person.passenger_id)
            .order_by(Person.passenger_id, Booking.id)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        items = []
        for person, booking in rows_result.all():
            items.append(
                {
                    "id": booking.id,
                    "passenger_id": person.passenger_id,
                    "survived": person.survived,
                    "pclass": booking.pclass,
                    "name": person.name,
                    "gender": person.gender,
                    "age": person.age,
                    "sib_sp": person.sib_sp,
                    "parch": person.parch,
                    "ticket": booking.ticket,
                    "fare": booking.fare,
                    "cabin": booking.cabin,
                    "embarked": booking.embarked,
                }
            )
        return total, items
