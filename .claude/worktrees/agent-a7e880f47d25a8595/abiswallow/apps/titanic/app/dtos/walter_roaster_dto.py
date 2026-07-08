from dataclasses import dataclass



@dataclass(frozen=True, slots=True)
class WalterRoasterQuery:
    id: int
    name: str
    memo: str

    
