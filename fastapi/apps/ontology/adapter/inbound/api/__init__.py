from fastapi import APIRouter

from ontology.adapter.inbound.api.v1.vision_router import vision_upload_router
from ontology.adapter.inbound.api.v1.rag_router_router import rag_router_query_router

vision_router = APIRouter(prefix="/vision", tags=["vision"])
vision_router.include_router(vision_upload_router)

route_router = APIRouter(prefix="/route", tags=["route"])
route_router.include_router(rag_router_query_router)
