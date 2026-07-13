import csv
from io import StringIO

from typing import Literal

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile

from community.adapter.inbound.api.schemas.detective_watson_executor_schema import (
    WatsonExecutorSchema,
    WatsonSendEmailRequest,
)
from community.adapter.inbound.api.schemas.juso_schema import ContactItemSchema, ContactListSchema, ContactRowSchema, ContactUploadResultSchema
from community.app.dtos.detective_watson_executor_dto import (
    WatsonExecutorQuery,
    WatsonExecutorResponse,
    WatsonSendEmailQuery,
    WatsonSendEmailResult,
)
from community.app.ports.input.detective_watson_executor_use_case import WatsonExecutorUseCase
from community.app.ports.input.juso_use_case import JusoUseCase
from community.dependencies.detective_watson_executor_provider import get_watson_executor_interactor
from community.dependencies.juso_provider import get_juso_use_case

watson_executor_router = APIRouter(prefix="/watson", tags=["watson"])


@watson_executor_router.post("/introduce", response_model=WatsonExecutorResponse)
async def introduce_myself(
    schema: WatsonExecutorSchema,
    use_case: WatsonExecutorUseCase = Depends(get_watson_executor_interactor),
) -> WatsonExecutorResponse:
    query = WatsonExecutorQuery(id=schema.id, name=schema.name)
    return await use_case.introduce_myself(query)


@watson_executor_router.post("/send-email", response_model=WatsonSendEmailResult)
async def send_email(
    schema: WatsonSendEmailRequest,
    use_case: WatsonExecutorUseCase = Depends(get_watson_executor_interactor),
) -> WatsonSendEmailResult:
    query = WatsonSendEmailQuery(to=schema.to, prompt=schema.prompt, from_account=schema.from_account)
    return await use_case.send_email(query)


@watson_executor_router.get("/contacts", response_model=ContactListSchema, summary="주소록 목록 조회")
async def list_contacts(
    juso: JusoUseCase = Depends(get_juso_use_case),
) -> ContactListSchema:
    result = await juso.list_contacts()
    return ContactListSchema(
        total=result.total,
        contacts=[ContactItemSchema(**vars(c)) for c in result.contacts],
    )


@watson_executor_router.post("/contacts/upload", response_model=ContactUploadResultSchema, summary="Google 연락처 CSV 업로드")
async def upload_contacts(
    file: UploadFile = File(...),
    mode: Literal["replace", "upsert"] = Query("replace", description="replace: 전체 교체 / upsert: 누적 추가"),
    juso: JusoUseCase = Depends(get_juso_use_case),
) -> ContactUploadResultSchema:
    rows = _parse_csv((await file.read()).decode("utf-8", errors="replace"))
    commands = [r.to_command() for r in rows]
    if mode == "upsert":
        result = await juso.upsert_contacts(commands)
    else:
        result = await juso.upload_contacts(commands)
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
