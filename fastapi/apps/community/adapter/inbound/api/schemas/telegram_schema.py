from pydantic import BaseModel, Field


class TelegramSchema(BaseModel):
    id: int = Field(0, description="Channel ID")
    name: str = Field("텔레그램 채널", description="Channel name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 13,
                "name": "텔레그램 채널 (Telegram)",
            }
        }
    }
