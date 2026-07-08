from fastapi import APIRouter

from vision.adapter.inbound.api.v1.vision_router import vision_upload_router

vision_router = APIRouter(prefix="/vision", tags=["vision"])
vision_router.include_router(vision_upload_router)
