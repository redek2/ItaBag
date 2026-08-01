import json
import os
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app import models

def seed_data():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    mountain_path = os.path.join(os.path.dirname(__file__), "mountains.json")
    badges_path = os.path.join(os.path.dirname(__file__), "badges.json")

    if not os.path.exists(mountain_path):
        print("Brak pliku mountains.json.")
        return
    if not os.path.exists(badges_path):
        print("Brak pliku badges.json.")
        return

    mountains_data = load_json_data(mountain_path)
    badges_data = load_json_data(badges_path)
    for badge in badges_data:
        badge_name = badge["name"].strip()
        if not db.query(models.Badge).filter_by(name=badge_name).first():
            db.add(models.Badge(
                name=badge_name,
                rules_url=badge.get("rules_url") or badge.get("Address")
                ))
    db.commit()

    for item in mountains_data:
        # 1. Pasmo górskie
        range_names = item.get("range_name", [])
        if isinstance(range_names, str):
            range_names = [range_names]

        primary_range = None
        if range_names and range_names[0].strip():
            range_name = range_names[0].strip()
            primary_range = db.query(models.Range).filter_by(name=range_name).first()
            if not primary_range:
                primary_range = models.Range(name=range_name)
                db.add(primary_range)
                db.flush()

        # 2. Góra
        mountain_name = item["name"].strip()
        mountain = db.query(models.Mountain).filter_by(name=mountain_name).first()
        if not mountain:
            mountain = models.Mountain(
                name=mountain_name,
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
        
        if isinstance(badge_names, str):
            badge_names = [badge_names]

        for badge_name in badge_names:
            badge_name_clean = badge_name.strip()
            if badge_name_clean:
                badge = db.query(models.Badge).filter(models.Badge.name.ilike(badge_name_clean)).first()
                if badge and badge not in mountain.badges:
                    mountain.badges.append(badge)
    db.commit()
    db.close()
    print("Zasilanie bazy zakończone sukcesem!")

def load_json_data(file_path: str) -> list[dict]:
    """Wczytuje JSON i zwraca przefiltrowaną listę słowników bez pustych wpisów."""
    try:
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
            return [
                item for item in data
                if isinstance(item, dict) and item.get("name", "").strip()
            ]
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Błąd podczas wczytywania {file_path}: {e}")
        return []

if __name__ == "__main__":
    seed_data()