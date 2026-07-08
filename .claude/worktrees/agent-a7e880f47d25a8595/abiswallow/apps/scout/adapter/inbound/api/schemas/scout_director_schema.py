from pydantic import BaseModel


class ScoutDirectorStatusSchema(BaseModel):
    module: str
    message: str
