Get Rate Estimate Documentation
================================
Get a rate estimate for a shipment given a minimal set of shipment details. Unlike
`get_rates_from_shipment`, this method does not require a full shipment object, making
it ideal for quickly comparing rates across carriers before committing to a shipment.

Please see [our docs](https://www.shipengine.com/docs/rates/estimate/) to learn more about
estimating rates.

> **Note:** Rate estimates do not include all possible charges such as fuel surcharges,
> customs fees, or other carrier-imposed fees. Actual rates may differ when purchasing a label.

Input Parameters
----------------
The `get_rate_estimate` method accepts a dictionary of rate estimate params as seen below.
```python
params = {
    "carrier_ids": ["se-656171"],
    "from_country_code": "US",
    "from_postal_code": "78756",
    "from_city_locality": "Austin",
    "from_state_province": "TX",
    "to_country_code": "US",
    "to_postal_code": "95128",
    "to_city_locality": "San Jose",
    "to_state_province": "CA",
    "weight": {
        "value": 1.0,
        "unit": "ounce",
    },
    "dimensions": {
        "unit": "inch",
        "length": 5.0,
        "width": 5.0,
        "height": 5.0,
    },
}
```

Output
------
The `get_rate_estimate` method returns a list of rate estimates from the specified carriers.

Example:
========
- Pass in a dictionary of params you wish to fetch rate estimates for.
```python
import os

from shipengine import ShipEngine
from shipengine.errors import ShipEngineError


def get_rate_estimate_demo():
    api_key = os.getenv("SHIPENGINE_API_KEY")

    shipengine = ShipEngine(
        {"api_key": api_key, "page_size": 75, "retries": 3, "timeout": 10}
    )

    try:
        params = {
            "carrier_ids": ["se-656171"],
            "from_country_code": "US",
            "from_postal_code": "78756",
            "from_city_locality": "Austin",
            "from_state_province": "TX",
            "to_country_code": "US",
            "to_postal_code": "95128",
            "to_city_locality": "San Jose",
            "to_state_province": "CA",
            "weight": {
                "value": 1.0,
                "unit": "ounce",
            },
            "dimensions": {
                "unit": "inch",
                "length": 5.0,
                "width": 5.0,
                "height": 5.0,
            },
        }
        result = shipengine.get_rate_estimate(params=params)
        print("::SUCCESS::")
        print(result)
    except ShipEngineError as err:
        print("::ERROR::")
        print(err.to_json())


get_rate_estimate_demo()
```

Example Output:
===============
- Successful `get_rate_estimate()` result.
```python
[
    {
        "rate_type": "check",
        "carrier_id": "se-656171",
        "shipping_amount": {"currency": "usd", "amount": 20.59},
        "insurance_amount": {"currency": "usd", "amount": 0.0},
        "confirmation_amount": {"currency": "usd", "amount": 0.0},
        "other_amount": {"currency": "usd", "amount": 6.38},
        "requested_comparison_amount": {"currency": "usd", "amount": 0.0},
        "rate_details": [
            {
                "rate_detail_type": "shipping",
                "carrier_description": "Shipping",
                "carrier_billing_code": "BaseServiceCharge",
                "carrier_memo": None,
                "amount": {"currency": "usd", "amount": 20.59},
                "billing_source": "Carrier",
            },
            {
                "rate_detail_type": "fuel_charge",
                "carrier_description": "Fuel Surcharge",
                "carrier_billing_code": "375",
                "carrier_memo": None,
                "amount": {"currency": "usd", "amount": 6.38},
                "billing_source": "Carrier",
            },
        ],
        "zone": None,
        "package_type": None,
        "carrier_weight": None,
        "delivery_days": 2,
        "guaranteed_service": True,
        "estimated_delivery_date": "2026-04-15T23:00:00Z",
        "carrier_delivery_days": "Wednesday 4/15 by 11:00 PM",
        "ship_date": "2026-04-13T00:00:00Z",
        "negotiated_rate": True,
        "service_type": "UPS 2nd Day Air®",
        "service_code": "ups_2nd_day_air",
        "trackable": True,
        "carrier_code": "ups",
        "carrier_nickname": "UPS",
        "carrier_friendly_name": "UPS",
        "display_scheme": None,
        "validation_status": "unknown",
        "warning_messages": [],
        "error_messages": [],
    },
    {
        "rate_type": "check",
        "carrier_id": "se-656171",
        "shipping_amount": {"currency": "usd", "amount": 23.58},
        "insurance_amount": {"currency": "usd", "amount": 0.0},
        "confirmation_amount": {"currency": "usd", "amount": 0.0},
        "other_amount": {"currency": "usd", "amount": 7.31},
        "requested_comparison_amount": {"currency": "usd", "amount": 0.0},
        "rate_details": [
            {
                "rate_detail_type": "shipping",
                "carrier_description": "Shipping",
                "carrier_billing_code": "BaseServiceCharge",
                "carrier_memo": None,
                "amount": {"currency": "usd", "amount": 23.58},
                "billing_source": "Carrier",
            },
            {
                "rate_detail_type": "fuel_charge",
                "carrier_description": "Fuel Surcharge",
                "carrier_billing_code": "375",
                "carrier_memo": None,
                "amount": {"currency": "usd", "amount": 7.31},
                "billing_source": "Carrier",
            },
        ],
        "zone": None,
        "package_type": None,
        "carrier_weight": None,
        "delivery_days": 2,
        "guaranteed_service": True,
        "estimated_delivery_date": "2026-04-15T10:30:00Z",
        "carrier_delivery_days": "Wednesday 4/15 by 10:30 AM",
        "ship_date": "2026-04-13T00:00:00Z",
        "negotiated_rate": True,
        "service_type": "UPS 2nd Day Air AM®",
        "service_code": "ups_2nd_day_air_am",
        "trackable": True,
        "carrier_code": "ups",
        "carrier_nickname": "UPS",
        "carrier_friendly_name": "UPS",
        "display_scheme": None,
        "validation_status": "unknown",
        "warning_messages": [],
        "error_messages": [],
    },
    {
        "rate_type": "check",
        "carrier_id": "se-656171",
        "shipping_amount": {"currency": "usd", "amount": 16.46},
        "insurance_amount": {"currency": "usd", "amount": 0.0},
        "confirmation_amount": {"currency": "usd", "amount": 0.0},
        "other_amount": {"currency": "usd", "amount": 5.10},
        "requested_comparison_amount": {"currency": "usd", "amount": 0.0},
        "rate_details": [
            {
                "rate_detail_type": "shipping",
                "carrier_description": "Shipping",
                "carrier_billing_code": "BaseServiceCharge",
                "carrier_memo": None,
                "amount": {"currency": "usd", "amount": 16.46},
                "billing_source": "Carrier",
            },
            {
                "rate_detail_type": "fuel_charge",
                "carrier_description": "Fuel Surcharge",
                "carrier_billing_code": "375",
                "carrier_memo": None,
                "amount": {"currency": "usd", "amount": 5.10},
                "billing_source": "Carrier",
            },
        ],
        "zone": None,
        "package_type": None,
        "carrier_weight": None,
        "delivery_days": 3,
        "guaranteed_service": True,
        "estimated_delivery_date": "2026-04-16T23:00:00Z",
        "carrier_delivery_days": "Thursday 4/16 by 11:00 PM",
        "ship_date": "2026-04-13T00:00:00Z",
        "negotiated_rate": True,
        "service_type": "UPS 3 Day Select®",
        "service_code": "ups_3_day_select",
        "trackable": True,
        "carrier_code": "ups",
        "carrier_nickname": "UPS",
        "carrier_friendly_name": "UPS",
        "display_scheme": None,
        "validation_status": "unknown",
        "warning_messages": [],
        "error_messages": [],
    },
    {
        "rate_type": "check",
        "carrier_id": "se-656171",
        "shipping_amount": {"currency": "usd", "amount": 9.94},
        "insurance_amount": {"currency": "usd", "amount": 0.0},
        "confirmation_amount": {"currency": "usd", "amount": 0.0},
        "other_amount": {"currency": "usd", "amount": 0.0},
        "requested_comparison_amount": {"currency": "usd", "amount": 0.0},
        "rate_details": [
            {
                "rate_detail_type": "shipping",
                "carrier_description": "Shipping",
                "carrier_billing_code": "BaseServiceCharge",
                "carrier_memo": None,
                "amount": {"currency": "usd", "amount": 9.94},
                "billing_source": "Carrier",
            },
        ],
        "zone": None,
        "package_type": None,
        "carrier_weight": None,
        "delivery_days": 4,
        "guaranteed_service": True,
        "estimated_delivery_date": "2026-04-17T23:00:00Z",
        "carrier_delivery_days": "Friday 4/17 by 11:00 PM",
        "ship_date": "2026-04-13T00:00:00Z",
        "negotiated_rate": True,
        "service_type": "UPS® Ground",
        "service_code": "ups_ground",
        "trackable": True,
        "carrier_code": "ups",
        "carrier_nickname": "UPS",
        "carrier_friendly_name": "UPS",
        "display_scheme": None,
        "validation_status": "unknown",
        "warning_messages": [],
        "error_messages": [],
    },
    {
        "rate_type": "check",
        "carrier_id": "se-656171",
        "shipping_amount": {"currency": "usd", "amount": 50.66},
        "insurance_amount": {"currency": "usd", "amount": 0.0},
        "confirmation_amount": {"currency": "usd", "amount": 0.0},
        "other_amount": {"currency": "usd", "amount": 15.71},
        "requested_comparison_amount": {"currency": "usd", "amount": 0.0},
        "rate_details": [
            {
                "rate_detail_type": "shipping",
                "carrier_description": "Shipping",
                "carrier_billing_code": "BaseServiceCharge",
                "carrier_memo": None,
                "amount": {"currency": "usd", "amount": 50.66},
                "billing_source": "Carrier",
            },
            {
                "rate_detail_type": "fuel_charge",
                "carrier_description": "Fuel Surcharge",
                "carrier_billing_code": "375",
                "carrier_memo": None,
                "amount": {"currency": "usd", "amount": 15.71},
                "billing_source": "Carrier",
            },
        ],
        "zone": None,
        "package_type": None,
        "carrier_weight": None,
        "delivery_days": 1,
        "guaranteed_service": True,
        "estimated_delivery_date": "2026-04-14T10:30:00Z",
        "carrier_delivery_days": "Tomorrow by 10:30 AM",
        "ship_date": "2026-04-13T00:00:00Z",
        "negotiated_rate": True,
        "service_type": "UPS Next Day Air®",
        "service_code": "ups_next_day_air",
        "trackable": True,
        "carrier_code": "ups",
        "carrier_nickname": "UPS",
        "carrier_friendly_name": "UPS",
        "display_scheme": None,
        "validation_status": "unknown",
        "warning_messages": [],
        "error_messages": [],
    },
    {
        "rate_type": "check",
        "carrier_id": "se-656171",
        "shipping_amount": {"currency": "usd", "amount": 142.57},
        "insurance_amount": {"currency": "usd", "amount": 0.0},
        "confirmation_amount": {"currency": "usd", "amount": 0.0},
        "other_amount": {"currency": "usd", "amount": 44.20},
        "requested_comparison_amount": {"currency": "usd", "amount": 0.0},
        "rate_details": [
            {
                "rate_detail_type": "shipping",
                "carrier_description": "Shipping",
                "carrier_billing_code": "BaseServiceCharge",
                "carrier_memo": None,
                "amount": {"currency": "usd", "amount": 142.57},
                "billing_source": "Carrier",
            },
            {
                "rate_detail_type": "fuel_charge",
                "carrier_description": "Fuel Surcharge",
                "carrier_billing_code": "375",
                "carrier_memo": None,
                "amount": {"currency": "usd", "amount": 44.20},
                "billing_source": "Carrier",
            },
        ],
        "zone": None,
        "package_type": None,
        "carrier_weight": None,
        "delivery_days": 1,
        "guaranteed_service": True,
        "estimated_delivery_date": "2026-04-14T08:00:00Z",
        "carrier_delivery_days": "Tomorrow by 08:00 AM",
        "ship_date": "2026-04-13T00:00:00Z",
        "negotiated_rate": True,
        "service_type": "UPS Next Day Air® Early",
        "service_code": "ups_next_day_air_early_am",
        "trackable": True,
        "carrier_code": "ups",
        "carrier_nickname": "UPS",
        "carrier_friendly_name": "UPS",
        "display_scheme": None,
        "validation_status": "unknown",
        "warning_messages": [],
        "error_messages": [],
    },
    {
        "rate_type": "check",
        "carrier_id": "se-656171",
        "shipping_amount": {"currency": "usd", "amount": 44.21},
        "insurance_amount": {"currency": "usd", "amount": 0.0},
        "confirmation_amount": {"currency": "usd", "amount": 0.0},
        "other_amount": {"currency": "usd", "amount": 13.70},
        "requested_comparison_amount": {"currency": "usd", "amount": 0.0},
        "rate_details": [
            {
                "rate_detail_type": "shipping",
                "carrier_description": "Shipping",
                "carrier_billing_code": "BaseServiceCharge",
                "carrier_memo": None,
                "amount": {"currency": "usd", "amount": 44.21},
                "billing_source": "Carrier",
            },
            {
                "rate_detail_type": "fuel_charge",
                "carrier_description": "Fuel Surcharge",
                "carrier_billing_code": "375",
                "carrier_memo": None,
                "amount": {"currency": "usd", "amount": 13.70},
                "billing_source": "Carrier",
            },
        ],
        "zone": None,
        "package_type": None,
        "carrier_weight": None,
        "delivery_days": 1,
        "guaranteed_service": True,
        "estimated_delivery_date": "2026-04-14T23:00:00Z",
        "carrier_delivery_days": "Tomorrow by 11:00 PM",
        "ship_date": "2026-04-13T00:00:00Z",
        "negotiated_rate": True,
        "service_type": "UPS Next Day Air Saver®",
        "service_code": "ups_next_day_air_saver",
        "trackable": True,
        "carrier_code": "ups",
        "carrier_nickname": "UPS",
        "carrier_friendly_name": "UPS",
        "display_scheme": None,
        "validation_status": "unknown",
        "warning_messages": [],
        "error_messages": [],
    },
]
```

Exceptions
==========

- This method will only throw an exception that is an instance/extension of
  ([ShipEngineError](../shipengine/errors/__init__.py)) if there is a problem, such as a network
  error or an error response from the API.
