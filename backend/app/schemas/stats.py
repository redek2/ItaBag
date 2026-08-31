from pydantic import BaseModel, ConfigDict
from app.schemas.mountain import MountainResponse

class BadgeProgressResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    icon_url: str | None = None
    total_mountains: int
    acquired_mountains_count: int
    completion_percentage: float
    model_config = ConfigDict(from_attributes=True)


class BadgeProgressDetailResponse(BadgeProgressResponse):
    acquired_mountains: list[MountainResponse] = []
    missing_mountains: list[MountainResponse] = []


class UserStatsResponse(BaseModel):
    total_trips_count: int
    unique_mountains_count: int
    highest_mountain_visited: MountainResponse | None = None
    days_since_last_trip: int | None = None
    model_config = ConfigDict(from_attributes=True)