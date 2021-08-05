Track package by carrier_code and tracking_number Documentation
===============================================================
[ShipEngine](www.shipengine.com) allows you to track a package for a given carrier and tracking number.

Please see [our docs](https://www.shipengine.com/docs/tracking/) to learn more about tracking shipments.


Input Parameters
----------------
The `track_pacakge_by_carrier_code_and_tracking_number` method requires the carrier code
and tracking number of the shipment being tracked.

Output
------
The `track_pacakge_by_carrier_code_and_tracking_number` method returns tracking information associated with the shipment for the carrier code and tracking number.


Example
=======
```python
import os

from shipengine import ShipEngine
from shipengine.errors import ShipEngineError


def track_package_by_carrier_code_and_tracking_number_demo():
    api_key = os.getenv("SHIPENGINE_API_KEY")

    shipengine = ShipEngine(
        {"api_key": api_key, "page_size": 75, "retries": 3, "timeout": 10}
    )

    try:
        result = shipengine.track_package_by_carrier_code_and_tracking_number(
            carrier_code="stamps_com", tracking_number="9405511899223197428490"
        )
        print("::SUCCESS::")
        print(result)
    except ShipEngineError as err:
        print("::ERROR::")
        print(err.to_json())


track_package_by_carrier_code_and_tracking_number_demo()
```

Example Output
==============
Tracking data for the shipment that corresponds to the tracking number provided.
```python
{
    "tracking_number": "9405511899223197428490",
    "tracking_url": "https://tools.usps.com/go/TrackConfirmAction.action?tLabels=9405511899223197428490",
    "status_code": "MY",
    "carrier_code": "stamps_com",
    "carrier_id": 1,
    "carrier_detail_code": None,
    "status_description": "Not Yet In System",
    "carrier_status_code": -2147219283,
    "carrier_status_description": "A status update is not yet available for this tracking number.  More information will become available when USPS receives the tracking information, or when the package is received by USPS.",
    "ship_date": "8/4/2021",
    "estimated_delivery_date": None,
    "actual_delivery_date": None,
    "exception_description": None,
    "events": [],
}
```

Exceptions
==========

- This method will only throw an exception that is an instance/extension of
  ([ShipEngineError](../shipengine/errors/__init__.py)) if there is a problem if a problem occurs, such as a network
  error or an error response from the API.
