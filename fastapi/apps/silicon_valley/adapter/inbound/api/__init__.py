from fastapi import APIRouter

from silicon_valley.adapter.inbound.api.v1.piper_handrick_ceo_router import handrick_ceo_router
from silicon_valley.adapter.inbound.api.v1.piper_dunn_coo_router import dunn_coo_router
from silicon_valley.adapter.inbound.api.v1.piper_dinesh_dash_router import dinesh_dash_router
from silicon_valley.adapter.inbound.api.v1.piper_gilfoyle_system_router import gilfoyle_system_router
from silicon_valley.adapter.inbound.api.v1.piper_bighetti_hr_router import bighetti_hr_router

silicon_valley_router = APIRouter(prefix="/silicon-valley", tags=["silicon-valley"])
silicon_valley_router.include_router(handrick_ceo_router)
silicon_valley_router.include_router(dunn_coo_router)
silicon_valley_router.include_router(dinesh_dash_router)
silicon_valley_router.include_router(gilfoyle_system_router)
silicon_valley_router.include_router(bighetti_hr_router)
