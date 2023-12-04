from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator


class InvalidTimestampFormatError(Exception):
    def __init__(self):
        self.message = "Timestamp must be in the format YYYY-MM-DDTHH:MM:SS"
        super().__init__(self.message)


class LastKnownLocationDataModel(BaseModel):
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
    object_id: str
    creation_date: datetime
    latitude: Optional[float]
    longitude: Optional[float]

    @validator('creation_date', pre=True)
    def format_creation_date(cls, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S")

class ClosestSatelliteDataModel(BaseModel):
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
    object_id: str
    creation_date: datetime
    latitude: float
    longitude: float 

    @validator('creation_date', pre=True)
    def format_creation_date(cls, value):
        return value.strftime('%Y-%m-%d %H:%M:%S')