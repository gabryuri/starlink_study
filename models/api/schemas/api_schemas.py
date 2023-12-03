LAST_KNOWN_POS_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "object_id": {"type": "string"},
        "timestamp": {"type": "string"},
    },
    "required": ["object_id", "timestamp"],
}

CLOSEST_SATELLITE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "timestamp": {"type": "string"},
        "latitude": {"type": "number"},
        "longitude": {"type": "number"},
    },
    "required": ["timestamp", "latitude", "longitude"],
}
