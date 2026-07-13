from pydantic import BaseModel


class VisionUploadResponseSchema(BaseModel):
    filename: str
    content_type: str
    size_bytes: int
    message: str


class FaceRecognitionResponseSchema(BaseModel):
    name: str
    confidence: float
