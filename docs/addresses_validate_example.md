Addresses Validate Documentation
================================
[ShipEngine](www.shipengine.com) allows you to validate an address before using it to create a shipment to ensure
accurate delivery of your packages.

Address validation can lead to reduced shipping costs by preventing address correction surcharges. ShipEngine
cross-references multiple databases to validate addresses and identify potential delivery issues and supports address
validation for virtually every country_code on Earth, including the United state_provinces, Canada, Great Britain,
Australia, Germany, France, Norway, Spain, Sweden, Israel, Italy, and over 160 others.

Please see [our docs](https://www.shipengine.com/docs/addresses/validation/) to learn more about validating addresses.

Input Parameters
----------------
The `validate_addresses` method accepts a list of addresses as seen below.
```python
address = [
    {
        "name": "ShipEngine",
        "company": "Auctane",
        "phone": "1-123-123-1234",
        "address_line1": "3800 N Lamar Blvd",
        "address_line2": "ste 220",
        "city_locality": "Austin",
        "state_province": "TX",
        "postal_code": "78756",
        "country_code": "US",
        "address_residential_indicator": "unknown",
    }
]
```

Output
------
The `validate_addresses` method returns a list of address validation result objects.

Example:
========
- Pass in a list of addresses you wish to validate into the `validate_addresses` method.
```python
import os

from shipengine import ShipEngine
from shipengine.errors import ShipEngineError


def validate_addresses_demo():
    api_key = os.getenv("SHIPENGINE_API_KEY")

    shipengine = ShipEngine(
        {"api_key": api_key, "page_size": 75, "retries": 3, "timeout": 10}
    )
    addresses = [
        {
            "name": "ShipEngine",
            "company": "Auctane",
            "phone": "1-123-123-1234",
            "address_line1": "3800 N Lamar Blvd",
            "address_line2": "ste 220",
            "city_locality": "Austin",
            "state_province": "TX",
            "postal_code": "78756",
            "country_code": "US",
            "address_residential_indicator": "unknown",
        },
        {
            "name": "ShipEngine",
            "company": "Auctane",
            "phone": "1-123-123-1234",
            "address_line1": "3800 N Lamar Blvd",
            "address_line2": "ste 220",
            "address_line3": "2nd Floor",
            "city_locality": "Austin",
            "state_province": "TX",
            "postal_code": "78756",
            "country_code": "US",
            "address_residential_indicator": "unknown",
        },
    ]

    try:
        result = shipengine.validate_addresses(address=addresses)
        print("::SUCCESS::")
        print(result)
    except ShipEngineError as err:
        print("::ERROR::")
        print(err.to_json())


validate_addresses_demo()
```

Example Output:
===============
- A list of carrier account that are connected to a given ShipEngine account.
```python
[
    {
        "matched_address": {
            "address_line1": "3800 N LAMAR BLVD STE 220",
            "address_line2": "",
            "address_line3": None,
            "address_residential_indicator": "no",
            "city_locality": "AUSTIN",
            "company_name": None,
            "country_code": "US",
            "name": "SHIPENGINE",
            "phone": "1-123-123-1234",
            "postal_code": "78756-0003",
            "state_province": "TX",
        },
        "messages": [],
        "original_address": {
            "address_line1": "3800 N Lamar Blvd",
            "address_line2": "ste 220",
            "address_line3": None,
            "address_residential_indicator": "unknown",
            "city_locality": "Austin",
            "company_name": None,
            "country_code": "US",
            "name": "ShipEngine",
            "phone": "1-123-123-1234",
            "postal_code": "78756",
            "state_province": "TX",
        },
        "status": "verified",
    },
    {
        "matched_address": {
            "address_line1": "3800 N LAMAR BLVD STE 220",
            "address_line2": "",
            "address_line3": "2ND FLOOR",
            "address_residential_indicator": "no",
            "city_locality": "AUSTIN",
            "company_name": None,
            "country_code": "US",
            "name": "SHIPENGINE",
            "phone": "1-123-123-1234",
            "postal_code": "78756-0003",
            "state_province": "TX",
        },
        "messages": [],
        "original_address": {
            "address_line1": "3800 N Lamar Blvd",
            "address_line2": "ste 220",
            "address_line3": "2nd Floor",
            "address_residential_indicator": "unknown",
            "city_locality": "Austin",
            "company_name": None,
            "country_code": "US",
            "name": "ShipEngine",
            "phone": "1-123-123-1234",
            "postal_code": "78756",
            "state_province": "TX",
        },
        "status": "verified",
    },
]
```

Exceptions
==========

- This method will only throw an exception that is an instance/extension of
  ([ShipEngineError](../shipengine/errors/__init__.py)) if there is a problem if a problem occurs, such as a network
  error or an error response from the API.
