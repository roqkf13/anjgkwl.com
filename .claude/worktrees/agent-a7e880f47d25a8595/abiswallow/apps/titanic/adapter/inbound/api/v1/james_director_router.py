from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from titanic.adapter.inbound.api.james_upload_csv import (
    CsvUploadError,
    parse_titanic_upload,
    records_to_dicts,
)
from titanic.adapter.inbound.api.schemas.james_director_schema import (
    JamesDirectorUploadResponse,
)
from titanic.app.dependencies.james_director import get_james_director_use_case
from titanic.app.ports.input.james_director_use_case import JamesDirectorUseCase

james_director_router = APIRouter(prefix="/titanic/james", tags=["james"])


@james_director_router.post("/upload", response_model=JamesDirectorUploadResponse)
async def upload_titanic_file(
    file: UploadFile = File(...),
    use_case: JamesDirectorUseCase = Depends(get_james_director_use_case),
):
    """타이타닉 승객 CSV → Person/Booking 커맨드로 Neon 저장."""
    try:
        records = parse_titanic_upload(
            content_type=file.content_type,
            raw=await file.read(),
        )
    except CsvUploadError as exc:
        raise HTTPException(status_code=400, detail=exc.detail) from exc

    return await use_case.receive_uploaded_records(records_to_dicts(records))
