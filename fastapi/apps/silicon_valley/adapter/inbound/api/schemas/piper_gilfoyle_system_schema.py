from pydantic import BaseModel, Field


class GilfoyleSystemSchema(BaseModel):

    id: int = Field(0, description="Employee ID")
    name: str = Field("버트람 길포일", description="Employee's name")
    # 시스템 아키텍트. 인프라 및 서버 담당. 냉소적이지만 탁월한 실력의 소유자

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 4,
                "name": "Bertram Gilfoyle",
            }
        }
    }
