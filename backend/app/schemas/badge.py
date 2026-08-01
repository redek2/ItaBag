from pydantic import BaseModel, ConfigDict
from app.schemas.mountain import MountainResponse

class BadgeBase(BaseModel):
    name: str
    description: str | None = None
    icon_url: str | None = None
    rules_url: str | None = None

class BadgeResponse(BadgeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class BadgeDetailResponse(BadgeResponse):
    mountains: list[MountainResponse] = []