"""Testing basic ShipEngineClient functionality."""
import pytest
import responses

from shipengine_sdk import ShipEngine
from shipengine_sdk.errors import ClientSystemError
from shipengine_sdk.models import ErrorCode, ErrorSource, ErrorType
from shipengine_sdk.models.address import Address
from shipengine_sdk.models.enums import Endpoints


def validate_address(address):
    shipengine = ShipEngine(
        dict(
            api_key="baz",
            base_uri=Endpoints.TEST_RPC_URL.value,
            page_size=50,
            retries=2,
            timeout=10,
        )
    )
    return shipengine.validate_address(address)


def valid_residential_address() -> Address:
    return Address(
        street=["4 Jersey St"],
        city_locality="Boston",
        state_province="MA",
        postal_code="02215",
        country_code="US",
    )


def get_500_server_error() -> Address:
    return Address(
        street=["500 Server Error"],
        city_locality="Boston",
        state_province="MA",
        postal_code="02215",
        country_code="US",
    )


class TestShipEngineClient:
    @responses.activate
    def test_500_server_response(self):
        responses.add(
            responses.POST,
            Endpoints.TEST_RPC_URL.value,
            json={
                "jsonrpc": "2.0",
                "id": "req_DezVNUvRkAP819f3JeqiuS",
                "error": {
                    "code": "-32603",
                    "message": "Unable to connect to the database",
                    "data": {"source": "shipengine", "type": "system", "code": "unspecified"},
                },
            },
            status=500,
        )
        try:
            validate_address(get_500_server_error())
        except ClientSystemError as e:
            assert e.message == "Unable to connect to the database"
            assert e.request_id is not None
            assert e.source == ErrorSource.SHIPENGINE.value
            assert e.error_type == ErrorType.SYSTEM.value
            assert e.error_code == ErrorCode.UNSPECIFIED.value
            with pytest.raises(ClientSystemError):
                validate_address(get_500_server_error())

    @responses.activate
    def test_404_server_response(self):
        responses.add(
            responses.POST,
            Endpoints.TEST_RPC_URL.value,
            json={
                "jsonrpc": "2.0",
                "id": "req_DezVNUvRkAP819f3JeqiuS",
                "error": {
                    "code": "-32603",
                    "message": "Content not found.",
                    "data": {"source": "shipengine", "type": "system", "code": "not_found"},
                },
            },
            status=404,
        )
        try:
            validate_address(valid_residential_address())
        except ClientSystemError as e:
            assert e.message == "Content not found."
            assert e.request_id is not None
            assert e.source == ErrorSource.SHIPENGINE.value
            assert e.error_type == ErrorType.SYSTEM.value
            assert e.error_code == ErrorCode.NOT_FOUND.value
        with pytest.raises(ClientSystemError):
            validate_address(valid_residential_address())
