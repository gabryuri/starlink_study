import unittest
from unittest.mock import patch, MagicMock
import os
from scripts.configuration.database import DatabaseConfigurationHelper, load_required_env


class TestConfiguration(unittest.TestCase):
    # Defining Mock env vars
    mock_env_vars = {
        "POSTGRES_USER": "gabe",
        "POSTGRES_PASSWORD": "gabe_pw",
        "POSTGRES_PORT": "5432",
        "POSTGRES_DB": "testdb",
        "POSTGRES_HOST": "localhost",
    }

    def setUp(self):
        self.logger = MagicMock()

    @patch.dict(os.environ, {}, clear=True)
    def test_should_fail_when_missing_env_var(self):
        with self.assertRaises(DatabaseConfigurationHelper.NecessaryParameterMissing):
            load_required_env("POSTGRES_USER")

    @patch.dict(os.environ, {"POSTGRES_USER": ""}, clear=True)
    def test_should_fail_when_empty_env_var(self):
        with self.assertRaises(DatabaseConfigurationHelper.NecessaryParameterMissing):
            load_required_env("POSTGRES_USER")

    @patch.dict(os.environ, mock_env_vars)
    def test_should_load_required_env_when_set(self):
        self.assertEqual(load_required_env("POSTGRES_USER"), "gabe")

    @patch.dict(os.environ, mock_env_vars)
    def test_should_create_database_uri_correctly(self):
        config_helper = DatabaseConfigurationHelper(self.logger)
        expected_uri = "postgresql+psycopg2://gabe:gabe_pw@localhost:5432/testdb"
        self.assertEqual(config_helper.database_uri, expected_uri)

    @patch.dict(os.environ, {}, clear=True)
    def test_configuration_should_fail_when_missing_env_vars(self):
        with self.assertRaises(DatabaseConfigurationHelper.NecessaryParameterMissing):
            DatabaseConfigurationHelper(self.logger)


if __name__ == "__main__":
    unittest.main()
