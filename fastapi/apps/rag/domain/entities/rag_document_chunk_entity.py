from dataclasses import dataclass


@dataclass(frozen=True)
class RagDocumentChunkEntity:
    id: int | None
    document_name: str
    chunk_index: int
    content: str
    embedding: list[float]
