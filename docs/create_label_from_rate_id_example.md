Create Label From Rate ID Documentation
=======================================
When retrieving rates for shipments using the `get_rates_from_shipment` method, the returned information contains a `rate_id` property that can be used to purchase a label without having to refill in the shipment information repeatedly.

Please see [our docs](https://www.shipengine.com/docs/labels/create-from-rate/) to learn more about creating shipping labels from rates.

Input Parameters
----------------
The `create_label_from_rate_id` method accepts a valid `rate_id` and a dictionary of label params that
will dictate the label display and level of verification.
```python
params = {
    "validate_address": "no_validation",
    "label_layout": "4x6",
    "label_format": "pdf",
    "label_download_type": "url",
    "display_scheme": "label",
}
```

Output
------
The `create_label_from_rate_id` method returns a shipping label that corresponds to the
shipping and rate details encapsulated in the `rate_id` passed in.

Example:
========

```python
import os

from shipengine import ShipEngine
from shipengine.errors import ShipEngineError


def create_label_from_rate_id_demo():
    api_key = os.getenv("SHIPENGINE_API_KEY")

    shipengine = ShipEngine(
        {"api_key": api_key, "page_size": 75, "retries": 3, "timeout": 10}
    )

    try:
        params = {
            "validate_address": "no_validation",
            "label_layout": "4x6",
            "label_format": "pdf",
            "label_download_type": "url",
            "display_scheme": "label",
        }
        result = shipengine.create_label_from_rate_id_id(
            rate_id="se-799373193", params=params
        )
        print("::SUCCESS::")
        p.pprint(result)
    except ShipEngineError as err:
        print("::ERROR::")
        print(err.to_json())


create_label_from_rate_id_demo()
```

Example Output:
===============
- Successful `create_label_from_rate_id()` result.
```python
{
    "batch_id": "",
    "carrier_code": "stamps_com",
    "carrier_id": "se-656171",
    "charge_event": "carrier_default",
    "created_at": "2021-08-05T16:47:47.8768838Z",
    "display_scheme": "label",
    "form_download": None,
    "insurance_claim": None,
    "insurance_cost": {"amount": 0.0, "currency": "usd"},
    "is_international": False,
    "is_return_label": False,
    "label_download": {
        "href": "https://api.shipengine.com/v1/downloads/10/_EKGeA4yuEuLzLq81iOzew/label-75693596.pdf",
        "pdf": "https://api.shipengine.com/v1/downloads/10/_EKGeA4yuEuLzLq81iOzew/label-75693596.pdf",
        "png": "https://api.shipengine.com/v1/downloads/10/_EKGeA4yuEuLzLq81iOzew/label-75693596.png",
        "zpl": "https://api.shipengine.com/v1/downloads/10/_EKGeA4yuEuLzLq81iOzew/label-75693596.zpl",
    },
    "label_format": "pdf",
    "label_id": "se-75693596",
    "label_image_id": None,
    "label_layout": "4x6",
    "package_code": "package",
    "packages": [
        {
            "dimensions": {"height": 0.0, "length": 0.0, "unit": "inch", "width": 0.0},
            "external_package_id": None,
            "insured_value": {"amount": 0.0, "currency": "usd"},
            "label_messages": {
                "reference1": None,
                "reference2": None,
                "reference3": None,
            },
            "package_code": "package",
            "package_id": 80328023,
            "sequence": 1,
            "tracking_number": "9400111899560334651289",
            "weight": {"unit": "ounce", "value": 1.0},
        }
    ],
    "rma_number": None,
    "service_code": "usps_first_class_mail",
    "ship_date": "2021-08-05T00:00:00Z",
    "shipment_cost": {"amount": 3.35, "currency": "usd"},
    "shipment_id": "se-144794216",
    "status": "completed",
    "trackable": True,
    "tracking_number": "9400111899560334651289",
    "tracking_status": "in_transit",
    "voided": False,
    "voided_at": None,
}
```

Exceptions
==========

- This method will only throw an exception that is an instance/extension of
  ([ShipEngineError](../shipengine/errors/__init__.py)) if there is a problem if a problem occurs, such as a network
  error or an error response from the API.
