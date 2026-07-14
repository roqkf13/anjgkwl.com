from __future__ import annotations

import re

_CHUNK_SIZE = 800
_CHUNK_OVERLAP = 100

_INSERT_HEADER_RE = re.compile(
    r"INSERT\s+INTO\s+(\w+)\s*\(([^)]+)\)\s*VALUES",
    re.IGNORECASE,
)


def split_into_chunks(text: str, chunk_size: int = _CHUNK_SIZE, overlap: int = _CHUNK_OVERLAP) -> list[str]:
    """문서 텍스트를 겹치는 구간을 두고 고정 길이로 분할한다."""
    stripped = text.strip()
    if not stripped:
        return []

    chunks: list[str] = []
    start = 0
    length = len(stripped)
    while start < length:
        end = min(start + chunk_size, length)
        chunk = stripped[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == length:
            break
        start = end - overlap
    return chunks


def _split_top_level(raw: str) -> list[str]:
    """따옴표 안의 콤마/괄호는 무시하고, 최상위 콤마 기준으로 나눈다."""
    fields: list[str] = []
    depth = 0
    in_quote = False
    field_start = 0
    i = 0
    n = len(raw)
    while i < n:
        ch = raw[i]
        if in_quote:
            if ch == "'":
                if i + 1 < n and raw[i + 1] == "'":
                    i += 1  # 이스케이프된 '' 는 건너뜀
                else:
                    in_quote = False
        elif ch == "'":
            in_quote = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch == "," and depth == 0:
            fields.append(raw[field_start:i])
            field_start = i + 1
        i += 1
    fields.append(raw[field_start:])
    return [f.strip() for f in fields]


def _clean_value(value: str) -> str | None:
    v = value.strip()
    if v.upper() == "NULL" or v == "":
        return None
    v = re.sub(r"::\w+$", "", v).strip()  # '1984-06-05'::date 같은 캐스트 제거
    if v.startswith("'") and v.endswith("'") and len(v) >= 2:
        v = v[1:-1].replace("''", "'")
    return v or None


def _extract_insert_rows(text: str) -> list[tuple[str, list[str], str]]:
    """(table, columns, row_raw) 튜플 목록. row_raw는 괄호 안 원문."""
    rows: list[tuple[str, list[str], str]] = []
    for header in _INSERT_HEADER_RE.finditer(text):
        table = header.group(1)
        columns = [c.strip() for c in header.group(2).split(",")]
        body_start = header.end()
        stmt_end = text.find(";", body_start)
        body = text[body_start : stmt_end if stmt_end != -1 else len(text)]

        depth = 0
        in_quote = False
        tuple_start = -1
        i = 0
        n = len(body)
        while i < n:
            ch = body[i]
            if in_quote:
                if ch == "'":
                    if i + 1 < n and body[i + 1] == "'":
                        i += 1
                    else:
                        in_quote = False
            elif ch == "'":
                in_quote = True
            elif ch == "(":
                if depth == 0:
                    tuple_start = i + 1
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0 and tuple_start != -1:
                    rows.append((table, columns, body[tuple_start:i]))
                    tuple_start = -1
            i += 1
    return rows


def split_sql_into_chunks(text: str, chunk_size: int = _CHUNK_SIZE) -> list[str]:
    """INSERT 문의 각 행을 '컬럼=값' 형태 자연어 문장으로 바꿔, 행이 잘리지 않게 청크로 묶는다.

    임베딩 유사도 검색은 원본 SQL 조각보다 이런 문장형 표현에서 훨씬 잘 맞는다.
    INSERT 문을 못 찾으면(스키마 DDL 등) 기존 고정 길이 분할로 폴백한다.
    """
    rows = _extract_insert_rows(text)
    if not rows:
        return split_into_chunks(text, chunk_size=chunk_size)

    row_sentences: list[str] = []
    for table, columns, row_raw in rows:
        values = _split_top_level(row_raw)
        pairs = [
            f"{col}={_clean_value(val)}"
            for col, val in zip(columns, values)
            if _clean_value(val) is not None
        ]
        row_sentences.append(f"{table} 테이블 행: " + ", ".join(pairs))

    chunks: list[str] = []
    current: list[str] = []
    current_len = 0
    for sentence in row_sentences:
        if current and current_len + len(sentence) + 1 > chunk_size:
            chunks.append("\n".join(current))
            current = []
            current_len = 0
        current.append(sentence)
        current_len += len(sentence) + 1
    if current:
        chunks.append("\n".join(current))
    return chunks
