from pydantic import BaseModel, Field


class DineshDashSchema(BaseModel):

    id: int = Field(0, description="Employee ID")
    name: str = Field("디네시 추그타이", description="Employee's name")
    # 백엔드 엔지니어. 대시보드 개발 담당. 길포일과 끊임없이 경쟁하는 인물

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 3,
                "name": "Dinesh Chugtai",
            }
        }
    }
