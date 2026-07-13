from fastapi import APIRouter, Depends

from admin.adapter.inbound.api.schemas.piper_dunn_coo_schema import DunnCooSchema
from admin.app.dtos.piper_dunn_coo_dto import DunnCooResponse
from admin.app.ports.input.piper_dunn_coo_use_case import DunnCooUseCase
from admin.dependencies.piper_dunn_coo_provider import get_dunn_coo_use_case

'''
재러드 던 (Jared Dunn)
Pied Piper COO. 이전 직장인 Hooli 출신으로 냉철한 비즈니스 감각과 진심 어린 따뜻함을 함께 가진 인물.
'''
dunn_coo_router = APIRouter(prefix="/dunn", tags=["dunn"])


@dunn_coo_router.get("/myself")
async def introduce_myself(
    dunn: DunnCooUseCase = Depends(get_dunn_coo_use_case),
) -> DunnCooResponse:

    return await dunn.introduce_myself(
        DunnCooSchema(
            id=2,
            name="재러드 던 (Jared Dunn)",
        )
    )
