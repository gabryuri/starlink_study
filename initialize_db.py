import logging

from sqlalchemy import create_engine

from scripts.configuration.database import DatabaseConfigurationHelper
from scripts.importer.import_data import JsonToRdbmsDataImporter
from models.database.starlink_positions import SatelliteLocations, Base
from models.json_input.satellite_position import SatelliteData

logging.basicConfig(
    format="[%(levelname)s] [%(asctime)s][%(filename)-15s][%(lineno)4d] : %(message)s",
    level=logging.INFO,
    force=True,
)
logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
log = logging.getLogger()

config = DatabaseConfigurationHelper(log)
engine = create_engine(config.database_uri, echo=False)
Base.metadata.create_all(engine)

## Ingest data
importer = JsonToRdbmsDataImporter(log, engine)
satellite_position_objects = importer.import_json_data_into_table(
    data_file_path="data/starlink_historical_data.json", table=SatelliteLocations, model=SatelliteData
)
