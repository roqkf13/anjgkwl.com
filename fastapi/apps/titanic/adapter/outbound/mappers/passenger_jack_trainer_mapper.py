from __future__ import annotations

from titanic.adapter.outbound.orm.passenger_jack_trainer_orm import JackTrainerOrm
from titanic.domain.entities.passenger_jack_trainer_entity import PassengerEntity
from titanic.domain.value_objects.passenger_jack_trainer_vo import (
    Age,
    FamilyRelation,
    Gender,
    PassengerId,
    PassengerName,
    SurvivalStatus,
)


class JackTrainerMapper:
    @staticmethod
    def to_entity(orm: JackTrainerOrm) -> PassengerEntity:
        return PassengerEntity(
            id=orm.id,
            passenger_id=PassengerId(orm.passenger_id) if orm.passenger_id else None,
            name=PassengerName(orm.name) if orm.name else None,
            gender=Gender.from_raw(orm.gender),
            age=Age.from_raw(orm.age),
            family_relation=FamilyRelation.from_raw(orm.sib_sp, orm.parch),
            survival_status=SurvivalStatus.from_raw(orm.survived),
        )

    @staticmethod
    def to_orm(entity: PassengerEntity) -> JackTrainerOrm:
        # JackTrainerOrm에는 'id' 컬럼이 없음 → TypeError 발생 (Red 테스트로 문서화됨)
        return JackTrainerOrm(
            id=entity.id,
            passenger_id=entity.passenger_id.value if entity.passenger_id else None,
            name=entity.name.full_name if entity.name else None,
            gender=entity.gender.value.value,
            age=str(entity.age.value) if not entity.age.is_unknown else None,
            sib_sp=str(entity.family_relation.sib_sp),
            parch=str(entity.family_relation.parch),
            survived=("1" if entity.survival_status.survived else "0") if not entity.survival_status.is_unknown else None,
        )
