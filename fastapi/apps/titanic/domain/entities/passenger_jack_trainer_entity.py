from __future__ import annotations

from titanic.domain.value_objects.passenger_jack_trainer_vo import (
    Age, FamilyRelation, Gender, PassengerId, PassengerName, SurvivalStatus,
)


class PassengerEntity:
    def __init__(
        self,
        id: int,
        passenger_id: PassengerId | None,
        name: PassengerName | None,
        gender: Gender,
        age: Age,
        family_relation: FamilyRelation,
        survival_status: SurvivalStatus,
    ) -> None:
        self.id = id
        self.passenger_id = passenger_id
        self.name = name
        self.gender = gender
        self.age = age
        self.family_relation = family_relation
        self.survival_status = survival_status

    def is_high_risk(self) -> bool:
        return (
            not self.gender.is_female()
            and not self.age.is_minor
            and self.family_relation.is_alone
        )

    def has_family(self) -> bool:
        return not self.family_relation.is_alone

    def record_survival(self, survived: bool) -> None:
        self.survival_status = SurvivalStatus(survived=survived)

    @classmethod
    def from_orm(cls, orm) -> "PassengerEntity":
        return cls(
            id=orm.id,
            passenger_id=PassengerId(orm.passenger_id) if orm.passenger_id else None,
            name=PassengerName(orm.name) if orm.name else None,
            gender=Gender.from_raw(orm.gender),
            age=Age.from_raw(orm.age),
            family_relation=FamilyRelation.from_raw(orm.sib_sp, orm.parch),
            survival_status=SurvivalStatus.from_raw(orm.survived),
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PassengerEntity):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"PassengerEntity(id={self.id!r}, passenger_id={self.passenger_id!r})"
