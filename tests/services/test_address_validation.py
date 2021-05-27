"""Initial Docstring"""
from shipengine_sdk import ShipEngine
from shipengine_sdk.models.address import Address
from shipengine_sdk.models.enums import Endpoints


def stub_config() -> dict:
    """
    Return a test configuration dictionary to be used
    when instantiating the ShipEngine object.
    """
    return dict(
        api_key="baz", base_uri=Endpoints.TEST_RPC_URL.value, page_size=50, retries=2, timeout=15
    )


def stub_shipengine_instance() -> ShipEngine:
    """Return a test instance of the ShipEngine object."""
    return ShipEngine(stub_config())


def valid_residential_address() -> Address:
    """
    Return a test Address object with valid residential
    address information.
    """
    return Address(
        street=["4 Jersey St", "Apt. 2b"],
        city_locality="Boston",
        state_province="MA",
        postal_code="02215",
        country_code="US",
    )


# class TestValidateAddress:
#     def test_valid_residential_address(self) -> None:
#         shipengine = stub_shipengine_instance()
#         validated_address = shipengine.validate_address(valid_residential_address())
#         assert type(validated_address) is AddressValidateResult
