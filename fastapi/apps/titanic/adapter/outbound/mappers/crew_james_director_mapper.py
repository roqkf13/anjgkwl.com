# 도메인 집계(ManifestEntry) ↔ 영속성(ORM) 변환.
# 신원은 passenger 테이블(JackTrainerOrm), 예매는 bookings 테이블(RoseModelOrm)에 매핑한다.
from __future__ import annotations

from typing import Optional

from titanic.adapter.outbound.orm.passenger_jack_trainer_orm import JackTrainerOrm as PersonOrm
from titanic.adapter.outbound.orm.passenger_rose_model_strategies import RoseModelOrm as BookingOrm
from titanic.domain.entities.crew_james_director_entity import ManifestEntry
from titanic.domain.value_objects.passenger_jack_trainer_vo import Age


def _age_to_str(age: Optional[Age]) -> Optional[str]:
    if age is None:
        return None
    value = age.value
    return str(int(value)) if value.is_integer() else str(value)


class JamesDirectorMapper:
    @staticmethod
    def to_person_orm(entry: ManifestEntry) -> PersonOrm:
        return PersonOrm(
            passenger_id=int(entry.id.value),
            name=entry.name.value,
            gender=entry.gender.value,
            age=_age_to_str(entry.age),
            sib_sp=entry.family.siblings_spouses,
            parch=entry.family.parents_children,
            survived=entry.survival.value if entry.survival is not None else None,
        )

    @staticmethod
    def to_person_values(entry: ManifestEntry) -> dict:
        return {
            "passenger_id": int(entry.id.value),
            "name": entry.name.value,
            "gender": entry.gender.value,
            "age": _age_to_str(entry.age),
            "sib_sp": entry.family.siblings_spouses,
            "parch": entry.family.parents_children,
            "survived": entry.survival.value if entry.survival is not None else None,
        }

    @staticmethod
    def to_booking_orm(entry: ManifestEntry, person_id: int) -> BookingOrm:
        booking = entry.booking
        return BookingOrm(
            person_id=person_id,
            pclass=str(booking.ticket_class.value) if booking.ticket_class else None,
            ticket=booking.ticket.value if booking.ticket else None,
            fare=str(booking.fare.value) if booking.fare else None,
            cabin=booking.cabin.value if booking.cabin else None,
            embarked=booking.port.value if booking.port else None,
        )

    @staticmethod
    def to_booking_values(entry: ManifestEntry, person_id: int) -> dict:
        booking = entry.booking
        return {
            "person_id": person_id,
            "pclass": str(booking.ticket_class.value) if booking.ticket_class else None,
            "ticket": booking.ticket.value if booking.ticket else None,
            "fare": str(booking.fare.value) if booking.fare else None,
            "cabin": booking.cabin.value if booking.cabin else None,
            "embarked": booking.port.value if booking.port else None,
        }
