List Labels By Tracking Number Documentation
====================================
[ShipEngine](www.shipengine.com) allows you to get a list of labels using a tracking number.

Please see [our docs](https://www.shipengine.com/docs/reference/list-labels/) to learn more about listing labels.


Input Parameters
----------------
The `list_labels_by_tracking_number` method accepts a string that contains the tracking number of the desired label(s).


Output
------
The `list_labels_by_tracking_number` method returns a dictionary of the response from ShipEngine, including a list of labels with the inputted tracking number.


Example
=======
```python
import os

from shipengine import ShipEngine
from shipengine.errors import ShipEngineError


def list_labels_by_tracking_number_demo():
    api_key = os.getenv("SHIPENGINE_API_KEY")

    shipengine = ShipEngine(
        {"api_key": api_key, "page_size": 75, "retries": 3, "timeout": 10}
    )
    try:
        result = shipengine.list_labels_by_tracking_number(tracking_number="1ZXXXXXXXXXXXXXXXX")
        print("::SUCCESS::")
        print(result)
    except ShipEngineError as err:
        print("::ERROR::")
        print(err.to_json())


list_labels_by_tracking_number_demo()
```

Example Output
==============
```python
{
    "labels": [
        {
            "label_id": "se-92516364",
            "status": "completed",
            "shipment_id": "se-194998284",
            "external_shipment_id": "SEAuto-gYd5iXdyT0uvgfyLWAcfrA",
            "external_order_id": None,
            "ship_date": "2025-12-11T08:00:00Z",
            "created_at": "2025-12-11T21:06:39.307Z",
            "shipment_cost": {"currency": "usd", "amount": 95.41},
            "insurance_cost": {"currency": "usd", "amount": 0.0},
            "requested_comparison_amount": None,
            "rate_details": [
                {
                    "rate_detail_type": "shipping",
                    "carrier_description": "TransportationCharge",
                    "carrier_billing_code": None,
                    "carrier_memo": None,
                    "amount": {"currency": "usd", "amount": 95.410},
                    "billing_source": "carrier",
                }
            ],
            "tracking_number": "1ZXXXXXXXXXXXXXXXX",
            "is_return_label": False,
            "rma_number": None,
            "is_international": False,
            "batch_id": "",
            "carrier_id": "se-2815273",
            "service_code": "ups_ground",
            "package_code": "package",
            "voided": False,
            "voided_at": None,
            "label_format": "zpl",
            "display_scheme": "label",
            "label_layout": "4x6",
            "trackable": True,
            "label_image_id": None,
            "carrier_code": "ups",
            "carrier_weight": None,
            "confirmation": "none",
            "tracking_status": "in_transit",
            "label_download": {
                "href": "https://api.shipengine.com/v1/downloads/14/F9uiUwnwnEu0602g0lc_rw/label-92516364.zpl"
            },
            "form_download": None,
            "qr_code_download": None,
            "insurance_claim": None,
            "paperless_download": None,
            "packages": [
                {
                    "package_id": 72599271,
                    "package_code": "package",
                    "weight": {"value": 20.00, "unit": "pound"},
                    "dimensions": {
                        "unit": "inch",
                        "length": 24.00,
                        "width": 12.00,
                        "height": 6.00,
                    },
                    "insured_value": {"currency": "usd", "amount": 0.00},
                    "tracking_number": "1ZXXXXXXXXXXXXXXXX",
                    "label_download": {
                        "href": "https://api.shipengine.com/v1/downloads/14/_g6zkt9fs0us7Rrktmdpzw/labelpackage-72599271.zpl"
                    },
                    "qr_code_download": None,
                    "paperless_download": None,
                    "label_messages": {
                        "reference1": None,
                        "reference2": None,
                        "reference3": None,
                    },
                    "external_package_id": None,
                    "content_description": None,
                    "sequence": 1,
                    "alternative_identifiers": [],
                    "has_label_documents": False,
                    "has_form_documents": False,
                    "has_qr_code_documents": False,
                    "has_paperless_label_documents": False,
                },
                {
                    "package_id": 72599272,
                    "package_code": "package",
                    "weight": {"value": 10.00, "unit": "pound"},
                    "dimensions": {
                        "unit": "inch",
                        "length": 10.00,
                        "width": 10.00,
                        "height": 10.00,
                    },
                    "insured_value": {"currency": "usd", "amount": 0.00},
                    "tracking_number": "1ZXXXXXXXXXXXXXXXX",
                    "label_download": {
                        "href": "https://api.shipengine.com/v1/downloads/14/UTu1HZzgMkKSV-HXM16PPQ/labelpackage-72599272.zpl"
                    },
                    "qr_code_download": None,
                    "paperless_download": None,
                    "label_messages": {
                        "reference1": None,
                        "reference2": None,
                        "reference3": None,
                    },
                    "external_package_id": None,
                    "content_description": None,
                    "sequence": 2,
                    "alternative_identifiers": [],
                    "has_label_documents": False,
                    "has_form_documents": False,
                    "has_qr_code_documents": False,
                    "has_paperless_label_documents": False,
                },
            ],
            "charge_event": "carrier_default",
            "alternative_identifiers": [],
            "shipping_rule_id": None,
            "tracking_url": f"http://wwwapps.ups.com/WebTracking/processRequest?HTMLVersion=5.0&Requester=NES&AgreeToTermsAndConditions=yes&loc=en_US&tracknum=1ZXXXXXXXXXXXXXXXX",
            "ship_to": {
                "geolocation": [],
                "instructions": None,
                "name": "Jane Doe",
                "phone": None,
                "email": None,
                "company_name": None,
                "address_line1": "525 S Winchester Blvd",
                "address_line2": None,
                "address_line3": None,
                "city_locality": "San Jose",
                "state_province": "CA",
                "postal_code": "95128",
                "country_code": "US",
                "address_residential_indicator": "yes",
            },
        }
    ],
    "total": 1,
    "page": 1,
    "pages": 1,
    "links": {
        "first": {
            "href": f"https://api.shipengine.com/v1/labels?tracking_number=1ZXXXXXXXXXXXXXXXX&page=1&page_size=25"
        },
        "last": {
            "href": f"https://api.shipengine.com/v1/labels?tracking_number=1ZXXXXXXXXXXXXXXXX&page=1&page_size=25"
        },
        "prev": {},
        "next": {},
    },
}
```

Exceptions
==========

- This method will only throw an exception that is an instance/extension of
  ([ShipEngineError](../shipengine/errors/__init__.py)) if there is a problem if a problem occurs, such as a network
  error or an error response from the API.
