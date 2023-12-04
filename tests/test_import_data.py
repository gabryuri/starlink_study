import unittest
from unittest.mock import patch, MagicMock, mock_open
import json
import os
from scripts.importer.import_data import JsonToRdbmsDataImporter, SatelliteData, Base
from models.database.starlink_positions import SatelliteLocations
from sqlalchemy import Column, String, Float, Boolean, DateTime, PrimaryKeyConstraint
from pydantic import BaseModel


class MockTable(Base):
    __tablename__ = "mock_tbl"
    id = Column(Float)
    name = Column(Float)
    is_lat_long_complete = Column(Boolean)
    __table_args__ = (PrimaryKeyConstraint("id"),)


class MockModel(BaseModel):
    id: float
    name: str


def build_test_base_path():
    return "/".join(os.path.dirname(os.path.realpath(__file__)).split("/"))


class TestJsonToRdbmsDataImporter(unittest.TestCase):
    def setUp(self):
        self.mock_logger = MagicMock()
        self.mock_engine = MagicMock()
        self.batch_size = 5
        self.data_importer = JsonToRdbmsDataImporter(self.mock_logger, self.mock_engine, self.batch_size)

    @patch("scripts.importer.import_data.Session")
    @patch("scripts.importer.import_data.JsonToRdbmsDataImporter._JsonToRdbmsDataImporter__insert_data_to_rdbms")
    @patch("scripts.importer.import_data.JsonToRdbmsDataImporter._JsonToRdbmsDataImporter__instantiate_model_object")
    def test_should_insert_small_json_data_into_table(self, mock_instantiate_model, mock_insert_method, mock_session):
        self.data_importer.insert_json_data_into_table(
            f"{build_test_base_path()}/fixtures/valid_data.json", MockTable, MockModel
        )

        N = 2
        mock_insert_method.assert_called()
        self.assertEqual(mock_instantiate_model.call_count, N)

    @patch("scripts.importer.import_data.Session")
    @patch("scripts.importer.import_data.JsonToRdbmsDataImporter._JsonToRdbmsDataImporter__insert_data_to_rdbms")
    @patch("scripts.importer.import_data.JsonToRdbmsDataImporter._JsonToRdbmsDataImporter__instantiate_model_object")
    def test_should_insert_batched_data_into_table(self, mock_instantiate_model, mock_insert_method, mock_session):
        self.data_importer.insert_json_data_into_table(
            f"{build_test_base_path()}/fixtures/longer_valid_data.json", MockTable, MockModel
        )

        N = 18
        mock_insert_method.assert_called()
        self.assertEqual(mock_insert_method.call_count, 1 + (N // self.batch_size))
        self.assertEqual(mock_instantiate_model.call_count, 18)


if __name__ == "__main__":
    unittest.main()
