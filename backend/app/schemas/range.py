from pydantic import BaseModel, ConfigDict
from app.schemas.mountain import MountainResponse

class RangeBase(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class RangeResponse(RangeBase):
    pass

class RangeDetailsResponse(RangeResponse):
    mountains: list[MountainResponse] = []