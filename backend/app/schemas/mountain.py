from pydantic import BaseModel, ConfigDict

# Schemat bazowy (Request Body)
class MountainBase(BaseModel):
    id: int
    name: str
    elevation_m: int
    prominence_m: int | None = None
    lat: float
    lng: float
    range_id: int | None = None

    model_config = ConfigDict(from_attributes=True)

# Schemat wyjściowy (Response Model)
class MountainResponse(MountainBase):
    pass