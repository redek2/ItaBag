from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models

import os

router = APIRouter()

@router.delete("/{photo_id}", status_code=204)
def delete_photo(
    photo_id: int,
    db: Session = Depends(get_db)
):
    db_photo = db.query(models.Photo).filter(models.Photo.id == photo_id).first()
    if db_photo is None:
        raise HTTPException(status_code=404, detail=r"Photo not found ¯\_(ツ)_/¯")
    
    if db_photo.file_path and os.path.exists(db_photo.file_path):
        os.remove(db_photo.file_path)
        
    db.delete(db_photo)
    db.commit()
    return