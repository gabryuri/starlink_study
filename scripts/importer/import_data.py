from typing import Type

import ijson
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.inspection import inspect
from pydantic import BaseModel

from models.database.starlink_positions import Base


class JsonToRdbmsDataImporter:
    """
    This class is responsible for importing JSON data into a relational database management system (RDBMS).
    It reads JSON data from a file, converts it into model objects,
    and then inserts the data into a specified database table in batches.

    Inputs:
        logger (Logger): A logging object for capturing the activities of the data importer.
        engine (Engine): A SQLAlchemy engine object for database connection and operations.
        batch_size (int): The number of records to be inserted in a single batch.

    Methods:
        import_json_data_into_table: Parses JSON data and handles the batch inserts.
        __insert_data_to_rdbms: Performs the actual insertion of data into the RDBMS.
        __instantiate_model_object: Instantiates a Pydantic model object from a dictionary.
        __fetch_table_primary_key: Retrieves the primary key(s) of a given table.

    """

    def __init__(self, logger, engine, batch_size=300) -> None:
        self.logger = logger
        self.engine = engine
        self.batch_size = batch_size

        self.session = Session(bind=self.engine)

    def import_json_data_into_table(self, data_file_path: str, table: Type[Base], model: BaseModel) -> None:
        """
        Parses JSON data from a file using Pydantic models and handles the batched
        insertion into a specified database table.

        Parameters:
            data_file_path (str): The file path of the JSON data file.
            table (Type[Base]): The SQLAlchemy table class into which data will be inserted.
            model (BaseModel): The Pydantic model that represents the structure of the data.

        Returns:
            None
        """
        self.logger.info(f"Beginning to parse {data_file_path} json elements.")
        with open(data_file_path, "r") as json_file:
            json_content = ijson.items(json_file, "item")

            values_to_insert = []
            total_records = 0
            for element in json_content:
                satellite_obj = self.__instantiate_model_object(model, element)
                values_to_insert.append(satellite_obj.dict())

                total_records += 1

                if len(values_to_insert) >= self.batch_size:
                    self.logger.info(f"inserting, {len(values_to_insert)} records, index {total_records}")
                    self.__insert_data_to_rdbms(table, values_to_insert)
                    values_to_insert = []

            self.logger.info(f"inserted remaining {len(values_to_insert)} records, total of {total_records} records.")
            self.__insert_data_to_rdbms(table, values_to_insert)

    def __insert_data_to_rdbms(self, table: Type[Base], values_to_insert: list[dict]) -> None:
        """
        Inserts a list of dictionary values into the specified table in the database.
        It also fetches the primary key to be able to use the ON CONFICT DO NOTHING statement.

        Parameters:
            table (Type[Base]): The SQLAlchemy table class into which data will be inserted.
            values_to_insert (list[dict]): A list of dictionaries representing the records to be inserted.

        Returns:
            None
        """
        primary_keys = self.__fetch_table_primary_key(table)

        insert_stmt = insert(table).values(values_to_insert)
        conflict_stmt = insert_stmt.on_conflict_do_nothing(index_elements=primary_keys)
        self.session.execute(conflict_stmt)
        self.session.commit()

    def __instantiate_model_object(self, model: BaseModel, element: dict) -> BaseModel:
        """
        Instantiates a model object from a dictionary.

        Parameters:
            model (BaseModel): The Pydantic model class to instantiate.
            element (dict): The dictionary from which the model is to be instantiated.

        Returns:
            BaseModel: An instance of the specified Pydantic model.
        """
        satellite_obj = model.model_validate(element)
        return satellite_obj

    def __fetch_table_primary_key(self, table: Type[Base]) -> list[str]:
        """
        Fetches the primary key(s) of a specified table.

        Parameters:
            table (Type[Base]): The SQLAlchemy table class whose primary keys are to be fetched.

        Returns:
            list[str]: A list of primary key column names for the specified table.
        """
        primary_keys = [key.name for key in inspect(table).primary_key]
        return primary_keys
