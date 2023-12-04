from typing import Type

import ijson
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.inspection import inspect
from pydantic import BaseModel

from models.database.starlink_positions import Base

class JsonToRdbmsDataImporter:
    def __init__(self, logger, engine, batch_size=300) -> None:
        self.logger = logger
        self.batch_size = batch_size
        self.engine = engine
        self.session = Session(bind=self.engine)

    def insert_json_data_into_table(self, data_file_path: str, table: Type[Base], model: BaseModel) -> None:
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
        primary_keys = self.__fetch_table_primary_key(table)

        insert_stmt = insert(table).values(values_to_insert)
        conflict_stmt = insert_stmt.on_conflict_do_nothing(index_elements=primary_keys)
        self.session.execute(conflict_stmt)
        self.session.commit()

    def __instantiate_model_object(self, model: BaseModel, element: dict) -> BaseModel:
        satellite_obj = model.model_validate(element)
        return satellite_obj

    def __fetch_table_primary_key(self, table: Type[Base]) -> list[str]:
        primary_keys = [key.name for key in inspect(table).primary_key]
        return primary_keys
