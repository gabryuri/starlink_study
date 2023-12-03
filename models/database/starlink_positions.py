import datetime
from sqlalchemy import create_engine, Column, String, Float, Boolean, DateTime, PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base, Session
from geoalchemy2 import Geography

Base = declarative_base()


class SatelliteLocations(Base):
    __tablename__ = "satellite_locations"
    object_id = Column(String(255), primary_key=True)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow, primary_key=True)
    location = Column(Geography("POINT", srid=4326))
    longitude = Column(Float)
    latitude = Column(Float)
    is_lat_long_complete = Column(Boolean)

    __table_args__ = (PrimaryKeyConstraint("object_id", "creation_date"),)