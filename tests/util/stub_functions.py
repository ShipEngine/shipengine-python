"""Helper functions that return stub data for the test suite."""

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


def address_with_warnings() -> Address:
    """Return a test Address object that will cause the server to return warning messages."""
    return Address(
        street=["170 Warning Blvd", "Apartment 32-B"],
        city_locality="Toronto",
        state_province="ON",
        postal_code="M6K 3C3",
        country_code="CA",
    )


def address_with_errors() -> Address:
    """Return a test Address object that will cause the server to return an error message."""
    return Address(
        street=["4 Invalid St"],
        city_locality="Boston",
        state_province="MA",
        postal_code="02215",
        country_code="US",
    )


def valid_canadian_address() -> Address:
    """Return an Address object with a valid canadian address."""
    return Address(
        street=["170 Princes Blvd", "Ste 200"],
        city_locality="Toronto",
        state_province="ON",
        postal_code="M6K 3C3",
        country_code="CA",
    )


def multi_line_address() -> Address:
    """Returns a valid multiline address."""
    return Address(
        street=["4 Jersey St", "ste 200", "1st Floor"],
        city_locality="Boston",
        state_province="MA",
        postal_code="02215",
        country_code="US",
    )


def non_latin_address() -> Address:
    """Return an address with non-latin characters."""
    return Address(
        street=["上鳥羽角田町６８"],
        city_locality="南区",
        state_province="京都",
        postal_code="601-8104",
        country_code="JP",
    )


def unknown_address() -> Address:
    """
    Return an address that will make the server respond with an
    address with an unknown residential flag.
    """
    return Address(
        street=["4 Unknown St"],
        city_locality="Toronto",
        state_province="ON",
        postal_code="M6K 3C3",
        country_code="CA",
    )


def address_missing_required_fields() -> Address:
    """Return an address that is missing a state, city, and postal_code to return a ValidationError.."""
    return Address(
        street=["4 Jersey St"],
        city_locality="",
        state_province="",
        postal_code="",
        country_code="US",
    )


def address_missing_country() -> Address:
    """Return an address that is only missing the country_code."""
    return Address(
        street=["4 Jersey St", "Apt. 2b"],
        city_locality="Boston",
        state_province="MA",
        postal_code="02215",
        country_code="",
    )


def address_with_invalid_country() -> Address:
    """Return an address that has an invalid country_code specified."""
    return Address(
        street=["4 Jersey St", "Apt. 2b"],
        city_locality="Boston",
        state_province="MA",
        postal_code="02215",
        country_code="RZ",
    )


def get_server_side_error() -> Address:
    """Return an address that will cause the server to return a 500 server error."""
    return Address(
        street=["500 Server Error"],
        city_locality="Boston",
        state_province="MA",
        postal_code="02215",
        country_code="US",
    )
