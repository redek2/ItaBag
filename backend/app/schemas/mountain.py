from pydantic import BaseModel, ConfigDict

# Schemat wejściowy (Request Body)
class MountainBase(BaseModel):
    name: str
    elevation_m: int
    prominence_m: int | None = None
    lat: float
    lng: float

# Schemat wyjściowy (Response Model)
class MountainResponse(MountainBase):
    id: int
    range_id: int | None = None

    model_config = ConfigDict(from_attributes=True)