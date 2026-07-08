from pydantic import BaseModel, EmailStr, Field


class WatsonExecutorSchema(BaseModel):
    id: int = Field(0, description="Watson ID")
    name: str = Field("존 왓슨", description="Watson's name")

    model_config = {"json_schema_extra": {"example": {"id": 0, "name": "존 왓슨"}}}


class WatsonSendEmailRequest(BaseModel):
    to: EmailStr
    from_account: EmailStr
    prompt: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "to": "recipient@example.com",
                "from_account": "watson@sherlock.com",
                "prompt": "이 이메일 스팸 여부를 판단해줘",
            }
        }
    }
