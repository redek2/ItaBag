from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.schemas.range import RangeResponse, RangeDetailsResponse

router = APIRouter()

@router.get("/", response_model=list[RangeResponse])
def read_ranges(
    mountain_id: int | None = Query(default=None),
    db: Session = Depends(get_db)
):
    query = db.query(models.Range)
    if mountain_id is not None:
        query = query.filter(models.Range.mountains.any(models.Mountain.id == mountain_id))
    return query.all()

@router.get("/{range_id}", response_model=RangeDetailsResponse)
def read_range(
    range_id: int,
    db: Session = Depends(get_db)
):
    db_range = db.query(models.Range).filter(models.Range.id == range_id).first()
    if db_range is None:
        raise HTTPException(status_code=404, detail="Range not found")
    return db_range