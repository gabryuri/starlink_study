import logging
import datetime

from sqlalchemy import create_engine, Column, String, Boolean, DateTime, Float, PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base, Session

from scripts.configuration.database import DatabaseConfigurationHelper


from models.database.starlink_positions import SatelliteLocations, Base
from scripts.importer.import_data import JsonToRdbmsDataImporter
import logging

logging.basicConfig(
    format="[%(levelname)s] [%(asctime)s][%(filename)-15s][%(lineno)4d] : %(message)s",
    level=logging.INFO,
    force=True,
)
logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
log = logging.getLogger()


config = DatabaseConfigurationHelper(log)
# DATABASE_URI = "postgresql+psycopg2://blueonion:labs@localhost:5432/blueonion_starlink"
print(config.database_uri)
engine = create_engine(config.database_uri, echo=False)
# engine = create_engine(DATABASE_URI, echo=False)
Base.metadata.create_all(engine)


## Ingest data
importer = JsonToRdbmsDataImporter(log, engine)
satellite_position_objects = importer.insert_json_data_into_table(
    data_file_path="data/starlink_historical_data.json", table=SatelliteLocations
)
