Normalize Address Documentation
===============================
ShipEngine allows you to validate an address before using it to create a shipment to ensure accurate delivery
of your packages.

Address validation can lead to reduced shipping costs by preventing address correction surcharges. ShipEngine
cross-references multiple databases to validate addresses and identify potential delivery issues and supports address
validation for virtually every countryCode on Earth, including the United States, Canada, Great Britain, Australia,
Germany, France, Norway, Spain, Sweden, Israel, Italy, and over 160 others.

There are two ways to validate an address using this SDK.

- Single Address Validation - [validate_address(address: Address, config: Dict[str, Any])](./address_validation_example.md)
- Normalize an Address - `normalize_address(address: Address, config: Dict[str, Any])`

---
## **Table of Contents**
- [Address Object](#address-object)
  * [Input Parameters](#input-parameters)
  * [Output](#output)
- [Examples:](#examples-)
  * [Successful Address Validation Output (object repr)](#--successful-address-validation-output--object-repr----)
  * [Successful Address Validation Output (JSON object)](#--successful-address-validation-output--json-object----)
  * [Successful Address Validation Output (dictionary)](#--successful-address-validation-output--dictionary----)
- [Exceptions](#exceptions)

`normalize_address(address: Address, config: Dict[str, Any])` - Normalize a given address.
==========================================================================

- The `normalize_address` method accepts the same address object as the `validate_address` method as well as an `array`
containing method-level configuration options.

- **Behavior**: The `normalize_address` method will either return a normalized version of the address you pass in. This
  will throw an exception if address validation fails, or an invalid address is provided. The normalized address will
  be returned as an instance of the [Address](../shipengine/models/address/__init__.py) class.

- **Method level configuration** - You can optionally pass in an list that contains `configuration` values to be used
  for the current method call. The options are `api_key`, `base_uri`, `page_size`,
  `retries`, and `timeout`.

Address Object
==============

- **street** *array* `required`
- **city** *string*
- **state** *string*
- **postal_code** *string*
- **countryCode** *string* `required`
- **is_residential** *boolean*
- **name** *string*
- **phone** *string*
- **company** *string*


Input Parameters
----------------

The `normalize_address` method accepts an address object containing the properties listed below. You can import
the [`Address`]() type into your project to take advantage of your IDE's code completion functionality.


* `country` *required* <br>
  A *string* containing a valid [two digit country code](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes).

* `street` *required* <br>
  The street address provided as a single string or as multiple strings in an array. It should be one of the following:<br>

    * A *string* containing `0` to `1000` characters (i.e. `"4009 Marathon Blvd, Ste 200"`). <br>
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
If the address can be normalized, the `normalize_address` method returns a normalized version of the address. You can
import the [Address]() type into your project to take advantage of your IDE's code completion functionality.

* `street` <br>
  An *array* containing the street address. Each string in the array is a separate line, up to 3.<br>

* `country` <br>
  A *string* containing the [ISO 3166](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes) country code.

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


Examples:
=========

**Successful Address Normalization** - This example illustrates the following:
- Instantiate the ShipEngine class.
- Create an Address object.
- Use the `normalize_address` method to normalize a given `Address` by passing in the `Address` object you created in
  the previous step.
- Print out the result to view the normalized address object.

```python
import os

from shipengine import ShipEngine
from shipengine.models import Address

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

normalize_address = shipengine.validate_address(address=address)
print(normalize_address)
```
**Successful Address Validation Output (object repr):**
-------------------------------------------------------
As a raw `AddressValidateResult` object `repr`
```
Address(street=['4 JERSEY ST APT 2B'], city_locality='BOSTON', state_province='MA', postal_code='02215', country_code='US', is_residential=True, name='SHIPENGINE', phone='123456789', company='AUCTANE')
```

**Successful Address Validation Output (JSON object):**
-------------------------------------------------------
Continuing with the example above, you can also serialize the `Address` Type to a JSON string by using
the `.to_json()` on any of the models in our SDK. The following output comes from using the `print()` function
on the `normalized_address` variable as `normalized_address.to_json()`.
```json5
{
    "street": [
        "4 JERSEY ST APT 2B"
    ],
    "cityLocality": "BOSTON",
    "stateProvince": "MA",
    "postalCode": "02215",
    "countryCode": "US",
    "isResidential": true,
    "name": "SHIPENGINE",
    "phone": "123456789",
    "company": "AUCTANE"
}
```

**Successful Address Validation Output (dictionary):**
------------------------------------------------------
The `AddressValidateResult` can be converted to a dictionary by using
the `.to_dict()` method on any of the models in our SDK. The following output comes from using `pprint.pprint()` for
readability/formatting on the `validated_address` variable as `validated_address.to_dict()`.
```python
{
    "cityLocality": "BOSTON",
    "company": "AUCTANE",
    "countryCode": "US",
    "isResidential": True,
    "name": "SHIPENGINE",
    "phone": "123456789",
    "postalCode": "02215",
    "stateProvince": "MA",
    "street": ["4 JERSEY ST APT 2B"],
}
```

Exceptions
==========

- This method will throw an exception that is an instance/extension of
  ([ShipEngineException]()) if there is a problem with the `Address` provided, or
  if address validation fails.
