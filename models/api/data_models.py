from datetime import datetime

from pydantic import BaseModel, validator


class InvalidTimestampFormatError(Exception):
    def __init__(self):
        self.message = "Timestamp must be in the format YYYY-MM-DDTHH:MM:SS"
        super().__init__(self.message)


class LastKnownPositionDataModel(BaseModel):
    object_id: str
    timestamp: str

    @validator("timestamp")
    def validate_timestamp(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%dT%H:%M:%S")
            return v
        except ValueError:
            raise InvalidTimestampFormatError()


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