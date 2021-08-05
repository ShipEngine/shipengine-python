Create Label From Rate Documentation
====================================
When retrieving rates for shipments using the `get_rates_from_shipment` method, the returned information contains a `rate_id` property that can be used to purchase a label without having to refill in the shipment information repeatedly.

Please see [our docs](https://www.shipengine.com/docs/labels/create-from-rate/) to learn more about creating shipping labels from rates.

Input Parameters
----------------
The `create_label_from_rate` method accepts a valid `rate_id` and a dictionary of label params that
will dictate the label display and level of verification.
```python
shipment = {
    "shipment": {
        "service_code": "ups_ground",
        "ship_to": {
            "name": "Jane Doe",
            "address_line1": "525 S Winchester Blvd",
            "city_locality": "San Jose",
            "state_province": "CA",
            "postal_code": "95128",
            "country_code": "US",
            "address_residential_indicator": "yes",
        },
        "ship_from": {
            "name": "John Doe",
            "company_name": "Example Corp",
            "phone": "555-555-5555",
            "address_line1": "4009 Marathon Blvd",
            "city_locality": "Austin",
            "state_province": "TX",
            "postal_code": "78756",
            "country_code": "US",
            "address_residential_indicator": "no",
        },
        "packages": [
            {
                "weight": {"value": 20, "unit": "ounce"},
                "dimensions": {"height": 6, "width": 12, "length": 24, "unit": "inch"},
            }
        ],
    }
}
```

Output
------
The `create_label_from_shipment` method returns a shipping label that corresponds to
the shipping details passed in.

Example:
========
```python
import os

from shipengine import ShipEngine
from shipengine.errors import ShipEngineError


def create_label_from_shipment_demo():
    api_key = os.getenv("SHIPENGINE_API_KEY")

    shipengine = ShipEngine(
        {"api_key": api_key, "page_size": 75, "retries": 3, "timeout": 10}
    )
    try:
        shipment = {
            "shipment": {
                "service_code": "ups_ground",
                "ship_to": {
                    "name": "Jane Doe",
                    "address_line1": "525 S Winchester Blvd",
                    "city_locality": "San Jose",
                    "state_province": "CA",
                    "postal_code": "95128",
                    "country_code": "US",
                    "address_residential_indicator": "yes",
                },
                "ship_from": {
                    "name": "John Doe",
                    "company_name": "Example Corp",
                    "phone": "555-555-5555",
                    "address_line1": "4009 Marathon Blvd",
                    "city_locality": "Austin",
                    "state_province": "TX",
                    "postal_code": "78756",
                    "country_code": "US",
                    "address_residential_indicator": "no",
                },
                "packages": [
                    {
                        "weight": {"value": 20, "unit": "ounce"},
                        "dimensions": {
                            "height": 6,
                            "width": 12,
                            "length": 24,
                            "unit": "inch",
                        },
                    }
                ],
            }
        }
        result = shipengine.create_label_from_shipment(shipment=shipment)
        print("::SUCCESS::")
        print(result)
    except ShipEngineError as err:
        print("::ERROR::")
        print(err.to_json())


create_label_from_shipment_demo()
```

Example Output:
===============
- Successful `create_label_from_shipment()` result that contains label data that corresponds to the shipment details provided.
```python
{
    "label_id": "se-75714944",
    "status": "completed",
    "shipment_id": "se-144835189",
    "ship_date": "2021-08-05T00:00:00Z",
    "created_at": "2021-08-05T18:01:46.0013168Z",
    "shipment_cost": {"currency": "usd", "amount": 27.98},
    "insurance_cost": {"currency": "usd", "amount": 0.0},
    "tracking_number": "1Z63R0960311549776",
    "is_return_label": False,
    "rma_number": None,
    "is_international": False,
    "batch_id": "",
    "carrier_id": "se-656172",
    "service_code": "ups_ground",
    "package_code": "package",
    "voided": False,
    "voided_at": None,
    "label_format": "pdf",
    "display_scheme": "label",
    "label_layout": "4x6",
    "trackable": True,
    "label_image_id": None,
    "carrier_code": "ups",
    "tracking_status": "in_transit",
    "label_download": {
        "pdf": "https://api.shipengine.com/v1/downloads/10/nRpNbEgTzkaBB1HitZNfjQ/label-75714944.pdf",
        "png": "https://api.shipengine.com/v1/downloads/10/nRpNbEgTzkaBB1HitZNfjQ/label-75714944.png",
        "zpl": "https://api.shipengine.com/v1/downloads/10/nRpNbEgTzkaBB1HitZNfjQ/label-75714944.zpl",
        "href": "https://api.shipengine.com/v1/downloads/10/nRpNbEgTzkaBB1HitZNfjQ/label-75714944.pdf",
    },
    "form_download": None,
    "insurance_claim": None,
    "packages": [
        {
            "package_id": 80350838,
            "package_code": "package",
            "weight": {"value": 20.0, "unit": "ounce"},
            "dimensions": {
                "unit": "inch",
                "length": 24.0,
                "width": 12.0,
                "height": 6.0,
            },
            "insured_value": {"currency": "usd", "amount": 0.0},
            "tracking_number": "1Z63R0960311549776",
            "label_messages": {
                "reference1": None,
                "reference2": None,
                "reference3": None,
            },
            "external_package_id": None,
            "sequence": 1,
        }
    ],
    "charge_event": "carrier_default",
}
```

Exceptions
==========

- This method will only throw an exception that is an instance/extension of
  ([ShipEngineError](../shipengine/errors/__init__.py)) if there is a problem if a problem occurs, such as a network
  error or an error response from the API.
