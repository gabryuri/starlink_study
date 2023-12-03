from typing import Type
import logging
import ijson
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from geoalchemy2.functions import ST_MakePoint, ST_SetSRID, ST_Distance
from sqlalchemy.exc import NoResultFound
from models.json_input.satellite_position import SatelliteData
from models.database.starlink_positions import Base
from scripts.configuration.database import DatabaseConfigurationHelper

from models.database.starlink_positions import SatelliteLocations, Base


class RdbmsDataFetcher:
    def __init__(self, logger) -> None:
        self.logger = logger.getChild("RdbmsDataFetcher")
        self.logger.setLevel(logging.INFO)
        self.cfg = DatabaseConfigurationHelper(logger)
        self.engine = create_engine(self.cfg.database_uri, echo=False)
        self.session = Session(bind=self.engine)

    def get_last_known_location(self, object_id, timestamp):
        self.logger.info("Fetching last known location")
        last_known_position = (
            self.session.query(SatelliteLocations)
            .filter(SatelliteLocations.object_id == object_id)
            .filter(SatelliteLocations.creation_date <= timestamp)
            .order_by(SatelliteLocations.creation_date.desc())
            .first()
        )

        if last_known_position is None:
            raise NoResultFound("No position found for the given object_id and timestamp")

        return f"{last_known_position.latitude} and {last_known_position.longitude} "

    def get_closest_satellite(self, timestamp, latitude, longitude):
        self.logger.info("Fetching closest satellite")
        point = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)

        closest_satellite = (
            self.session.query(SatelliteLocations)
            .filter(SatelliteLocations.creation_date == timestamp)
            .order_by(ST_Distance(SatelliteLocations.location, point))
            .first()
        )

        if closest_satellite is None:
            raise NoResultFound("No position found for the given object_id and timestamp")

        return f"{closest_satellite.latitude} and {closest_satellite.longitude} and {closest_satellite.object_id} "
