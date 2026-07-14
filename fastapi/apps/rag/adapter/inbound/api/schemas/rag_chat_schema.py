from pydantic import BaseModel, Field
from typing import Literal


class RagMessageItem(BaseModel):
    role: Literal["user", "assistant"]
    text: str


class RagChatSchema(BaseModel):
    messages: list[RagMessageItem] = Field(..., description="채팅 메시지 히스토리")

    model_config = {
        "json_schema_extra": {
            "example": {
                "messages": [{"role": "user", "text": "업로드한 문서 요약해줘"}],
            }
        }
    }


class RagChatResponseSchema(BaseModel):
    text: str
