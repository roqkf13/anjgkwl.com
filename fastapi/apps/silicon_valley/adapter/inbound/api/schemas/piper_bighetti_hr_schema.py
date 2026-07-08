from pydantic import BaseModel, Field


class BighettiHrSchema(BaseModel):

    id: int = Field(0, description="Employee ID")
    name: str = Field("넬슨 빅헤드 비게티", description="Employee's name")
    # Pied Piper 공동창업자. 운으로 거대한 성공을 이룬 HR 담당

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 5,
                "name": "Nelson Bighetti",
            }
        }
    }
