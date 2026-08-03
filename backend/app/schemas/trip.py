from pydantic import BaseModel, ConfigDict
from app.schemas.mountain import MountainResponse
import datetime

class TripBase(BaseModel):
    date: datetime.date | None = None
    gpx_path: str | None = None
    rating_views: int | None = None
    rating_effort: int | None = None
    notes: str | None = None
    is_planned: bool = False
    
class TripCreate(TripBase):
    mountain_ids: list[int] = []

class TripUpdate(BaseModel):
    date: datetime.date | None = None
    gpx_path: str | None = None
    rating_views: int | None = None
    rating_effort: int | None = None
    notes: str | None = None
    is_planned: bool | None = None
    mountain_ids: list[int] | None = None

class TripResponse(BaseModel):
    id: int
    date: datetime.date | None = None
    gpx_path: str | None = None
    rating_views: int | None = None
    rating_effort: int | None = None
    notes: str | None = None
    is_planned: bool = False

    model_config = ConfigDict(from_attributes=True)

class TripDetailsResponse(TripResponse):
    mountains: list[MountainResponse] = []