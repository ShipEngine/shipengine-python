Track package by Label ID Documentation
=======================================
[ShipEngine](www.shipengine.com) allows you to track a package by its ShipEngine `label_id`. This is the recommended
way to track shipments whose labels have been crated using ShipEngine API.

Please see [our docs](https://www.shipengine.com/docs/tracking/track-by-label-id/) to learn
more about tracking shipments.

Input
------
The `track_by_label_id` method requires the ID of the label associated with the shipment you are trying to track.
```python
label_id = "se-75492762"
```

Output
------
The `track_by_label_id` method returns tracking information associated with the shipment for the given label ID.

Example
=======
```python
import os

from shipengine import ShipEngine
from shipengine.errors import ShipEngineError


def track_by_label_id_demo():
    api_key = os.getenv("SHIPENGINE_API_KEY")

    shipengine = ShipEngine(
        {"api_key": api_key, "page_size": 75, "retries": 3, "timeout": 10}
    )
    label_id = "se-75492762"
    try:
        result = shipengine.track_package_by_label_id(label_id=label_id)
        print("::SUCCESS::")
        print(result)
    except ShipEngineError as err:
        print("::ERROR::")
        print(err.to_json())


track_by_label_id_demo()
```

Example Output
==============
```python
{
    "tracking_number": "1Z932R800392060079",
    "status_code": "DE",
    "status_description": "Delivered",
    "carrier_status_code": 1,
    "carrier_status_description": "Your item was delivered in or at the mailbox at 9:10 am on March",
    "ship_date": "2018-09-23T15:00:00.000Z",
    "estimated_delivery_date": "2018-09-23T15:00:00.000Z",
    "actual_delivery_date": "2018-09-23T15:00:00.000Z",
    "exception_description": "string",
    "events": [
        {
            "occurred_at": "2018-09-23T15:00:00.000Z",
            "carrier_occurred_at": "2018-09-23T15:00:00.000Z",
            "description": "Delivered, In/At Mailbox",
            "city_locality": "AUSTIN",
            "state_province": "TX",
            "postal_code": 78756,
            "country_code": "CA",
            "company_name": "Stamps.com",
            "signer": "string",
            "event_code": "string",
            "latitude": -90,
            "longitude": -180,
        }
    ],
}
```

Exceptions
==========

- This method will only throw an exception that is an instance/extension of
  ([ShipEngineError](../shipengine/errors/__init__.py)) if there is a problem if a problem occurs, such as a network
  error or an error response from the API.
