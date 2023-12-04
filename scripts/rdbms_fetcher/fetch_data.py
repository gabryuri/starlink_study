import logging

from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.exc import NoResultFound
from geoalchemy2.functions import ST_MakePoint, ST_SetSRID, ST_Distance

from scripts.configuration.database import DatabaseConfigurationHelper
from models.database.starlink_positions import SatelliteLocations


class RdbmsDataFetcher:
    """
    Manages the ORM interaction between the API routes and our Postgresql (in this case) database.
    Can also be used with different RDBMS engines.

    Attributes:
        logger (Logger): A logging object for capturing the activities of the data fetcher.
        cfg (DatabaseConfigurationHelper): A helper object for database configuration.
        engine (Engine): A SQLAlchemy engine object for database connection and operations.

    Methods:
        get_last_known_location: Retrieves the last recorded position of a specified object up to a certain timestamp.
        get_closest_satellite: Finds the nearest satellite to a given latitude and longitude at a specific timestamp.

    """

    def __init__(self, logger) -> None:
        self.logger = logger.getChild("RdbmsDataFetcher")
        self.logger.setLevel(logging.INFO)
        self.cfg = DatabaseConfigurationHelper(logger)
        self.engine = create_engine(self.cfg.database_uri, echo=False)

    def get_last_known_location(self, object_id: str, timestamp_as_str: str) -> dict:
        """
        Retrieves the last known location of an satellite based on its object_id and a specified timestamp as a string.

        Parameters:
            object_id (str): The unique identifier of the object whose position is to be retrieved.
            timestamp (str): The upper time limit up to which the position data is considered.

        Returns:
            dict: A dictionary containing the database row of the last known position of the object.

        Raises:
            NoResultFound: If no position data is found for the given object_id and timestamp.
            To be used while outputting Error 404 in Flask
        """
        session = Session(bind=self.engine)
        self.logger.info("Fetching last known location")
        last_known_position = (
            session.query(SatelliteLocations)
            .filter(SatelliteLocations.object_id == object_id)
            .filter(SatelliteLocations.creation_date <= timestamp_as_str)
            .order_by(SatelliteLocations.creation_date.desc())
            .first()
        )

        if last_known_position is not None:
            return last_known_position.to_dict()
        else:
            raise NoResultFound("No position found for the given object_id and timestamp")

    def get_closest_satellite(self, timestamp_as_str: str, latitude: float, longitude: float) -> dict:
        """
        Identifies the closest satellite to a given latitude and longitude at a specific timestamp as a string.
        Note that the timestamp must be an exact match.

        Parameters:
            timestamp (str): The exact time at which the proximity of satellites is evaluated.
            latitude (float): The latitude of the point of interest.
            longitude (float): The longitude of the point of interest.

        Returns:
            dict: A dictionary containing details of the closest satellite.

        Raises:
            NoResultFound: If no satellite is found close to the specified location at the given timestamp.
            To be used while outputting Error 404 in Flask
        """
        session = Session(bind=self.engine)
        self.logger.info("Fetching closest satellite")
        point = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)

        closest_satellite = (
            session.query(SatelliteLocations)
            .filter(SatelliteLocations.creation_date == timestamp_as_str)
            .order_by(ST_Distance(SatelliteLocations.location, point))
            .first()
        )

        if closest_satellite is not None:
            return closest_satellite.to_dict()
        else:
            raise NoResultFound("No position found for the given object_id and timestamp")
