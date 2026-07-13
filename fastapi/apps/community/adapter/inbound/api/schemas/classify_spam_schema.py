from pydantic import BaseModel


class ClassifySpamRequest(BaseModel):
    subject: str
    body: str


class ClassifySpamResponseSchema(BaseModel):
    category: str
    reason: str
