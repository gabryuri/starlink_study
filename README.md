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

>A chrome tab will also be opened (if you're on linux!)

## Querying data

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
    "timestamp": "2020-09-16T18:36:09"
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
