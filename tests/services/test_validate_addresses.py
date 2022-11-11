"""Testing the validate_addresses functionality in the ShipEngine SDK."""
import json
import unittest
import urllib.parse as urlparse

import pytest
import responses

from shipengine.enums import BaseURL, Endpoints
from shipengine.errors import ShipEngineError, RateLimitExceededError

from ..util import stub_shipengine_instance, valid_commercial_address

expected_response_body = [
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

rate_limit_exceeded_response_body = {
    "message": "API rate limit exceeded",
}


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
                "body": json.dumps(expected_response_body),
                "status": 200,
                "content_type": "application/json",
            }
        )

        shipengine = stub_shipengine_instance()
        result = shipengine.validate_addresses(valid_commercial_address())
        self.assertEqual(result[0]["status"], "verified")

    @responses.activate
    def test_validate_addresses_when_rate_limit_exceeded_and_invalid_retry_value(self) -> None:
        """
        Tests that the validate_addresses method handles unexpected Retry-After
        header values upon the rate limit being exceeded.
        """
        responses.add(
            **{
                "method": responses.POST,
                "url": urlparse.urljoin(
                    BaseURL.SHIPENGINE_RPC_URL.value, Endpoints.ADDRESSES_VALIDATE.value
                ),
                "body": json.dumps(rate_limit_exceeded_response_body),
                "status": 429,
                "content_type": "application/json",
                "headers": {
                    "Retry-After": "10.1"
                }
            }
        )

        shipengine = stub_shipengine_instance()
        with pytest.raises(ShipEngineError) as exc_info:
            shipengine.validate_addresses(valid_commercial_address())
        
        self.assertEqual(exc_info.value.message, 'Unexpected Retry-After header value.')

    @responses.activate
    def test_validate_addresses_when_rate_limit_exceeded(self) -> None:
        """
        Tests that the validate_addresses method handles the rate limit being exceeded
        with the appropriate error.
        """
        responses.add(
            **{
                "method": responses.POST,
                "url": urlparse.urljoin(
                    BaseURL.SHIPENGINE_RPC_URL.value, Endpoints.ADDRESSES_VALIDATE.value
                ),
                "body": json.dumps(rate_limit_exceeded_response_body),
                "status": 429,
                "content_type": "application/json",
                "headers": {
                    "Retry-After": "0",  # NOTE: we use 0 here so that the test doesn't block
                    "x-shipengine-requestid": "56b2b0a3-8df5-4cfe-95f0-d7efefdda2ad"
                }
            }
        )

        shipengine = stub_shipengine_instance()
        with pytest.raises(RateLimitExceededError):
            shipengine.validate_addresses(valid_commercial_address())
