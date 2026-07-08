from __future__ import annotations

from fastapi import APIRouter

andrews_blueprint_router = APIRouter(prefix="/titanic/andrews", tags=["andrews_blueprint"])

_BLUEPRINT_COLUMNS = [
    {"field": "PassengerId", "alias": "passenger_id", "description": "승객 식별자"},
    {"field": "Survived", "alias": "survived", "description": "생존 여부 (0=사망, 1=생존)"},
    {"field": "Pclass", "alias": "pclass", "description": "객실 등급 (1, 2, 3)"},
    {"field": "Name", "alias": "name", "description": "승객 이름"},
    {"field": "gender", "alias": "gender", "description": "성별"},
    {"field": "Age", "alias": "age", "description": "나이"},
    {"field": "Sib_Sp", "alias": "sib_sp", "description": "동승 형제·배우자 수"},
    {"field": "Parch", "alias": "parch", "description": "동승 부모·자녀 수"},
    {"field": "Ticket", "alias": "ticket", "description": "티켓 번호"},
    {"field": "Fare", "alias": "fare", "description": "운임"},
    {"field": "Cabin", "alias": "cabin", "description": "객실"},
    {"field": "Embarked", "alias": "embarked", "description": "승선 항구 (C, Q, S)"},
]


@andrews_blueprint_router.get("/blueprint")
async def get_andrews_blueprint():
    """설계도(Andrews) — 타이타닉 데이터셋 컬럼 구조."""
    return {
        "title": "Titanic dataset blueprint",
        "table": "titanic_passengers",
        "columns": _BLUEPRINT_COLUMNS,
    }
