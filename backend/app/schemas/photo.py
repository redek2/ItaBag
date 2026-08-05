from pydantic import BaseModel, ConfigDict
from enum import Enum

class PhotoType(str, Enum):
    SUMMIT_PROOF = "SUMMIT_PROOF"
    ROUTE = "ROUTE"

class PhotoBase(BaseModel):
    file_path: str
    photo_type: PhotoType

class PhotoCreate(PhotoBase):
    pass

class PhotoResponse(PhotoBase):
    id: int
    trip_id: int

    model_config = ConfigDict(from_attributes=True)