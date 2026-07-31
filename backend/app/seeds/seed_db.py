import json
import os
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app import models

def seed_data():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    json_path = os.path.join(os.path.dirname(__file__), "mountains.json")
    if not os.path.exists(json_path):
        print("Brak pliku mountains.json!")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        mountains_data = json.load(f)

    for item in mountains_data:
        # 1. Pasmo górskie
        range_names = item.get("range_name", [])
        if isinstance(range_names, str):
            range_names = [range_names]

        primary_range = None
        if range_names:
            range_name = range_names[0]
            primary_range = db.query(models.Range).filter_by(name=range_name).first()
            if not primary_range:
                primary_range = models.Range(name=range_name)
                db.add(primary_range)
                db.flush()

        # 2. Góra
        mountain = db.query(models.Mountain).filter_by(name=item["name"]).first()
        if not mountain:
            mountain = models.Mountain(
                name=item["name"],
                elevation_m=item["elevation_m"],
                prominence_m=item.get("prominence_m"),
                lat=item["lat"],
                lng=item["lng"],
                range_id=primary_range.id if primary_range else None
            )
            db.add(mountain)
            db.flush()

        # 3. Odznaki i relacje
        badge_names = item.get("badges", [])
        for b_name in badge_names:
            badge = db.query(models.Badge).filter_by(name=b_name).first()
            if not badge:
                badge = models.Badge(name=b_name)
                db.add(badge)
                db.flush()

            if badge not in mountain.badges:
                mountain.badges.append(badge)
    db.commit()
    db.close()
    print("Zasilanie bazy zakończone sukcesem!")

if __name__ == "__main__":
    seed_data()