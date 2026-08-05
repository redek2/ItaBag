import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .database import engine, Base
from . import models
from app.api.v1.endpoints.mountains import router as mountain_router
from app.api.v1.endpoints.badges import router as badge_router
from app.api.v1.endpoints.ranges import router as range_router
from app.api.v1.endpoints.trips import router as trip_router
from app.api.v1.endpoints.photos import router as photo_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ItaBag API")
app.include_router(mountain_router, prefix="/api/v1/mountains", tags=["mountains"])
app.include_router(badge_router, prefix="/api/v1/badges", tags=["badges"])
app.include_router(range_router, prefix="/api/v1/ranges", tags=["ranges"])
app.include_router(trip_router, prefix="/api/v1/trips", tags=["trips"])
app.include_router(photo_router, prefix="/api/v1/photos", tags=["photos"])
os.makedirs("uploads/gpx", exist_ok=True)
os.makedirs("uploads/photos", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
def read_root():
    return {
        "status": "ok",
        "message": "Backend ItaBag działa"
    }