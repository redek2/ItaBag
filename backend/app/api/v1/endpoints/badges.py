from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.schemas.badge import BadgeResponse, BadgeDetailResponse

router = APIRouter()

@router.get("/", response_model=list[BadgeResponse])
def read_badges(
    mountain_id: int | None = Query(default=None),
    db: Session = Depends(get_db)
):
    query = db.query(models.Badge)
    if mountain_id is not None:
        query = query.filter(models.Badge.mountains.any(models.Mountain.id == mountain_id))
    return query.all()

@router.get("/{badge_id}", response_model=BadgeDetailResponse)
def read_badge(
    badge_id: int,
    db: Session = Depends(get_db)
):
    badge = db.query(models.Badge).filter(models.Badge.id == badge_id).first()
    if badge is None:
        raise HTTPException(status_code=404, detail="Badge not found")
    return badge