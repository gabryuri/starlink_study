import logging
from flask import Flask
from flask_restx import Resource, Api

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from models.database.starlink_positions import SatelliteLocations
from models.api.data_models import (
    LastKnownPositionDataModel,
    ClosestSatelliteDataModel,
    InvalidTimestampFormatError,
)
from models.api.schemas.api_schemas import LAST_KNOWN_POS_SCHEMA, CLOSEST_SATELLITE_SCHEMA

from scripts.rdbms_fetcher.fetch_data import RdbmsDataFetcher

HTTP_OK = 200
HTTP_NOT_FOUND = 404
HTTP_BAD_REQUEST = 400


app = Flask(__name__)
api = Api(app, title="Data Contracts API", version="1.0", description="Data Contracts Access layer.")


fetcher = RdbmsDataFetcher(logger=app.logger)

last_known_position_model = api.schema_model("LastKnownPositionModel", LAST_KNOWN_POS_SCHEMA)
expected_exceptions = (InvalidTimestampFormatError, NoResultFound)


@api.route("/last_known_location")
class LastKnownLocation(Resource):
    @api.doc(description="Retrieves the last known location of a satellite object based on its ID and timestamp.")
    @api.expect(last_known_position_model)
    @api.response(HTTP_OK, "Last known location found.")
    @api.response(HTTP_NOT_FOUND, "Not found")
    @api.response(HTTP_BAD_REQUEST, "Invalid request.")
    def post(self):
        try:
            payload = api.payload
            validated_data = LastKnownPositionDataModel.model_validate(payload)

            location = fetcher.get_last_known_location(validated_data.object_id, validated_data.timestamp)
            return location

        except expected_exceptions as ex:
            api.abort(HTTP_BAD_REQUEST, str(ex))

        except Exception as ex:
            print(str(ex))
            api.abort(HTTP_BAD_REQUEST, str(ex))


closest_satellite_model = api.schema_model("ClosestSatelliteModel", CLOSEST_SATELLITE_SCHEMA)


@api.route("/closest_satellite")
class LastKnownLocation(Resource):
    @api.doc(description="Retrieves the closest satellite given a timestamp and a position.")
    @api.expect(closest_satellite_model)
    @api.response(HTTP_OK, "Closest Satellite found.")
    @api.response(HTTP_NOT_FOUND, "Not found")
    @api.response(HTTP_BAD_REQUEST, "Invalid request.")
    def post(self):
        try:
            payload = api.payload
            validated_data = ClosestSatelliteDataModel.model_validate(payload)

            closest_satellite = fetcher.get_closest_satellite(
                validated_data.timestamp, validated_data.latitude, validated_data.longitude
            )
            return closest_satellite

        except expected_exceptions as ex:
            api.abort(HTTP_BAD_REQUEST, str(ex))

        except Exception as ex:
            print(str(ex))
            api.abort(HTTP_BAD_REQUEST, str(ex))


app.logger.info("Environment Initialized.")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
