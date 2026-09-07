from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.schemas.mountain import MountainDetailResponse, MountainResponse

router = APIRouter()

@router.get("/", response_model=list[MountainResponse])
def read_mountains(
    min_elevation: int | None = Query(default=None, description="Minimalna wysokość n.p.m."),
    max_elevation: int | None = Query(default=None, description="Maksymalna wysokość n.p.m."),
    range_id: int | None = Query(default=None, description="ID pasma górskiego"),
    badge_id: int | None = Query(default=None, description="ID odznaki"),
    is_visited: bool | None = Query(default=None, description="Czy góra została odwiedzona"),
    db: Session = Depends(get_db)
):
    query = db.query(models.Mountain)
    if min_elevation is not None:
        query = query.filter(models.Mountain.elevation_m >= min_elevation)
    if max_elevation is not None:
        query = query.filter(models.Mountain.elevation_m <= max_elevation)
    if range_id is not None:
        query = query.filter(models.Mountain.range_id == range_id)
    if badge_id is not None:
        query = query.join(models.Mountain.badges).filter(models.Badge.id == badge_id)
    visited_query = db.query(models.TripMountain.mountain_id).join(models.Trip).filter(models.Trip.is_planned == False)
    visited_ids = {row[0] for row in visited_query.all()}
    if is_visited is not None:
        if is_visited:
            query = query.filter(models.Mountain.id.in_(visited_ids))
        else:
            query = query.filter(models.Mountain.id.not_in(visited_ids))
    mountains = query.all()
    for m in mountains:
        m.is_visited = m.id in visited_ids
    return mountains

@router.get("/{mountain_id}", response_model=MountainDetailResponse)
def read_mountain(
    mountain_id: int,
    db: Session = Depends(get_db)
):
    mountain = db.query(models.Mountain).filter(models.Mountain.id == mountain_id).first()
    if mountain is None:
        raise HTTPException(status_code=404, detail="Mountain not found")
    has_visited = (
        db.query(models.TripMountain)
        .join(models.Trip)
        .filter(
            models.TripMountain.mountain_id == mountain_id,
            models.Trip.is_planned == False
        )
        .first()
        is not None
    )
    mountain.is_visited = has_visited
    return mountain