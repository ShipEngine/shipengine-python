"""Testing basic ShipEngineClient functionality."""
import pytest
import responses

from shipengine_sdk import ShipEngine
from shipengine_sdk.errors import ClientSystemError
from shipengine_sdk.models.address import Address
from shipengine_sdk.models.enums import Endpoints


def get_500_server_error():
    error_address = Address(
        street=["500 Server Error"],
        city_locality="Boston",
        state_province="MA",
        postal_code="02215",
        country_code="US",
    )
    shipengine = ShipEngine(
        dict(
            api_key="baz",
            base_uri=Endpoints.TEST_RPC_URL.value,
            page_size=50,
            retries=2,
            timeout=10,
        )
    )
    return shipengine.validate_address(error_address)


@responses.activate
def test_500_server_response():
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
    with pytest.raises(ClientSystemError):
        get_500_server_error()
