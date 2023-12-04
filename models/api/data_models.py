from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator


class InvalidTimestampFormatError(Exception):
    def __init__(self):
        self.message = "Timestamp must be in the format YYYY-MM-DDTHH:MM:SS"
        super().__init__(self.message)


class LastKnownLocationDataModel(BaseModel):
    """
    Pydantic model for validating input payloads for the last known location query.

    Attributes:
        object_id (str): The unique identifier of the object.
        timestamp (str): The timestamp representing the last known location of the object.

    Methods:
        validate_timestamp: Validates that the timestamp is in the correct format (YYYY-MM-DDTHH:MM:SS).
    """

    object_id: str
    timestamp: str

    @validator("timestamp")
    def validate_timestamp(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%dT%H:%M:%S")
            return v
        except ValueError:
            raise InvalidTimestampFormatError()


class LastKnownLocationResponseDataModel(BaseModel):
    """
    Pydantic model for the response data of the last known location query.

    Attributes:
        object_id (str): The unique identifier of the object.
        creation_date (datetime): The date and time of the record's creation.
        latitude (Optional[float]): The latitude of the object's location, if available.
        longitude (Optional[float]): The longitude of the object's location, if available.

    Methods:
        format_creation_date: Formats the creation date to a specific string format (YYYY-MM-DDTHH:MM:SS).

    Note: using model_dump() will not convert to the desired timestamp format.
    Use model_dump_json() instead and re convert to dict.
    """

    object_id: str
    creation_date: datetime
    latitude: Optional[float]
    longitude: Optional[float]

    @validator("creation_date", pre=True)
    def format_creation_date(cls, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S")


class ClosestSatelliteDataModel(BaseModel):
    """
    Pydantic model for validating input payloads for the closest satellite query.

    Attributes:
        timestamp (str): The timestamp at which the proximity of satellites is evaluated.
        latitude (float): The latitude coordinate of the location.
        longitude (float): The longitude coordinate of the location.

    Methods:
        validate_latitude: Validates that the latitude is within the range of -90 to 90.
        validate_longitude: Validates that the longitude is within the range of -180 to 180.
        validate_timestamp: Validates that the timestamp is in the correct format (YYYY-MM-DDTHH:MM:SS).
    """

    timestamp: str
    latitude: float
    longitude: float

    @validator("latitude")
    def validate_latitude(cls, value):
        if value is not None and not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        return value

    @validator("longitude")
    def validate_longitude(cls, value):
        if value is not None and not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        return value

    @validator("timestamp")
    def validate_timestamp(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%dT%H:%M:%S")
            return v
        except ValueError:
            raise InvalidTimestampFormatError()


class ClosestSatelliteResponseDataModel(BaseModel):
    """
    Pydantic model for the API response data of the closest satellite query.

    Attributes:
        object_id (str): The unique identifier of the satellite.
        creation_date (datetime): The date and time of the record's creation.
        latitude (float): The latitude of the satellite's location.
        longitude (float): The longitude of the satellite's location.

    Methods:
        format_creation_date: Formats the creation date to a specific string format (YYYY-MM-DD HH:MM:SS).

    Note: using model_dump() will not convert to the desired timestamp format.
    Use model_dump_json instead and re convert to dict.
    """

    object_id: str
    creation_date: datetime
    latitude: float
    longitude: float

    @validator("creation_date", pre=True)
    def format_creation_date(cls, value):
        return value.strftime("%Y-%m-%d %H:%M:%S")
