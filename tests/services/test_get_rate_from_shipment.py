"""Testing the get_rate_fro_shipment functionality in the ShipEngine SDK."""
import json
import unittest
import urllib.parse as urlparse

import responses

from shipengine.enums import BaseURL, Endpoints
from tests.util import stub_shipengine_instance


class TestGetRateFromShipment(unittest.TestCase):
    @responses.activate
    def test_get_rate_from_shipment(self) -> None:
        """Test get_rate_from_shipment functionality."""
        responses.add(
            **{
                "method": responses.POST,
                "url": urlparse.urljoin(
                    BaseURL.SHIPENGINE_RPC_URL.value, Endpoints.GET_RATE_FROM_SHIPMENT.value
                ),
                "body": json.dumps(
                    {
                        "shipmentId": "se-141694059",
                        "carrierId": "se-161650",
                        "serviceCode": "usps_first_class_mail",
                        "externalOrderId": None,
                        "items": [],
                        "taxIdentifiers": None,
                        "externalShipmentId": None,
                        "shipDate": "2021-07-28T00:00:00Z",
                        "createdAt": "2021-07-28T16:56:40.257Z",
                        "modifiedAt": "2021-07-28T16:56:40.223Z",
                        "shipmentStatus": "pending",
                        "shipTo": {
                            "name": "James Atkinson",
                            "phone": None,
                            "companyName": None,
                            "addressLine1": "28793 Fox Fire Lane",
                            "addressLine2": None,
                            "addressLine3": None,
                            "cityLocality": "Shell Knob",
                            "stateProvince": "MO",
                            "postalCode": "65747",
                            "countryCode": "US",
                            "addressResidentialIndicator": "yes",
                        },
                        "shipFrom": {
                            "name": "Medals of America",
                            "phone": "800-308-0849",
                            "companyName": None,
                            "addressLine1": "114 Southchase Blvd",
                            "addressLine2": None,
                            "addressLine3": None,
                            "cityLocality": "Fountain Inn",
                            "stateProvince": "SC",
                            "postalCode": "29644",
                            "countryCode": "US",
                            "addressResidentialIndicator": "unknown",
                        },
                        "warehouseId": None,
                        "returnTo": {
                            "name": "Medals of America",
                            "phone": "800-308-0849",
                            "companyName": None,
                            "addressLine1": "114 Southchase Blvd",
                            "addressLine2": None,
                            "addressLine3": None,
                            "cityLocality": "Fountain Inn",
                            "stateProvince": "SC",
                            "postalCode": "29644",
                            "countryCode": "US",
                            "addressResidentialIndicator": "unknown",
                        },
                        "confirmation": "none",
                        "customs": {
                            "contents": "merchandise",
                            "nonDelivery": "return_to_sender",
                            "customsItems": [],
                        },
                        "advancedOptions": {
                            "billToAccount": None,
                            "billToCountryCode": None,
                            "billToParty": None,
                            "billToPostalCode": None,
                            "containsAlcohol": None,
                            "deliveryDutyPaid": None,
                            "dryIce": None,
                            "dryIceWeight": None,
                            "nonMachinable": None,
                            "saturdayDelivery": None,
                            "useUPSGroundFreightPricing": None,
                            "freightClass": None,
                            "customField1": None,
                            "customField2": None,
                            "customField3": None,
                            "originType": None,
                            "shipperRelease": None,
                            "collectOnDelivery": None,
                        },
                        "originType": None,
                        "insuranceProvider": "none",
                        "tags": [],
                        "orderSourceCode": None,
                        "packages": [
                            {
                                "packageCode": "package",
                                "weight": {"value": 2.9, "unit": "ounce"},
                                "dimensions": {
                                    "unit": "inch",
                                    "length": 0,
                                    "width": 0,
                                    "height": 0,
                                },
                                "insuredValue": {"currency": "usd", "amount": 0},
                                "trackingNumber": None,
                                "labelMessages": {
                                    "reference1": "4051492",
                                    "reference2": None,
                                    "reference3": None,
                                },
                                "externalPackageId": None,
                            }
                        ],
                        "totalWeight": {"value": 2.9, "unit": "ounce"},
                        "rateResponse": {
                            "rates": [
                                {
                                    "rateId": "se-784001113",
                                    "rateType": "shipment",
                                    "carrierId": "se-161650",
                                    "shippingAmount": {"currency": "usd", "amount": 3.12},
                                    "insuranceAmount": {"currency": "usd", "amount": 0},
                                    "confirmationAmount": {"currency": "usd", "amount": 0},
                                    "otherAmount": {"currency": "usd", "amount": 0},
                                    "taxAmount": None,
                                    "zone": 5,
                                    "packageType": "package",
                                    "deliveryDays": 3,
                                    "guaranteedService": False,
                                    "estimatedDeliveryDate": "2021-07-31T00:00:00Z",
                                    "carrierDeliveryDays": "3",
                                    "shipDate": "2021-07-28T00:00:00Z",
                                    "negotiatedRate": False,
                                    "serviceType": "USPS First Class Mail",
                                    "serviceCode": "usps_first_class_mail",
                                    "trackable": True,
                                    "carrierCode": "usps",
                                    "carrierNickname": "USPS",
                                    "carrierFriendlyName": "USPS",
                                    "validationStatus": "valid",
                                    "warningMessages": [],
                                    "errorMessages": [],
                                }
                            ],
                            "invalidRates": [],
                            "rateRequestId": "se-85117731",
                            "shipmentId": "se-141694059",
                            "createdAt": "2021-07-28T16:56:40.6148892Z",
                            "status": "completed",
                            "errors": [],
                        },
                    }
                ),
                "status": 200,
                "content_type": "application/json",
            }
        )

        shipengine = stub_shipengine_instance()
        result = shipengine.get_rates_from_shipment(
            shipment={
                "rate_options": {
                    "carrier_ids": ["se-161650"],
                    "service_codes": ["usps_first_class_mail"],
                    "package_types": ["package"],
                },
                "shipment": {
                    "service_code": "",
                    "ship_to": {
                        "name": "James Atkinson",
                        "phone": None,
                        "address_line1": "28793 Fox Fire Lane",
                        "city_locality": "Shell Knob",
                        "state_province": "MO",
                        "postal_code": "65747",
                        "country_code": "US",
                        "address_residential_indicator": "yes",
                    },
                    "ship_from": {
                        "name": "Medals of America",
                        "phone": "800-308-0849",
                        "company_name": None,
                        "address_line1": "114 Southchase Blvd",
                        "address_line2": "",
                        "city_locality": "Fountain Inn",
                        "state_province": "SC",
                        "postal_code": "29644",
                        "country_code": "US",
                        "address_residential_indicator": "no",
                    },
                    "packages": [
                        {
                            "weight": {"value": 2.9, "unit": "ounce"},
                            "label_messages": {"reference1": "4051492"},
                        }
                    ],
                },
            }
        )
        self.assertEqual(result["rateResponse"]["rates"][0]["rateId"], "se-784001113")
