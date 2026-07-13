import logging
import tempfile
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from star_craft.adapter.inbound.api.schemas.vision_schema import (
    FaceRecognitionResponseSchema,
    VisionUploadResponseSchema,
)
from star_craft.app.ports.input.face_recognition_use_case import FaceRecognitionUseCase
from star_craft.dependencies.face_recognition_provider import get_face_recognition_use_case

logger = logging.getLogger(__name__)

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png"}

vision_upload_router = APIRouter(tags=["vision"])


@vision_upload_router.post(
    "/upload",
    response_model=VisionUploadResponseSchema,
    summary="비전 처리용 이미지(jpg, png) 업로드",
)
async def upload_vision_image(file: UploadFile = File(...)) -> VisionUploadResponseSchema:
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="jpg, png 파일만 업로드할 수 있습니다.")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="빈 파일입니다.")

    logger.info(
        "[VisionRouter] received %s (%s, %d bytes)",
        file.filename,
        file.content_type,
        len(content),
    )

    return VisionUploadResponseSchema(
        filename=file.filename or "",
        content_type=file.content_type or "",
        size_bytes=len(content),
        message="이미지가 서버에 정상적으로 전달되었습니다.",
    )


@vision_upload_router.post(
    "/recognize-face",
    response_model=FaceRecognitionResponseSchema,
    summary="업로드한 얼굴 이미지가 누구인지 인식",
)
async def recognize_face(
    file: UploadFile = File(...),
    use_case: FaceRecognitionUseCase = Depends(get_face_recognition_use_case),
) -> FaceRecognitionResponseSchema:
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="jpg, png 파일만 업로드할 수 있습니다.")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="빈 파일입니다.")

    suffix = Path(file.filename or "").suffix or ".jpg"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(content)
        tmp_path = Path(tmp.name)

    try:
        result = use_case.recognize(tmp_path)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    finally:
        tmp_path.unlink(missing_ok=True)

    return FaceRecognitionResponseSchema(name=result.name, confidence=result.confidence)
