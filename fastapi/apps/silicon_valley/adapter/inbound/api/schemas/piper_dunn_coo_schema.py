from pydantic import BaseModel, Field


class DunnCooSchema(BaseModel):

    id: int = Field(0, description="Employee ID")
    name: str = Field("재러드 던", description="Employee's name")
    # Pied Piper COO. 냉철한 비즈니스 감각과 인간적인 따뜻함을 함께 가진 인물

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 2,
                "name": "Jared Dunn",
            }
        }
    }
