from pydantic import BaseModel, ConfigDict
from app.schemas.mountain import MountainResponse

class BadgeBase(BaseModel):
    id: int
    name: str
    description: str | None = None
    icon_url: str | None = None
    rules_url: str | None = None

    model_config = ConfigDict(from_attributes=True)

class BadgeResponse(BadgeBase):
    pass
class BadgeDetailResponse(BadgeResponse):
    mountains: list[MountainResponse] = []