from pydantic import BaseModel, Field


class DiscordSchema(BaseModel):
    id: int = Field(0, description="Channel ID")
    name: str = Field("디스코드 채널", description="Channel name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 15,
                "name": "디스코드 채널 (Discord)",
            }
        }
    }
