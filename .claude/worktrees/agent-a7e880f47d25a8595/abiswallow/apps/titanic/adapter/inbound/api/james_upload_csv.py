"""James CSV 업로드 — 무상태 파싱·정규화 (HTTP 없음)."""

from __future__ import annotations

import csv
from io import StringIO
from typing import Any

from titanic.adapter.inbound.api.schemas.james_director_schema import (
    JamesDirectorRecordSchema,
)

_ALLOWED_CONTENT_TYPES = frozenset(
    {"text/csv", "application/vnd.ms-excel", "text/plain"}
)


class CsvUploadError(Exception):
    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(detail)


def normalize_titanic_row(row: dict) -> dict:
    normalized: dict = {}
    for raw_key, value in row.items():
        if raw_key is None:
            continue
        key = raw_key.strip()
        lower_key = key.lower()
        if lower_key == "sex":
            normalized["gender"] = value
        elif lower_key == "passengerid":
            normalized["passenger_id"] = value
        elif lower_key == "sibsp":
            normalized["sib_sp"] = value
        elif lower_key in {
            "survived",
            "pclass",
            "name",
            "age",
            "parch",
            "ticket",
            "fare",
            "cabin",
            "embarked",
            "gender",
        }:
            normalized[lower_key] = value
        else:
            normalized[key] = value
    return normalized


def parse_titanic_csv_text(text: str) -> list[JamesDirectorRecordSchema]:
    if not text.strip():
        raise CsvUploadError("빈 CSV 파일입니다.")

    reader = csv.DictReader(StringIO(text))
    if reader.fieldnames is None:
        raise CsvUploadError("CSV 헤더를 읽을 수 없습니다.")

    return [
        JamesDirectorRecordSchema(**normalize_titanic_row(row)) for row in reader
    ]


def parse_titanic_upload(
    *,
    content_type: str | None,
    raw: bytes,
) -> list[JamesDirectorRecordSchema]:
    if content_type not in _ALLOWED_CONTENT_TYPES:
        raise CsvUploadError("CSV 파일을 업로드해주세요.")

    text = raw.decode("utf-8", errors="replace")
    return parse_titanic_csv_text(text)


def records_to_dicts(
    records: list[JamesDirectorRecordSchema],
) -> list[dict[str, Any]]:
    return [record.model_dump() for record in records]
