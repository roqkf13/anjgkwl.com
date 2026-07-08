from pydantic import BaseModel, Field


class GenreGameDto(BaseModel):
    title: str = Field(..., min_length=1)
    summary: str = Field(default="")
    steam_app_id: int = Field(..., ge=1)


class GenreHubDto(BaseModel):
    id: str
    label: str
    description: str
    representative_title: str
    traits: list[str]
    games: list[GenreGameDto]
