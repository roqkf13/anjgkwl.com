# 명단 수집(ingestion) 바운디드 컨텍스트의 집계 루트.
# 업로드된 CSV 한 줄 = 승객 신원 + 예매 정보. 동일성은 PassengerId 로만 판단한다.
from __future__ import annotations

from typing import Optional

from titanic.domain.value_objects.passenger_jack_trainer_vo import (
    Age,
    FamilyComposition,
    Gender,
    Name,
    PassengerId,
    SurvivalStatus,
)
from titanic.domain.value_objects.crew_james_director_vo import Booking, blank_to_none


class ManifestEntry:
    """승객 명단 한 줄을 표현하는 집계 루트."""

    def __init__(
        self,
        passenger_id: PassengerId,
        name: Name,
        gender: Gender,
        family: FamilyComposition,
        booking: Booking,
        age: Optional[Age] = None,
        survival: Optional[SurvivalStatus] = None,
    ) -> None:
        self._id = passenger_id
        self._name = name
        self._gender = gender
        self._family = family
        self._booking = booking
        self._age = age
        self._survival = survival

    @classmethod
    def from_raw(
        cls,
        *,
        passenger_id: str,
        name: str,
        gender: str,
        sib_sp: str,
        parch: str,
        age: str,
        survived: str,
        pclass: str,
        ticket: str,
        fare: str,
        cabin: str,
        embarked: str,
    ) -> "ManifestEntry":
        """원천 문자열(한 행)로부터 도메인 불변식을 강제하며 집계를 생성한다."""
        age_raw = blank_to_none(age)
        survived_raw = blank_to_none(survived)
        return cls(
            passenger_id=PassengerId(passenger_id),
            name=Name(name),
            gender=Gender.from_raw(gender),
            family=FamilyComposition.from_raw(
                blank_to_none(sib_sp) or "0",
                blank_to_none(parch) or "0",
            ),
            booking=Booking.from_raw(
                pclass=pclass, ticket=ticket, fare=fare, cabin=cabin, embarked=embarked
            ),
            age=Age.from_raw(age_raw) if age_raw else None,
            survival=SurvivalStatus.from_raw(survived_raw) if survived_raw else None,
        )

    @property
    def id(self) -> PassengerId:
        return self._id

    @property
    def name(self) -> Name:
        return self._name

    @property
    def gender(self) -> Gender:
        return self._gender

    @property
    def family(self) -> FamilyComposition:
        return self._family

    @property
    def booking(self) -> Booking:
        return self._booking

    @property
    def age(self) -> Optional[Age]:
        return self._age

    @property
    def survival(self) -> Optional[SurvivalStatus]:
        return self._survival

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ManifestEntry):
            return NotImplemented
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

    def __repr__(self) -> str:
        return f"ManifestEntry(id={self._id.value!r}, name={self._name.value!r})"
