"""Initial Docstring"""
from shipengine_sdk import ShipEngine
from shipengine_sdk.models.address import Address, AddressValidateResult
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


def valid_commercial_address() -> Address:
    """
    Return a test Address object with valid commercial
    address information.
    """
    return Address(
        street=["4 Jersey St", "ste 200"],
        city_locality="Boston",
        state_province="MA",
        postal_code="02215",
        country_code="US",
    )


def validate_an_address(address: Address) -> AddressValidateResult:
    return stub_shipengine_instance().validate_address(address=address)


class TestValidateAddress:
    def test_valid_residential_address(self):
        """DX-1024 - Valid residential address."""
        residential_address = valid_residential_address()
        validated_address = validate_an_address(residential_address)
        address = validated_address.normalized_address

        assert type(validated_address) is AddressValidateResult
        assert validated_address.is_valid is True
        assert address is not None
        assert (
            address.street[0]
            == (residential_address.street[0] + " " + residential_address.street[1])
            .replace(".", "")
            .upper()
        )
        assert address.city_locality == residential_address.city_locality.upper()
        assert address.state_province == residential_address.state_province.upper()
        assert address.postal_code == residential_address.postal_code
        assert address.country_code == residential_address.country_code.upper()
        assert address.is_residential is True

    def test_valid_commercial_address(self):
        """DX-1025 - Valid commercial address."""
        commercial_address = valid_commercial_address()
        validated_address = validate_an_address(commercial_address)
        address = validated_address.normalized_address

        assert type(validated_address) is AddressValidateResult
        assert validated_address.is_valid is True
        assert len(validated_address.messages) == 0
        assert address is not None
        assert (
            address.street[0]
            == (commercial_address.street[0] + " " + commercial_address.street[1])
            .replace(".", "")
            .upper()
        )
        assert address.city_locality == commercial_address.city_locality.upper()
        assert address.state_province == commercial_address.state_province.upper()
        assert address.postal_code == commercial_address.postal_code
        assert address.country_code == commercial_address.country_code.upper()
        assert address.is_residential is False
