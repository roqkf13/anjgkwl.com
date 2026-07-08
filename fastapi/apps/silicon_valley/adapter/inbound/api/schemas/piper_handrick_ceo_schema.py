from pydantic import BaseModel, Field


class HandrickCeoSchema(BaseModel):

    id: int = Field(0, description="Employee ID")
    name: str = Field("리처드 헨드릭스", description="Employee's name")
    # Pied Piper 창업자 겸 CEO. 중간값 압축 알고리즘 발명가

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Richard Hendricks",
            }
        }
    }
