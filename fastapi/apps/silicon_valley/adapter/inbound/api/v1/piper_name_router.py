from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

name_router = APIRouter(tags=["silicon-valley-v1"])

_CHARACTERS: dict[str, dict] = {
    "handrick": {"id": 1,  "name": "리처드 헨드릭스 (Richard Hendricks)", "role": "CEO"},
    "dunn":     {"id": 2,  "name": "재러드 던 (Jared Dunn)",              "role": "COO"},
    "dinesh":   {"id": 3,  "name": "디네시 추그타이 (Dinesh Chugtai)",     "role": "Dashboard"},
    "gilfoyle": {"id": 4,  "name": "버트람 길포일 (Bertram Gilfoyle)",     "role": "System"},
    "bighetti": {"id": 5,  "name": "넬슨 빅헤드 비게티 (Nelson Bighetti)", "role": "HR"},
}


class MyselfResponse(BaseModel):
    id: int
    name: str
    role: str


@name_router.get("/{name}/myself", response_model=MyselfResponse)
async def introduce_myself(name: str) -> MyselfResponse:
    character = _CHARACTERS.get(name)
    if character is None:
        raise HTTPException(status_code=404, detail=f"'{name}' 캐릭터를 찾을 수 없습니다. 가능한 이름: {list(_CHARACTERS)}")
    return MyselfResponse(**character)
