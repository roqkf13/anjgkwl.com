from pydantic import BaseModel, Field


class RouteQuerySchema(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)

    model_config = {
        "json_schema_extra": {
            "example": {"text": "전북 현대 홈구장이 어디야?"},
        }
    }


class RouteQueryResponseSchema(BaseModel):
    route: str
    answer: str
    confidence: float
