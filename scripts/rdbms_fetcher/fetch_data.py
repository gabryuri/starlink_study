from typing import Type
import logging
import ijson
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from geoalchemy2.functions import ST_MakePoint, ST_SetSRID, ST_Distance
from sqlalchemy.exc import NoResultFound
from models.database.starlink_positions import Base
from scripts.configuration.database import DatabaseConfigurationHelper
from models.database.starlink_positions import SatelliteLocations, Base


class RdbmsDataFetcher:
    def __init__(self, logger) -> None:
        self.logger = logger.getChild("RdbmsDataFetcher")
        self.logger.setLevel(logging.INFO)
        self.cfg = DatabaseConfigurationHelper(logger)
        self.engine = create_engine(self.cfg.database_uri, echo=False)

    def get_last_known_location(self, object_id, timestamp):
        session = Session(bind=self.engine)
        self.logger.info("Fetching last known location")
        last_known_position = (
            session.query(SatelliteLocations)
            .filter(SatelliteLocations.object_id == object_id)
            .filter(SatelliteLocations.creation_date <= timestamp)
            .order_by(SatelliteLocations.creation_date.desc())
            .first()
        )

        if last_known_position is not None:
            return last_known_position.to_dict()
        else:
            raise NoResultFound("No position found for the given object_id and timestamp")


    def get_closest_satellite(self, timestamp, latitude, longitude):
        session = Session(bind=self.engine)
        self.logger.info("Fetching closest satellite")
        point = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)

        closest_satellite = (
            session.query(SatelliteLocations)
            .filter(SatelliteLocations.creation_date == timestamp)
            .order_by(ST_Distance(SatelliteLocations.location, point))
            .first()
        )

        if closest_satellite is not None:
            return closest_satellite.to_dict()
        else:
            raise NoResultFound("No position found for the given object_id and timestamp")

