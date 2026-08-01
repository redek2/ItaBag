from fastapi import FastAPI
from .database import engine, Base
from . import models
from app.api.v1.endpoints.mountains import router as mountain_router
from app.api.v1.endpoints.badges import router as badge_router
from app.api.v1.endpoints.ranges import router as range_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ItaBag API")
app.include_router(mountain_router, prefix="/api/v1/mountains", tags=["mountains"])
app.include_router(badge_router, prefix="/api/v1/badges", tags=["badges"])
app.include_router(range_router, prefix="/api/v1/ranges", tags=["ranges"])

@app.get("/")
def read_root():
    return {
        "status": "ok",
        "message": "Backend ItaBag działa"
    }