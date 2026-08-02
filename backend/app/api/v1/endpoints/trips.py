from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.schemas.trip import TripResponse, TripDetailsResponse, TripCreate, TripUpdate

from datetime import date

router = APIRouter()

@router.get("/", response_model=list[TripResponse])
def read_trips(
    date: date | None = Query(default=None),
    rating_views: int | None = Query(default=None),
    rating_effort: int | None = Query(default=None),
    is_planned: bool | None = Query(default=None),

    mountain_id: int | None = Query(default=None),

    db: Session = Depends(get_db)
):
    query = db.query(models.Trip)
    if is_planned is not None:
        query = query.filter(models.Trip.is_planned == is_planned)
    if mountain_id is not None:
        query = query.filter(models.Trip.mountains.any(models.Mountain.id == mountain_id))
    return query.all()

@router.get("/{trip_id}", response_model=TripDetailsResponse)
def read_trip(
    trip_id: int,
    db: Session = Depends(get_db)
):
    trip = db.query(models.Trip).filter(models.Trip.id == trip_id).first()
    if trip is None:
        raise HTTPException(status_code=404, detail=r"Trip not found ¯\_(ツ)_/¯")
    return trip

@router.post("/", response_model=TripDetailsResponse, status_code=201)
def create_trip(
    trip_in: TripCreate,
    db: Session = Depends(get_db)
):
    mountains = db.query(models.Mountain).filter(models.Mountain.id.in_(trip_in.mountain_ids)).all()
    trip_data = trip_in.model_dump(exclude={"mountain_ids"})
    db_trip = models.Trip(**trip_data)
    db_trip.mountains = mountains
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip

@router.patch("/{trip_id}", response_model=TripDetailsResponse)
def update_trip(
    trip_id: int,
    trip_in: TripUpdate,
    db: Session = Depends(get_db)
):
    db_trip = db.query(models.Trip).filter(models.Trip.id == trip_id).first()
    if db_trip is None:
        raise HTTPException(status_code=404, detail=r"Trip not found ¯\_(ツ)_/¯")

    update_data = trip_in.model_dump(exclude_unset=True)

    if "mountain_ids" in update_data:
        mountain_ids = update_data.pop("mountain_ids")
        mountains = db.query(models.Mountain).filter(models.Mountain.id.in_(mountain_ids)).all()
        db_trip.mountains = mountains

    for field, value in update_data.items():
        setattr(db_trip, field, value)

    db.commit()
    db.refresh(db_trip)
    return db_trip

@router.delete("/{trip_id}", status_code=204)
def delete_trip(
    trip_id: int,
    db: Session = Depends(get_db)
):
    db_trip = db.query(models.Trip).filter(models.Trip.id == trip_id).first()
    if db_trip is None:
        raise HTTPException(status_code=404, detail=r"Trip not found ¯\_(ツ)_/¯")
    db.delete(db_trip)
    db.commit()
    return