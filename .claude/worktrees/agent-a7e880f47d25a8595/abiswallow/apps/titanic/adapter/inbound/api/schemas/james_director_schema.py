from __future__ import annotations

from pydantic import BaseModel, Field


class JamesDirectorRecordSchema(BaseModel):
    """CSV 업로드·정규화 후 승객 한 행."""

    passenger_id: str = ""
    survived: str = ""
    pclass: str = ""
    name: str = ""
    gender: str = ""
    age: str = ""
    sib_sp: str = ""
    parch: str = ""
    ticket: str = ""
    fare: str = ""
    cabin: str = ""
    embarked: str = ""

class JamesDirectorItemSchema(BaseModel):
    """DB에 저장된 승객 한 행."""

    id: int
    passenger_id: str | None = None
    survived: str | None = None
    pclass: str | None = None
    name: str | None = None
    gender: str | None = None
    age: str | None = None
    sib_sp: str | None = None
    parch: str | None = None
    ticket: str | None = None
    fare: str | None = None
    cabin: str | None = None
    embarked: str | None = None


class JamesDirectorListResponse(BaseModel):
    """GET /titanic/james_director/passengers 응답."""

    total: int
    page: int
    page_size: int = Field(..., serialization_alias="pageSize")
    items: list[JamesDirectorItemSchema]

    model_config = {"populate_by_name": True}


class JamesDirectorUploadResponse(BaseModel):
    """POST /titanic/james_director/upload 응답."""

    count: int
    records: list[JamesDirectorRecordSchema]
    stored_count: int = Field(..., serialization_alias="storedCount")
    message: str

    model_config = {"populate_by_name": True}
