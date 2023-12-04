from typing import Optional

from pydantic import BaseModel, Field, computed_field, validator
from geoalchemy2.functions import ST_MakePoint


class SpaceTrack(BaseModel):
    """
    Pydantic model representing space track nested data of a satellite.

    This model parses and stores basic space track information:
        the object's identifier and creation date.

    Attributes:
        object_id (str): The unique identifier of the satellite, aliased as 'OBJECT_ID'.
        creation_date (str): The creation date of the satellite record, aliased as 'CREATION_DATE'.

    Class Config:
        populate_by_name (bool): Configuration to allow Pydantic to enable our aliasing strategy.
    """

    object_id: str = Field(..., alias="OBJECT_ID")
    creation_date: str = Field(..., alias="CREATION_DATE")

    class Config:
        populate_by_name = True


class SatelliteData(BaseModel):
    """
    Pydantic model representing detailed satellite data, including space track information and geographical coordinates.

    Attributes:
        spaceTrack (SpaceTrack): An instance of the SpaceTrack model representing the basic space track data.
        latitude (Optional[float]): The latitude coordinate of the satellite. May be None if not available.
        longitude (Optional[float]): The longitude coordinate of the satellite. May be None if not available.

    Class Config:
        from_attributes (bool): Configuration indicating that sub-models should be populated from attributes with the same name.

    Methods:
        dict: Converts the SatelliteData instance into a dictionary format, including computed fields.
        is_lat_long_complete: A property indicating whether both latitude and longitude are provided.
        location: A property that instantiates a Point object from latitude and longitude.
        validate_latitude: Validates the latitude value to ensure it's within the valid range or null.
        validate_longitude: Validates the longitude value to ensure it's within the valid range or null.
    """

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
