from typing import Optional

from pydantic import BaseModel, Field, computed_field, validator
from geoalchemy2.functions import ST_MakePoint


class SpaceTrack(BaseModel):
    object_id: str = Field(..., alias="OBJECT_ID")
    creation_date: str = Field(..., alias="CREATION_DATE")

    class Config:
        populate_by_name = True


class SatelliteData(BaseModel):
    spaceTrack: SpaceTrack
    latitude: Optional[float]
    longitude: Optional[float]

    class Config:
        from_attributes = True

    def dict(self, *args, **kwargs) -> dict:
        return {
            "object_id": self.spaceTrack.object_id,
            "creation_date": self.spaceTrack.creation_date,
            "location": self.location,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "is_lat_long_complete": self.is_lat_long_complete,
        }

    @computed_field
    @property
    def is_lat_long_complete(self) -> bool:
        """
        Property to check if both latitude and longitude are present.

        Returns:
            bool: True if both latitude and longitude are present. Otherwise, False.
        """
        return self.latitude is not None and self.longitude is not None

    @computed_field
    @property
    def location(self) -> bool:
        """
        Property to turn latitude and longitude into point for ORM

        Returns:
            Point object.
        """
        return ST_MakePoint(self.longitude, self.latitude)

    @validator("latitude")
    def validate_latitude(cls, value):
        if value is not None and not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90 or null.")
        return value

    @validator("longitude")
    def validate_longitude(cls, value):
        if value is not None and not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180 or null.")
        return value
