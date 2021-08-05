List Carriers Documentation
===========================
[ShipEngine](www.shipengine.com) allows you to connect
your own carrier accounts through the ShipEngine [dashboard](https://www.shipengine.com/docs/carriers/setup/). You can list all the carrier accounts you have connected with the `list_carriers` method.

To learn more about carrier accounts please see [our docs](https://www.shipengine.com/docs/reference/list-carriers/).

Output
------
The `list_carriers` method returns a list of carrier accounts connected to a given ShipEngine account.

Example
=======
```python
import os

from shipengine import ShipEngine
from shipengine.errors import ShipEngineError


def list_carriers_demo():
    api_key = os.getenv("SHIPENGINE_API_KEY")

    shipengine = ShipEngine(
        {"api_key": api_key, "page_size": 75, "retries": 3, "timeout": 10}
    )

    try:
        result = shipengine.list_carriers()
        print("::SUCCESS::")
        print(result)
    except ShipEngineError as err:
        print("::ERROR::")
        print(err.to_json())


list_carriers_demo()
```

Example Output
==============
A list of carrier accounts connected to a given ShipEngine account.
```python
{
    "carriers": [
        {
            "carrier_id": "se-656171",
            "carrier_code": "stamps_com",
            "account_number": "test_account_656171",
            "requires_funded_amount": True,
            "balance": 8742.9100,
            "nickname": "ShipEngine Test Account - Stamps.com",
            "friendly_name": "Stamps.com",
            "primary": False,
            "has_multi_package_supporting_services": False,
            "supports_label_messages": True,
            "services": [
                {
                    "carrier_id": "se-656171",
                    "carrier_code": "stamps_com",
                    "service_code": "usps_first_class_mail",
                    "name": "USPS First Class Mail",
                    "domestic": True,
                    "international": False,
                    "is_multi_package_supported": False,
                },
                {
                    "carrier_id": "se-656171",
                    "carrier_code": "stamps_com",
                    "service_code": "usps_media_mail",
                    "name": "USPS Media Mail",
                    "domestic": True,
                    "international": False,
                    "is_multi_package_supported": False,
                },
                {
                    "carrier_id": "se-656171",
                    "carrier_code": "stamps_com",
                    "service_code": "usps_parcel_select",
                    "name": "USPS Parcel Select Ground",
                    "domestic": True,
                    "international": False,
                    "is_multi_package_supported": False,
                },
                {
                    "carrier_id": "se-656171",
                    "carrier_code": "stamps_com",
                    "service_code": "usps_priority_mail",
                    "name": "USPS Priority Mail",
                    "domestic": True,
                    "international": False,
                    "is_multi_package_supported": False,
                },
                {
                    "carrier_id": "se-656171",
                    "carrier_code": "stamps_com",
                    "service_code": "usps_priority_mail_express",
                    "name": "USPS Priority Mail Express",
                    "domestic": True,
                    "international": False,
                    "is_multi_package_supported": False,
                },
                {
                    "carrier_id": "se-656171",
                    "carrier_code": "stamps_com",
                    "service_code": "usps_first_class_mail_international",
                    "name": "USPS First Class Mail Intl",
                    "domestic": False,
                    "international": True,
                    "is_multi_package_supported": False,
                },
                {
                    "carrier_id": "se-656171",
                    "carrier_code": "stamps_com",
                    "service_code": "usps_priority_mail_international",
                    "name": "USPS Priority Mail Intl",
                    "domestic": False,
                    "international": True,
                    "is_multi_package_supported": False,
                },
                {
                    "carrier_id": "se-656171",
                    "carrier_code": "stamps_com",
                    "service_code": "usps_priority_mail_express_international",
                    "name": "USPS Priority Mail Express Intl",
                    "domestic": False,
                    "international": True,
                    "is_multi_package_supported": False,
                },
            ],
            "packages": [
                {"package_code": "cubic", "name": "Cubic", "description": "Cubic"},
                {
                    "package_code": "flat_rate_envelope",
                    "name": "Flat Rate Envelope",
                    "description": 'USPS flat rate envelope. A special cardboard envelope provided by the USPS that clearly indicates "Flat Rate".',
                },
                {
                    "package_code": "flat_rate_legal_envelope",
                    "name": "Flat Rate Legal Envelope",
                    "description": "Flat Rate Legal Envelope",
                },
                {
                    "package_code": "flat_rate_padded_envelope",
                    "name": "Flat Rate Padded Envelope",
                    "description": "Flat Rate Padded Envelope",
                },
                {
                    "package_code": "large_envelope_or_flat",
                    "name": "Large Envelope or Flat",
                    "description": 'Large envelope or flat. Has one dimension that is between 11 1/2" and 15" long, 6 1/18" and 12" high, or 1/4" and 3/4" thick.',
                },
                {
                    "package_code": "large_flat_rate_box",
                    "name": "Large Flat Rate Box",
                    "description": "Large Flat Rate Box",
                },
                {
                    "package_code": "large_package",
                    "name": 'Large Package (any side \u003e 12")',
                    "description": 'Large package. Longest side plus the distance around the thickest part is over 84" and less than or equal to 108".',
                },
                {"package_code": "letter", "name": "Letter", "description": "Letter"},
                {
                    "package_code": "medium_flat_rate_box",
                    "name": "Medium Flat Rate Box",
                    "description": 'USPS flat rate box. A special 11" x 8 1/2" x 5 1/2" or 14" x 3.5" x 12" USPS box that clearly indicates "Flat Rate Box"',
                },
                {
                    "package_code": "non_rectangular",
                    "name": "Non Rectangular Package",
                    "description": "Non-Rectangular package type that is cylindrical in shape.",
                },
                {
                    "package_code": "package",
                    "name": "Package",
                    "description": 'Package. Longest side plus the distance around the thickest part is less than or equal to 84"',
                },
                {
                    "package_code": "regional_rate_box_a",
                    "name": "Regional Rate Box A",
                    "description": "Regional Rate Box A",
                },
                {
                    "package_code": "regional_rate_box_b",
                    "name": "Regional Rate Box B",
                    "description": "Regional Rate Box B",
                },
                {
                    "package_code": "small_flat_rate_box",
                    "name": "Small Flat Rate Box",
                    "description": "Small Flat Rate Box",
                },
                {
                    "package_code": "thick_envelope",
                    "name": "Thick Envelope",
                    "description": 'Thick envelope. Envelopes or flats greater than 3/4" at the thickest point.',
                },
            ],
            "options": [
                {"name": "non_machinable", "default_value": "False", "description": ""},
                {"name": "bill_to_account", "description": "Bill To Account"},
                {"name": "bill_to_party", "description": "Bill To Party"},
                {"name": "bill_to_postal_code", "description": "Bill To Postal Code"},
                {"name": "bill_to_country_code", "description": "Bill To Country Code"},
            ],
        },
        {
            "carrier_id": "se-656172",
            "carrier_code": "ups",
            "account_number": "test_account_656172",
            "requires_funded_amount": False,
            "balance": 0.0,
            "nickname": "ShipEngine Test Account - UPS",
            "friendly_name": "UPS",
            "primary": False,
            "has_multi_package_supporting_services": True,
            "supports_label_messages": True,
            "services": [
                {
                    "carrier_id": "se-656172",
                    "carrier_code": "ups",
                    "service_code": "ups_standard_international",
                    "name": "UPS Standard®",
                    "domestic": False,
                    "international": True,
                    "is_multi_package_supported": True,
                },
                {
                    "carrier_id": "se-656172",
                    "carrier_code": "ups",
                    "service_code": "ups_next_day_air_early_am",
                    "name": "UPS Next Day Air® Early",
                    "domestic": True,
                    "international": False,
                    "is_multi_package_supported": True,
                },
                {
                    "carrier_id": "se-656172",
                    "carrier_code": "ups",
                    "service_code": "ups_worldwide_express",
                    "name": "UPS Worldwide Express®",
                    "domestic": False,
                    "international": True,
                    "is_multi_package_supported": True,
                },
                {
                    "carrier_id": "se-656172",
                    "carrier_code": "ups",
                    "service_code": "ups_next_day_air",
                    "name": "UPS Next Day Air®",
                    "domestic": True,
                    "international": False,
                    "is_multi_package_supported": True,
                },
                {
                    "carrier_id": "se-656172",
                    "carrier_code": "ups",
                    "service_code": "ups_ground_international",
                    "name": "UPS Ground® (International)",
                    "domestic": False,
                    "international": True,
                    "is_multi_package_supported": True,
                },
                {
                    "carrier_id": "se-656172",
                    "carrier_code": "ups",
                    "service_code": "ups_worldwide_express_plus",
                    "name": "UPS Worldwide Express Plus®",
                    "domestic": False,
                    "international": True,
                    "is_multi_package_supported": True,
                },
                {
                    "carrier_id": "se-656172",
                    "carrier_code": "ups",
                    "service_code": "ups_next_day_air_saver",
                    "name": "UPS Next Day Air Saver®",
                    "domestic": True,
                    "international": False,
                    "is_multi_package_supported": True,
                },
                {
                    "carrier_id": "se-656172",
                    "carrier_code": "ups",
                    "service_code": "ups_worldwide_expedited",
                    "name": "UPS Worldwide Expedited®",
                    "domestic": False,
                    "international": True,
                    "is_multi_package_supported": True,
                },
                {
                    "carrier_id": "se-656172",
                    "carrier_code": "ups",
                    "service_code": "ups_2nd_day_air_am",
                    "name": "UPS 2nd Day Air AM®",
                    "domestic": True,
                    "international": False,
                    "is_multi_package_supported": True,
                },
                {
                    "carrier_id": "se-656172",
                    "carrier_code": "ups",
                    "service_code": "ups_2nd_day_air",
                    "name": "UPS 2nd Day Air®",
                    "domestic": True,
                    "international": False,
                    "is_multi_package_supported": True,
                },
                {
                    "carrier_id": "se-656172",
                    "carrier_code": "ups",
                    "service_code": "ups_worldwide_saver",
                    "name": "UPS Worldwide Saver®",
                    "domestic": False,
                    "international": True,
                    "is_multi_package_supported": True,
                },
                {
                    "carrier_id": "se-656172",
                    "carrier_code": "ups",
                    "service_code": "ups_2nd_day_air_international",
                    "name": "UPS 2nd Day Air® (International)",
                    "domestic": False,
                    "international": True,
                    "is_multi_package_supported": True,
                },
                {
                    "carrier_id": "se-656172",
                    "carrier_code": "ups",
                    "service_code": "ups_3_day_select",
                    "name": "UPS 3 Day Select®",
                    "domestic": True,
                    "international": False,
                    "is_multi_package_supported": True,
                },
                {
                    "carrier_id": "se-656172",
                    "carrier_code": "ups",
                    "service_code": "ups_ground",
                    "name": "UPS® Ground",
                    "domestic": True,
                    "international": False,
                    "is_multi_package_supported": True,
                },
                {
                    "carrier_id": "se-656172",
                    "carrier_code": "ups",
                    "service_code": "ups_next_day_air_international",
                    "name": "UPS Next Day Air® (International)",
                    "domestic": False,
                    "international": True,
                    "is_multi_package_supported": True,
                },
            ],
            "packages": [
                {
                    "package_code": "package",
                    "name": "Package",
                    "description": 'Package. Longest side plus the distance around the thickest part is less than or equal to 84"',
                },
                {
                    "package_code": "ups__express_box_large",
                    "name": "UPS  Express® Box - Large",
                    "description": "Express Box - Large",
                },
                {
                    "package_code": "ups_10_kg_box",
                    "name": "UPS 10 KG Box®",
                    "description": "10 KG Box",
                },
                {
                    "package_code": "ups_25_kg_box",
                    "name": "UPS 25 KG Box®",
                    "description": "25 KG Box",
                },
                {
                    "package_code": "ups_express_box",
                    "name": "UPS Express® Box",
                    "description": "Express Box",
                },
                {
                    "package_code": "ups_express_box_medium",
                    "name": "UPS Express® Box - Medium",
                    "description": "Express Box - Medium",
                },
                {
                    "package_code": "ups_express_box_small",
                    "name": "UPS Express® Box - Small",
                    "description": "Express Box - Small",
                },
                {
                    "package_code": "ups_express_pak",
                    "name": "UPS Express® Pak",
                    "description": "Pak",
                },
                {
                    "package_code": "ups_letter",
                    "name": "UPS Letter",
                    "description": "Letter",
                },
                {"package_code": "ups_tube", "name": "UPS Tube", "description": "Tube"},
            ],
            "options": [
                {"name": "bill_to_account", "default_value": "", "description": ""},
                {
                    "name": "bill_to_country_code",
                    "default_value": "",
                    "description": "",
                },
                {"name": "bill_to_party", "default_value": "", "description": ""},
                {"name": "bill_to_postal_code", "default_value": "", "description": ""},
                {"name": "collect_on_delivery", "default_value": "", "description": ""},
                {
                    "name": "contains_alcohol",
                    "default_value": "False",
                    "description": "",
                },
                {
                    "name": "delivered_duty_paid",
                    "default_value": "False",
                    "description": "",
                },
                {"name": "dry_ice", "default_value": "False", "description": ""},
                {"name": "dry_ice_weight", "default_value": "0", "description": ""},
                {"name": "freight_class", "default_value": "", "description": ""},
                {"name": "non_machinable", "default_value": "False", "description": ""},
                {
                    "name": "saturday_delivery",
                    "default_value": "False",
                    "description": "",
                },
                {
                    "name": "shipper_release",
                    "default_value": "False",
                    "description": "Driver may release package without signature",
                },
            ],
        },
        {
            "carrier_id": "se-656173",
            "carrier_code": "fedex",
            "account_number": "test_account_656173",
            "requires_funded_amount": False,
            "balance": 0.0,
            "nickname": "ShipEngine Test Account - FedEx",
            "friendly_name": "FedEx",
            "primary": False,
            "has_multi_package_supporting_services": True,
            "supports_label_messages": True,
            "services": [
                {
                    "carrier_id": "se-656173",
                    "carrier_code": "fedex",
                    "service_code": "fedex_ground",
                    "name": "FedEx Ground®",
                    "domestic": True,
                    "international": False,
                    "is_multi_package_supported": True,
                },
                {
                    "carrier_id": "se-656173",
                    "carrier_code": "fedex",
                    "service_code": "fedex_home_delivery",
                    "name": "FedEx Home Delivery®",
                    "domestic": True,
                    "international": False,
                    "is_multi_package_supported": True,
                },
                {
                    "carrier_id": "se-656173",
                    "carrier_code": "fedex",
                    "service_code": "fedex_2day",
                    "name": "FedEx 2Day®",
                    "domestic": True,
                    "international": False,
                    "is_multi_package_supported": True,
                },
                {
                    "carrier_id": "se-656173",
                    "carrier_code": "fedex",
                    "service_code": "fedex_2day_am",
                    "name": "FedEx 2Day® A.M.",
                    "domestic": True,
                    "international": False,
                    "is_multi_package_supported": True,
                },
                {
                    "carrier_id": "se-656173",
                    "carrier_code": "fedex",
                    "service_code": "fedex_express_saver",
                    "name": "FedEx Express Saver®",
                    "domestic": True,
                    "international": False,
                    "is_multi_package_supported": True,
                },
                {
                    "carrier_id": "se-656173",
                    "carrier_code": "fedex",
                    "service_code": "fedex_standard_overnight",
                    "name": "FedEx Standard Overnight®",
                    "domestic": True,
                    "international": False,
                    "is_multi_package_supported": True,
                },
                {
                    "carrier_id": "se-656173",
                    "carrier_code": "fedex",
                    "service_code": "fedex_priority_overnight",
                    "name": "FedEx Priority Overnight®",
                    "domestic": True,
                    "international": False,
                    "is_multi_package_supported": True,
                },
                {
                    "carrier_id": "se-656173",
                    "carrier_code": "fedex",
                    "service_code": "fedex_first_overnight",
                    "name": "FedEx First Overnight®",
                    "domestic": True,
                    "international": False,
                    "is_multi_package_supported": True,
                },
                {
                    "carrier_id": "se-656173",
                    "carrier_code": "fedex",
                    "service_code": "fedex_1_day_freight",
                    "name": "FedEx 1Day® Freight",
                    "domestic": True,
                    "international": False,
                    "is_multi_package_supported": True,
                },
                {
                    "carrier_id": "se-656173",
                    "carrier_code": "fedex",
                    "service_code": "fedex_2_day_freight",
                    "name": "FedEx 2Day® Freight",
                    "domestic": True,
                    "international": False,
                    "is_multi_package_supported": True,
                },
                {
                    "carrier_id": "se-656173",
                    "carrier_code": "fedex",
                    "service_code": "fedex_3_day_freight",
                    "name": "FedEx 3Day® Freight",
                    "domestic": True,
                    "international": False,
                    "is_multi_package_supported": True,
                },
                {
                    "carrier_id": "se-656173",
                    "carrier_code": "fedex",
                    "service_code": "fedex_first_overnight_freight",
                    "name": "FedEx First Overnight® Freight",
                    "domestic": True,
                    "international": False,
                    "is_multi_package_supported": True,
                },
                {
                    "carrier_id": "se-656173",
                    "carrier_code": "fedex",
                    "service_code": "fedex_ground_international",
                    "name": "FedEx International Ground®",
                    "domestic": False,
                    "international": True,
                    "is_multi_package_supported": True,
                },
                {
                    "carrier_id": "se-656173",
                    "carrier_code": "fedex",
                    "service_code": "fedex_international_economy",
                    "name": "FedEx International Economy®",
                    "domestic": False,
                    "international": True,
                    "is_multi_package_supported": True,
                },
                {
                    "carrier_id": "se-656173",
                    "carrier_code": "fedex",
                    "service_code": "fedex_international_priority",
                    "name": "FedEx International Priority®",
                    "domestic": False,
                    "international": True,
                    "is_multi_package_supported": True,
                },
                {
                    "carrier_id": "se-656173",
                    "carrier_code": "fedex",
                    "service_code": "fedex_international_first",
                    "name": "FedEx International First®",
                    "domestic": False,
                    "international": True,
                    "is_multi_package_supported": True,
                },
                {
                    "carrier_id": "se-656173",
                    "carrier_code": "fedex",
                    "service_code": "fedex_international_economy_freight",
                    "name": "FedEx International Economy® Freight",
                    "domestic": False,
                    "international": True,
                    "is_multi_package_supported": True,
                },
                {
                    "carrier_id": "se-656173",
                    "carrier_code": "fedex",
                    "service_code": "fedex_international_priority_freight",
                    "name": "FedEx International Priority® Freight",
                    "domestic": False,
                    "international": True,
                    "is_multi_package_supported": True,
                },
                {
                    "carrier_id": "se-656173",
                    "carrier_code": "fedex",
                    "service_code": "fedex_international_connect_plus",
                    "name": "FedEx International Connect Plus®",
                    "domestic": False,
                    "international": True,
                    "is_multi_package_supported": False,
                },
            ],
            "packages": [
                {
                    "package_code": "fedex_envelope_onerate",
                    "name": "FedEx One Rate® Envelope",
                    "description": "FedEx® Envelope",
                },
                {
                    "package_code": "fedex_extra_large_box_onerate",
                    "name": "FedEx One Rate® Extra Large Box",
                    "description": "FedEx® Extra Large Box",
                },
                {
                    "package_code": "fedex_large_box_onerate",
                    "name": "FedEx One Rate® Large Box",
                    "description": "FedEx® Large Box",
                },
                {
                    "package_code": "fedex_medium_box_onerate",
                    "name": "FedEx One Rate® Medium Box",
                    "description": "FedEx® Medium Box",
                },
                {
                    "package_code": "fedex_pak_onerate",
                    "name": "FedEx One Rate® Pak",
                    "description": "FedEx® Pak",
                },
                {
                    "package_code": "fedex_small_box_onerate",
                    "name": "FedEx One Rate® Small Box",
                    "description": "FedEx® Small Box",
                },
                {
                    "package_code": "fedex_tube_onerate",
                    "name": "FedEx One Rate® Tube",
                    "description": "FedEx® Tube",
                },
                {
                    "package_code": "fedex_10kg_box",
                    "name": "FedEx® 10kg Box",
                    "description": "FedEx® 10kg Box",
                },
                {
                    "package_code": "fedex_25kg_box",
                    "name": "FedEx® 25kg Box",
                    "description": "FedEx® 25kg Box",
                },
                {
                    "package_code": "fedex_box",
                    "name": "FedEx® Box",
                    "description": "FedEx® Box",
                },
                {
                    "package_code": "fedex_envelope",
                    "name": "FedEx® Envelope",
                    "description": "FedEx® Envelope",
                },
                {
                    "package_code": "fedex_pak",
                    "name": "FedEx® Pak",
                    "description": "FedEx® Pak",
                },
                {
                    "package_code": "fedex_tube",
                    "name": "FedEx® Tube",
                    "description": "FedEx® Tube",
                },
                {
                    "package_code": "package",
                    "name": "Package",
                    "description": 'Package. Longest side plus the distance around the thickest part is less than or equal to 84"',
                },
            ],
            "options": [
                {"name": "bill_to_account", "default_value": "", "description": ""},
                {
                    "name": "bill_to_country_code",
                    "default_value": "",
                    "description": "",
                },
                {"name": "bill_to_party", "default_value": "", "description": ""},
                {"name": "bill_to_postal_code", "default_value": "", "description": ""},
                {"name": "collect_on_delivery", "default_value": "", "description": ""},
                {
                    "name": "contains_alcohol",
                    "default_value": "False",
                    "description": "",
                },
                {
                    "name": "delivered_duty_paid",
                    "default_value": "False",
                    "description": "",
                },
                {"name": "dry_ice", "default_value": "False", "description": ""},
                {"name": "dry_ice_weight", "default_value": "0", "description": ""},
                {"name": "non_machinable", "default_value": "False", "description": ""},
                {
                    "name": "saturday_delivery",
                    "default_value": "False",
                    "description": "",
                },
            ],
        },
    ],
    "request_id": "1ce3a55d-9ba0-457d-ba6d-6ab60ddc9468",
    "errors": [],
}
```

Exceptions
==========

- This method will only throw an exception that is an instance/extension of
  ([ShipEngineError](../shipengine/errors/__init__.py)) if there is a problem if a problem occurs, such as a network
  error or an error response from the API.
