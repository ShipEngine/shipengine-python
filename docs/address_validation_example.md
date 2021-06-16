Address Validation Documentation
================================
[ShipEngine](www.shipengine.com) allows you to validate an address before using it to create a shipment to ensure accurate delivery
of your packages.

Address validation can lead to reduced shipping costs by preventing address correction surcharges. ShipEngine
cross-references multiple databases to validate addresses and identify potential delivery issues and supports address
validation for virtually every country_code on Earth, including the United state_provinces, Canada, Great Britain,
Australia, Germany, France, Norway, Spain, Sweden, Israel, Italy, and over 160 others.

There are two ways to validate an address using this SDK.

- Single Address Validation - `validate_address(address: Address, config: Dict[str, Any])`
- Normalize an Address - [normalizeAddress(address: Address, config: Dict[str, Any])](./normalize_address_example.md)

---
## **Table of Contents**
- [Address Object](#address-object)
  * [Input Parameters](#input-parameters)
  * [Output](#output)
- [Examples:](#examples-)
  * [Successful Address Validation Output (object repr)](#--successful-address-validation-output--object-repr----)
  * [Successful Address Validation Output (JSON object)](#--successful-address-validation-output--json-object----)
  * [Successful Address Validation Output (dictionary)](#--successful-address-validation-output--dictionary----)
  * [Successful Address Validation with Warnings (JSON Object)](#--successful-address-validation-with-warnings--json-object----)
  * [Unsuccessful Address Validation with Errors (JSON object)](#--unsuccessful-address-validation-with-errors--json-object----)
- [Exceptions](#exceptions)


`validate_address(address: Address, config: Dict[str, Any])` - Validate a single address.
=========================================================================

- The `validate_address` method takes in an list containing address information, which would typically be a set of
  **Address Line 1, Address Line 2, and Address Line 3** within a `street` list. This object should also have a
  `city_localityLocality`, `state_provinceProvince`, `postal_code`, `country_code`, `name`, `phone`, and `company`. This method
  requires a `country_code` which should be the 2 character capitalized abbreviation for a given country_code.

- **Behavior**: The `validate_address` method allows you to determine whether an address is valid before using it for
  your shipments. It accepts an address object containing typical address properties, described below, and will return
  a normalized address object if the address is valid.

- **Method level configuration** - You can optionally pass in an list that contains `configuration` values to be used
  for the current method call. The options are `api_key`, `base_uri`, `page_size`,
  `retries`, and `timeout`.


Address Object
==============

- **street** *list* `required`
- **city_locality** *string*
- **state_province** *string*
- **postal_code** *string*
- **country_code** *string* `required`
- **is_residential** *boolean*
- **name** *string*
- **phone** *string*
- **company** *string*

Input Parameters
----------------

The `validate_address` method accepts an address object containing the properties listed below.
You can import the [`Address`](../shipengine_sdk/models/address/__init__.py)
type into your project to take advantage of your
IDE's code completion functionality.

* `country_code` *required* <br>
A *string* containing a valid [two digit country code](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes).


* `street` *required* <br>
The street address provided as a single string or as multiple strings in an array. It should be one of the following:<br>
  *  A *string* containing `0` to `1000` characters (i.e. `"4009 Marathon Blvd, Ste 200"`). <br>
  * An *array* containing `1` to `3` elements. Each element
should contain a *string* value containing `0` to `1000` characters. <br>
  (i.e. `["4009 Marathon Blvd", "Ste 200"]`).

**Either the `postal_code` OR the `city_locality` AND `state_province` must be provided.**

* `postal_code`  <br>
A *string* between`0` to `1000` characters containing the postal code. <br>


* `city_locality`  <br>
A *string* between `0` to `1000` characters containing the city or locality.<br>


* `state_province`  <br>
A *string* between `0` to `1000` characters containing the state or province.<br>


* `is_residential` <br>
A *boolean* value indicating whether this is a residential or commercial address. Leave `None` if unknown. <br>


* `name` <br>
A *string* between `0` and `1000` characters indicating the name of the sender or recipient at the address, if applicable.


* `phone` <br>
A *string* between `0` and `1000` characters indicating the phone number associated with this address, if any.


* `company` <br>
A *string* between `0` and `1000` characters indicating the company name, if this is a business address.

Output
------
The `validate_address` method returns an address validation result object containing the properties listed below.
You can import the [`AddressValidationResult`](../shipengine_sdk/models/address/__init__.py)
type into your project to take advantage of your IDE's code completion functionality.

* `is_valid` <br>
  A *boolean* indicating whether the address provided is valid.


* `normalized_address` <br>
An object containing the normalized form of the address, according to the normalization rules of the country in which the address resides.
This property will only be provided if the address is valid.

   <br>

  * `street` <br>
     An *array* containing the street address. Each string in the array is a separate line, up to 3. <br>

  * `country_code` <br>
  A *string* containing the [ISO 3166 country code]((https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes)).

  * `postal_code`  <br>
  A *string* containing the postal code.

  * `city_locality`  <br>
  A *string* containing the city or locality.

  * `state_province`  <br>
  A *string* containing the state or province.

  * `is_residential` <br>
  A *boolean* indicating whether the address is residential or commercial.
  If unknown, this field will be `None`.

  * `name` <br>
  A *string* containing the name of the sender or recipient at the address, if applicable.
  This field may be empty.

  * `phone` <br>
  A *string* containing the phone number associated with this address, if any.
  This field may be empty.

  * `company` <br>
  A *string* containing the company name, if this is a known business address.
  This field may be empty.

<br>

* `info` <br>
An *array* of informational messages about the address validation, such as minor corrections.

* `warnings` <br>
An *array* of warning messages about the address validation, such as major changes that
were made to the normalized address.

* `error` <br>
An *array* of Error messages about the address validation, such as invalid fields that
prevent the address from being fully validated.



Examples:
=========

**Successful Address Validation:** - This example illustrates the following:
  - Instantiate the ShipEngine class.
  - Create an Address object.
  - Use the `validate_address` method to validate the address by passing in the Address object you created in the previous step.
  - Print out the result to view validated address/address validation response from ShipEngine API.

```python
import os

from shipengine_sdk import ShipEngine
from shipengine_sdk.models import Address

api_key = os.getenv("SHIPENGINE_API_KEY")

shipengine = ShipEngine(
    {"api_key": api_key, "page_size": 75, "retries": 3, "timeout": 10}
)
address = Address(
    name="ShipEngine",
    company="Auctane",
    phone="123456789",
    street=["4 Jersey St", "Apt. 2b"],
    city_locality="Boston",
    state_province="MA",
    postal_code="02215",
    country_code="US",
)

validated_address = shipengine.validate_address(address=address)
print(validated_address)
```

**Successful Address Validation Output (object repr):**
-------------------------------------------------------
As a raw `AddressValidateResult` object `repr`.

```
Address(street=['4 JERSEY ST APT 2B'], city_locality='BOSTON', state_province='MA', postal_code='02215', country_code='US', is_residential=True, name='SHIPENGINE', phone='123456789', company='AUCTANE')
```

**Successful Address Validation Output (JSON object):**
-------------------------------------------------------
Continuing with the example above, you can also serialize the `Address` Type to a JSON string by using
the `.to_json()` on any of the models in our SDK. The following output comes from using the `print()` function
on the `validated_address` variable as `validated_address.to_json()`.

```json5
{
  "is_valid": true,
  "request_id": "req_ca5951303bb74885b53ac29673bead02",
  "normalized_address": {
    "street": [
      "4 JERSEY ST APT 2B"
    ],
    "city_locality": "BOSTON",
    "state_province": "MA",
    "postal_code": "02215",
    "country_code": "US",
    "is_residential": true,
    "name": "SHIPENGINE",
    "phone": "123456789",
    "company": "AUCTANE"
  },
  "info": [],
  "warnings": [],
  "errors": []
}
```

**Successful Address Validation Output (dictionary):**
------------------------------------------------------
The `AddressValidateResult` can be converted to a dictionary by using
the `.to_dict()` method on any of the models in our SDK. The following output comes from using `pprint.pprint()` for
readability/formatting on the `validated_address` variable as `validated_address.to_dict()`.
```python
{
    "errors": [],
    "info": [],
    "is_valid": True,
    "normalized_address": Address(
        street=["4 JERSEY ST APT 2B"],
        city_locality="BOSTON",
        state_province="MA",
        postal_code="02215",
        country_code="US",
        is_residential=True,
        name="SHIPENGINE",
        phone="123456789",
        company="AUCTANE",
    ),
    "request_id": "req_ca5951303bb74885b53ac29673bead02",
    "warnings": [],
}
```

**Successful Address Validation with Warnings (JSON Object):**
--------------------------------------------------------------
```json5
{
  "is_valid": true,
  "request_id": "req_ca5951303bb74885b53ac29673bead02",
  "normalized_address": {
    "street": [
      "4 JERSEY ST APT 2B"
    ],
    "city_locality": "BOSTON",
    "state_province": "MA",
    "postal_code": "02215",
    "country_code": "US",
    "is_residential": true,
    "name": "SHIPENGINE",
    "phone": "123456789",
    "company": "AUCTANE"
  },
  "info": [],
  "warnings": [
     "This address has been verified down to the house/building level (highest possible accuracy with the provided data)"
  ],
  "errors": []
}
```

**Unsuccessful Address Validation with Errors (JSON object):**
--------------------------------------------------------------
```json5
{
  "isValid": false,
  "info": [],
  "warnings": [],
  "errors": [
    "Invalid City, State, or Zip"
  ]
}
```

Exceptions
==========

- This method will only throw an exception that is an instance/extension of
  ([ShipEngineError](../shipengine_sdk/errors/__init__.py)) if there is a problem if a problem occurs, such as a
  network error or an error response from the API.
