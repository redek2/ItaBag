from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.schemas.stats import BadgeProgressResponse, BadgeProgressDetailResponse, UserStatsResponse

from datetime import date

router = APIRouter()

@router.get("/badges", response_model=list[BadgeProgressResponse])
def read_badge_progress(
    db: Session = Depends(get_db)
):
    visited_rows = db.query(models.TripMountain.mountain_id).join(models.Trip, models.Trip.id == models.TripMountain.trip_id).filter(models.Trip.is_planned == False).all()
    visited_ids = {row[0] for row in visited_rows}
    badges = db.query(models.Badge).all()
    results = []
    for badge in badges:
        total = len(badge.mountains)
        acquired = [m for m in badge.mountains if m.id in visited_ids]
        acquired_count = len(acquired)
        percentage = round((acquired_count/total) * 100, 2) if total > 0 else 0.0
        results.append(
            BadgeProgressResponse(
                id=badge.id,
                name=badge.name,
                description=badge.description,
                icon_url=badge.icon_url,
                total_mountains=total,
                acquired_mountains_count=acquired_count,
                completion_percentage=percentage,
            )
        )
    return results

@router.get("/badges/{badge_id}", response_model=BadgeProgressDetailResponse)
def read_badge_progress_detail(
    badge_id: int,
    db: Session = Depends(get_db)
):
    badge = db.query(models.Badge).filter(models.Badge.id == badge_id).first()
    if badge is None:
        raise HTTPException(status_code=404, detail="Badge not found")
    visited_rows = db.query(models.TripMountain.mountain_id).join(models.Trip, models.Trip.id == models.TripMountain.trip_id).filter(models.Trip.is_planned == False).all()
    visited_ids = {row[0] for row in visited_rows}
    acquired_mountains = [m for m in badge.mountains if m.id in visited_ids]
    missing_mountains = [m for m in badge.mountains if m.id not in visited_ids]
    total = len(badge.mountains)
    acquired_count = len(acquired_mountains)
    completion_percentage = round((acquired_count / total) * 100, 2) if total > 0 else 0.0
    return BadgeProgressDetailResponse(
        id=badge.id,
        name=badge.name,
        description=badge.description,
        icon_url=badge.icon_url,
        total_mountains=total,
        acquired_mountains_count=acquired_count,
        completion_percentage=completion_percentage,
        acquired_mountains=acquired_mountains,
        missing_mountains=missing_mountains,
    )

@router.get("/summary", response_model=UserStatsResponse)
def read_user_summary(
    db: Session = Depends(get_db)
):
    total_trips_count = db.query(models.Trip.id).filter(models.Trip.is_planned == False).count()
    visited_rows = db.query(models.TripMountain.mountain_id).join(models.Trip, models.Trip.id == models.TripMountain.trip_id).filter(models.Trip.is_planned == False).all()
    visited_ids = {row[0] for row in visited_rows}
    unique_mountains_count = len(visited_ids)
    highest_mountain_visited = (db.query(models.Mountain).filter(models.Mountain.id.in_(visited_ids)).order_by(models.Mountain.elevation_m.desc()).first() if visited_ids else None)
    latest_trip = db.query(models.Trip).filter(models.Trip.is_planned == False, models.Trip.date.isnot(None)).order_by(models.Trip.date.desc()).first()
    days_since_last_trip = (date.today() - latest_trip.date).days if latest_trip and latest_trip.date else None
    return UserStatsResponse(
        total_trips_count=total_trips_count,
        unique_mountains_count=unique_mountains_count,
        highest_mountain_visited=highest_mountain_visited,
        days_since_last_trip=days_since_last_trip,
    )