from pydantic import BaseModel


class WalterRoasterSchema(BaseModel):
    id: int = 1
    name: str = "walter"
    memo: str = "월터는 타이타닉의 승무원이다"
