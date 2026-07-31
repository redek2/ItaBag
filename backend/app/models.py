from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Range(Base):
    __tablename__ = "ranges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    mountains = relationship("Mountain", back_populates="range")

class Mountain(Base):
    __tablename__ = "mountains"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    elevation_m = Column(Integer, nullable=False)
    prominence_m = Column(Integer, nullable=True)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    range_id = Column(Integer, ForeignKey("ranges.id"))

    range = relationship("Range", back_populates="mountains")
    badges = relationship("Badge", secondary="mountain_badges", back_populates="mountains")

class Badge(Base):
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    rules_url = Column(String, nullable=True)

    mountains = relationship("Mountain", secondary="mountain_badges", back_populates="badges")

class MountainBadge(Base):
    __tablename__ = "mountain_badges"

    mountain_id = Column(Integer, ForeignKey("mountains.id"), primary_key=True)
    badge_id = Column(Integer, ForeignKey("badges.id"), primary_key=True)

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, nullable=True)
    gpx_path = Column(String, nullable=True)
    rating_views = Column(Integer, nullable=True)
    rating_effort = Column(Integer, nullable=True)
    notes = Column(String, nullable=True)
    is_planned = Column(Boolean, default=False)

    mountains = relationship("Mountain", secondary="trip_mountains")
    photos = relationship("Photo", back_populates="trip")

class TripMountain(Base):
    __tablename__ = "trip_mountains"

    trip_id = Column(Integer, ForeignKey("trips.id"), primary_key=True)
    mountain_id = Column(Integer, ForeignKey("mountains.id"), primary_key=True)

class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    file_path = Column(String, nullable=False)
    type = Column(String, nullable=False)  # SUMMIT_PROOF / ROUTE

    trip = relationship("Trip", back_populates="photos")