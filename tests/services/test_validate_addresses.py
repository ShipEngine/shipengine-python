"""Testing the validate_addresses functionality in the ShipEngine SDK."""
import json
import unittest
import urllib.parse as urlparse

import responses

from shipengine_sdk.enums import BaseURL, Endpoints

from ..util import stub_shipengine_instance, valid_commercial_address


class TestValidateAddresses(unittest.TestCase):
    @responses.activate
    def test_validate_addresses(self) -> None:
        """
        Tests that the validate_addresses method properly interacts with ShipEngine API,
        and returns a successful response from ShipEngine API.
        """
        responses.add(
            **{
                "method": responses.POST,
                "url": urlparse.urljoin(
                    BaseURL.SHIPENGINE_RPC_URL.value, Endpoints.ADDRESSES_VALIDATE.value
                ),
                "body": json.dumps(
                    [
                        {
                            "status": "verified",
                            "original_address": {
                                "name": "ShipEngine",
                                "phone": "1-123-123-1234",
                                "company_name": "None",
                                "address_line1": "3800 N Lamar Blvd",
                                "address_line2": "ste 220",
                                "address_line3": "None",
                                "city_locality": "Austin",
                                "state_province": "TX",
                                "postal_code": "78756",
                                "country_code": "US",
                                "address_residential_indicator": "unknown",
                            },
                            "matched_address": {
                                "name": "SHIPENGINE",
                                "phone": "1-123-123-1234",
                                "company_name": "None",
                                "address_line1": "3800 N LAMAR BLVD STE 220",
                                "address_line2": "",
                                "address_line3": "None",
                                "city_locality": "AUSTIN",
                                "state_province": "TX",
                                "postal_code": "78756-0003",
                                "country_code": "US",
                                "address_residential_indicator": "no",
                            },
                            "messages": [],
                        }
                    ]
                ),
                "status": 200,
                "content_type": "application/json",
            }
        )

        shipengine = stub_shipengine_instance()
        result = shipengine.validate_addresses(valid_commercial_address())
        self.assertEqual(result[0]["status"], "verified")
