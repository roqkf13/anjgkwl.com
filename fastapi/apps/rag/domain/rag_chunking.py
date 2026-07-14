from __future__ import annotations

_CHUNK_SIZE = 800
_CHUNK_OVERLAP = 100


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
