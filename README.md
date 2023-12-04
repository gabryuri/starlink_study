# Starlink Historical Data Processor

## Usage 
to deploy this project, one can just use:

``` 
make deploy
 ```

Three containers will be created: 
1. Postgresql instance
2. Table initialization and Data import (ephemeral)
3. Flask application

>A chrome tab will also be opened (if you're in linux!)

## Querying data
> **Important:** Timestamp must be passed with the exact format  ` %Y-%m-%dT%H:%M:%S`
### Closest satellite
The closest satellite on a given moment can be queried through POST request against the  http://127.0.0.1:5000/closest_satellite route.

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
{
  "creation_date": "2021-01-26T06:26:10",
  "latitude": 1.1477942900869147,
  "longitude": 10,
  "object_id": "2020-055AE"
}
```
### Last known location 
The closest satellite on a given moment can be queried through POST request against the  http://127.0.0.1:5000/last_known_location route.

Example of expected input:
``` 
{
    "object_id": "2019-029AF",
    "timestamp": "2023-12-03T18:36:09"
}
```
Expected output: 
```
{
  "creation_date": "2021-01-26T06:26:10",
  "latitude": 1.1477942900869147,
  "longitude": 10,
  "object_id": "2020-055AE"
}
```

## Key Components
- **`initialize_db.py`**: Responsible for setting up the database table and triggering the data import process.
  - **Pydantic Modeling**: Located in `models/json_input/satellite_position.py`, it validates timestamps, latitude, and longitude, and creates POSTGIS-compatible points for ORM SQLAlchemy insertion.
- **`app.py` - Flask API**: The interface from which to query the data.
- **Data validation**: The interface from which to query the data.
- **PostGIS**: The interface from which to query the data.
  - This feature enables us to query the last known location **without** needing to use application logic to determine the closest satellite. 
- **ORM**: The interface from which to query the data.

## Code structure
### Models 
> Models were broadly used in this project. To enrich data being imported, as well as validating incoming request payloads. Additionally, ORM data models through SQLAlchemy were implemented.

- #### Json input

    Json inputs were validated and enriched. The main goals to implement this model were:
    - To validate the incoming data
    - Latitude between -90 and 90 degrees
    - Longitude between -180 and 180 degrees
    - To create custom columns to the final table
    - PostGIS Point column (lat/long)
    - check if both lat and long were present

  
- #### Database 

    Database modelling with SQLAlchemy enabled us to use ORM (Object-Relational Mapping).


- #### API models

    API Models specify both payload input models and api response models. Some of the validations implemented were:
    - Same Latitude and Longitude validations as in the input data.
    - Timestamp formatting

    Also, expected schemas for the incoming payloads were created, adding one more layer of validation.

### Scripts 

- #### Configuration
    Fetches environment variables and creates database URI. Also outputs custom error messages when environment variables are wrongfully set.

- #### Importer
    Makes use of the SQLAlchemy model to import data into an existing table.
- #### RDBMS fetcher 
    Fetches data from the Postgres instance using ORM based queries.

##  Flask API
The interface exposed is a simple, yet effective Flask API. Its Swagger can be used to query data from the two existing routes. 

# Final considerations 
- tests
- Not using initdb sql commands but ORM instead 
- modelling with pydantic 
  - for input validations and enrichment - tradeoffs with performance on the input or on the output 
- instead of harvesine, using PostGIS
  - no code in application side to solve for the closest satellite
