# Starlink Historical Data Processor

## Usage 
to deploy this project, one can just use:

``` 
make deploy
 ```

Three containers will be created: 
1. Postgresql instance
2. Data import and table initialization (ephemeral)
3. Flask application

>A chrome tab will also be opened (if you're on linux!)

## Querying data

### Closest satellite
The closest satellite on a given moment can be queried through POST request against the  http://127.0.0.1:5000/closest_satellite endpoint.

Example of expected input:
``` 
{
    "timestamp": "2021-01-26T06:26:10",
    "latitude": 0.3,
    "longitude": 10
}
```
Expected output: 
```
ADD EXPECTED OUTPUT!
```
### Last known location 
The closest satellite on a given moment can be queried through POST request against the  http://127.0.0.1:5000/last_known_location endpoint.

Example of expected input:
``` 
{
    "object_id": "2019-029AF",
    "timestamp": "2020-09-16T18:36:09"
}
```
Expected output: 
```
ADD EXPECTED OUTPUT!
```
## Key Components
- **`initialize_db.py`**: Responsible for setting up the database table and triggering the data import process.
  - **Pydantic Modeling**: Located in `models/json_input/satellite_position.py`, it validates timestamps, latitude, and longitude, and creates POSTGIS-compatible points for ORM SQLAlchemy insertion.
- **`app.py` - Flask API**: The interface from which to query the data.
- **Data validation**: The interface from which to query the data.
- **PostGIS**: The interface from which to query the data.
- **ORM**: The interface from which to query the data.

## Code structure
### Models 
> Models were broadly used in this project. To enrich data being imported, as well as validating incoming request payloads, as well as ORM data models through SQLAlchemy.
#### API models

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce fringilla cursus orci vitae condimentum. Sed ultricies est vel tellus faucibus iaculis. In pretium gravida posuere. Suspendisse potenti. Nam at orci augue. Nunc et aliquam libero, et iaculis metus. Integer id malesuada elit. Curabitur mattis tellus sollicitudin eros ultricies vestibulum. In vitae mollis massa, a viverra ligula. Duis egestas nunc eget tempus dignissim. Suspendisse et consectetur lorem. Ut ornare malesuada suscipit. Maecenas hendrerit pretium odio sed iaculis.
#### Database 

 Curabitur mattis tellus sollicitudin eros ultricies vestibulum. In vitae mollis massa, a viverra ligula. Duis egestas nunc eget tempus dignissim. Suspendisse et consectetur lorem. Ut ornare malesuada suscipit. Maecenas hendrerit pretium odio sed iaculis.
#### Json input
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce fringilla cursus orci vitae condimentum. Sed ultricies est vel tellus faucibus iaculis. In pretium gravida posuere. Suspendisse potenti. Nam at orci augue. Nunc et aliquam libero, et iaculis metus. Integer id malesuada elit.

### Scripts 

#### Configuration
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce fringilla cursus orci vitae condimentum. Sed ultricies est vel tellus faucibus iaculis. In pretium gravida posuere. Suspendisse potenti. Nam at orci augue. Nunc et aliquam libero, et iaculis metus. Integer id malesuada elit.
#### Importer
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce fringilla cursus orci vitae condimentum. Sed ultricies est vel tellus faucibus iaculis. In pretium gravida posuere. Suspendisse potenti. Nam at orci augue. Nunc et aliquam libero, et iaculis metus. Integer id malesuada elit.
#### RDBMS fetcher 
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce fringilla cursus orci vitae condimentum. Sed ultricies est vel tellus faucibus iaculis. In pretium gravida posuere. Suspendisse potenti. Nam at orci augue. Nunc et aliquam libero, et iaculis metus. Integer id malesuada elit.
##  Flask API

# Final considerations 
## tests
## Not using initdb sql commands but ORM instead 
## modelling with pydantic 
    for input validations and enrichment - tradeoffs with performance on the input or on the 
## instead of harvesine, using PostGIS


<!-- 
## other 
4. usage
5. querying data
6. explaining Models
     3.1 api models (pydantic validations for the API inputs)
          3.1.1 api schemas (for input requirements)
     3.2 database models (SQLAlchemy for ORM)
     3.3 json_input models (Pydantic validations and enrichment)

7. explaining scripts
     4.1 configuration
     4.2 importer
     4.3 rdbms_fetcher
8. explaining Flask application
     5.1 app.py
9.  tests
10. Makefile
11. Considerations 
     8.1 Not using initdb sql commands but ORM instead 
     8.2 modelling with pydantic for input validations and enrichment - tradeoffs with performance on the input or on the output
     8.3 instead of harvesine, using PostGIS
     8.4 losing precision when using float -->
## Overview
This project processes historical data of Starlink satellites, reading from `data/starlink_historical_data.json` and using SQLAlchemy along with GeoAlchemy2 to create a database table. The table is populated with the object ID, creation date, latitude, longitude, and a point combining latitude and longitude.

## Key Components
- **`initialize_db.py`**: Responsible for setting up the database and triggering the data import process.
- **`JsonToRdbmsDataImporter`**: A class in `scripts/importer/import_data.py` that handles the conversion of JSON data to RDBMS format.
- **Pydantic Modeling**: Located in `models/json_input/satellite_position.py`, it validates timestamps, latitude, and longitude, and creates points for ORM SQLAlchemy insertion.
- **Data Modeling**: The data model for the Starlink positions is defined in `models/database/starlink_positions.py`, using SQLAlchemy.

## Features
- **Data Import**: The `initialize-db` container service, defined in the Docker compose setup, executes `initialize_db.py` to start the data import process.
- **Data Validation**: The input data from the JSON file is validated for timestamp format and geographical coordinate validity.
- **Efficient Data Handling**: Latitude and longitude are stored both as separate fields and as a combined point object. While the point object is convenient for distance calculations, separate fields simplify data presentation.
- **Logging**: Extensive logging throughout the data processing steps, including SQLAlchemy operations.

## How it Works
1. **Database Setup**: The `initialize_db.py` script creates the necessary database schema using SQLAlchemy and GeoAlchemy2.
2. **Data Ingestion**: The `JsonToRdbmsDataImporter` class reads the JSON data, validates it, and then batches the data for insertion into the PostgreSQL database.
3. **Insertion Logic**: The data is inserted using SQLAlchemy's `insert` method with a conflict handling strategy, ensuring efficient and error-free data insertion.

## Configuration
- Database configurations are fetched using a configuration helper class, ensuring flexibility and ease of maintenance.

## Usage
To start the project, run the Docker compose command, which will set up the necessary services, including the database and the `initialize-db` service for initializing the database with the historical data.

```bash
docker-compose up -d
