from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.schemas.mountain import MountainResponse

router = APIRouter()

@router.get("/", response_model=list[MountainResponse])
def read_mountains(
    min_elevation: int | None = Query(default=None, description="Minimalna wysokość n.p.m."),
    range_id: int | None = Query(default=None, description="ID pasma górskiego"),
    db: Session = Depends(get_db)
):
    query = db.query(models.Mountain)
    if min_elevation is not None:
        query = query.filter(models.Mountain.elevation_m >= min_elevation)
    if range_id is not None:
        query = query.filter(models.Mountain.range_id == range_id)
    return query.all()

@router.get("/{mountain_id}", response_model=MountainResponse)
def read_mountain(
    mountain_id: int,
    db: Session = Depends(get_db)
):
    mountain = db.query(models.Mountain).filter(models.Mountain.id == mountain_id).first()
    if mountain is None:
        raise HTTPException(status_code=404, detail="Mountain not found")
    return mountain