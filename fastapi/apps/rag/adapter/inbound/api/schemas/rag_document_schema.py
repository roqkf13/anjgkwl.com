from pydantic import BaseModel


class RagUploadResponseSchema(BaseModel):
    filename: str
    content_type: str
    size_bytes: int
    chunk_count: int
    message: str
