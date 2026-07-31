from fastapi import FastAPI
from .database import engine, Base
from . import models
from app.api.v1.endpoints.mountains import router as mountain_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ItaBag API")
app.include_router(mountain_router, prefix="/api/v1/mountains", tags=["mountains"])

@app.get("/")
def read_root():
    return {
        "status": "ok",
        "message": "Backend ItaBag działa"
    }