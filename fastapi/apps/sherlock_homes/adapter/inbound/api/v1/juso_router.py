import csv
from io import StringIO

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from sherlock_homes.adapter.inbound.api.schemas.juso_schema import (
    ContactRowSchema,
    ContactUploadResultSchema,
)
from sherlock_homes.app.dtos.juso_dto import JusoQuery, JusoResponse
from sherlock_homes.app.ports.input.juso_use_case import JusoUseCase
from sherlock_homes.dependencies.juso_provider import get_juso_use_case

juso_router = APIRouter(prefix="/juso", tags=["juso"])


@juso_router.get("/myself")
async def introduce_myself(
    juso: JusoUseCase = Depends(get_juso_use_case),
) -> JusoResponse:
    return await juso.introduce_myself(
        JusoQuery(id=14, name="주소 검색기 (Juso)")
    )


@juso_router.post("/upload", response_model=ContactUploadResultSchema, summary="Google 연락처 CSV 업로드")
async def upload_contacts(
    file: UploadFile = File(...),
    juso: JusoUseCase = Depends(get_juso_use_case),
) -> ContactUploadResultSchema:
    rows = _parse_csv((await file.read()).decode("utf-8", errors="replace"))
    result = await juso.upload_contacts([r.to_command() for r in rows])
    return ContactUploadResultSchema(
        total=result.total,
        contacts=[ContactRowSchema(**vars(c)) for c in result.contacts],
    )


def _parse_csv(text: str) -> list[ContactRowSchema]:
    if not text.strip():
        raise HTTPException(status_code=400, detail="빈 CSV 파일입니다.")
    reader = csv.DictReader(StringIO(text))
    if reader.fieldnames is None:
        raise HTTPException(status_code=400, detail="CSV 헤더를 읽을 수 없습니다.")
    return [ContactRowSchema(**_normalize_contact_row(row)) for row in reader]


def _normalize_contact_row(row: dict) -> dict:
    normalized = {}
    for raw_key, value in row.items():
        if raw_key is None:
            continue
        key = (
            raw_key.strip()
            .replace(" - ", "_")
            .replace(" ", "_")
            .replace("-", "_")
            .lower()
            .replace("__", "_")
        )
        normalized[key] = value or ""
    return normalized
