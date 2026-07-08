from pydantic import BaseModel, Field


class ReceiveEmailRequest(BaseModel):
    gmail_id: str = Field(alias="messageId")
    thread_id: str | None = Field(None, alias="threadId")
    from_: str | None = Field(None, alias="from")
    to: str | None = Field(None, alias="to")
    subject: str | None = Field(None, alias="subject")
    snippet: str | None = Field(None, alias="preview")

    model_config = {"populate_by_name": True}


class ReceivedEmailSchema(BaseModel):
    id: str
    gmail_id: str
    thread_id: str | None
    from_: str | None
    to: str | None
    subject: str | None
    snippet: str | None


class ReceivedEmailListSchema(BaseModel):
    total: int
    emails: list[ReceivedEmailSchema]
