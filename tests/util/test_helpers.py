"""Test data as functions and common assertion helper functions."""
from typing import Dict, Optional, Union

from shipengine_sdk import ShipEngine, ShipEngineConfig
from shipengine_sdk.models import (
    Address,
    AddressValidateResult,
    Endpoints,
    TrackingQuery,
)


def stub_config(
    retries: int = 1,
) -> Dict[str, any]:
    """
    Return a test configuration dictionary to be used
    when instantiating the ShipEngine object.
    """
    return dict(
        api_key="baz",
        base_uri=Endpoints.TEST_RPC_URL.value,
        page_size=50,
        retries=retries,
        timeout=15,
    )


def stub_shipengine_config() -> ShipEngineConfig:
    """Return a valid test ShipEngineConfig object."""
    return ShipEngineConfig(config=stub_config())


def configurable_stub_shipengine_instance(config: Dict[str, any]) -> ShipEngine:
    """"""
    return ShipEngine(config=config)


def stub_shipengine_instance() -> ShipEngine:
    """Return a test instance of the ShipEngine object."""
    return ShipEngine(config=stub_config())


def address_with_all_fields() -> Address:
    """Return an address with all fields populated."""
    return Address(
        name="ShipEngine",
        company="Auctane",
        phone="123456789",
        street=["4 Jersey St", "Apt. 2b"],
        city_locality="Boston",
        state_province="MA",
        postal_code="02215",
        country_code="US",
    )


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


def address_with_single_error() -> Address:
    """Return a test Address object that will cause the server to return a single error message."""
    return Address(
        street=["170 Error Blvd"],
        city_locality="Boston",
        state_province="MA",
        postal_code="02215",
        country_code="US",
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


def empty_address_lines() -> Address:
    """Returns an invalid address with empty street list."""
    return Address(
        street=list(),
        city_locality="Boston",
        state_province="MA",
        postal_code="02215",
        country_code="US",
    )


def address_with_too_many_lines() -> Address:
    """Return an address with too many address lines in the street list."""
    return Address(
        street=["4 Jersey St", "ste 200", "1st Floor", "Room B"],
        city_locality="Boston",
        state_province="MA",
        postal_code="02215",
        country_code="US",
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


def address_with_invalid_state() -> Address:
    """Return an address with an invalid state value."""
    return Address(
        street=["4 Jersey St", "Apt. 2b"],
        city_locality="Boston",
        state_province="&$",
        postal_code="02215",
        country_code="US",
    )


def address_with_invalid_postal_code() -> Address:
    """Return an address with an invalid postal code."""
    return Address(
        street=["4 Jersey St", "Apt. 2b"],
        city_locality="Boston",
        state_province="MA",
        postal_code="2$1*5",
        country_code="US",
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


def validate_an_address(address: Address) -> AddressValidateResult:
    """
    Helper function that passes a config dictionary into the ShipEngine object to instantiate
    it and calls the `validate_address` method, providing it the `address` that is passed into
    this function.
    """
    return stub_shipengine_instance().validate_address(address=address)


def normalize_an_address(address: Address) -> Address:
    """
    Helper function that passes a config dictionary into the ShipEngine object to instantiate
    it and calls the `normalize_address` method, providing it the `address` that is passed into
    this function.
    """
    return stub_shipengine_instance().normalize_address(address=address)


def track_a_package(tracking_data: Union[str, Dict[str, any], TrackingQuery]):
    """"""
    return stub_shipengine_instance().track_package(tracking_data=tracking_data)


def stub_get_carrier_accounts(carrier_code: Optional[str] = None):
    """Helper function that passes the `get_carrier_accounts` method a given carrier_code or None."""
    return stub_shipengine_instance().get_carrier_accounts(carrier_code=carrier_code)


# Assertion helper functions


def valid_address_assertions(
    test_method: str,
    locale: str,
    original_address: Address,
    returned_address: Union[Address, AddressValidateResult],
    expected_residential_indicator,
) -> None:
    """
    A set of common assertions that are regularly made on the commercial US address
    used for testing the `validate_address` or `normalize_address` methods, based on
    the `test_method` that is passed in. It also makes different sets of assertions
    depending on what `locale` is passed in.
    """
    address = (
        returned_address.normalized_address
        if type(returned_address) is AddressValidateResult
        else returned_address
    )
    if locale == "domestic":
        if test_method == "validate":
            assert type(returned_address) is AddressValidateResult
            assert returned_address.is_valid is True
            assert type(address) is Address
            assert len(returned_address.info) == 0
            assert len(returned_address.warnings) == 0
            assert len(returned_address.errors) == 0
            assert address is not None
            assert address.city_locality == original_address.city_locality.upper()
            assert address.state_province == original_address.state_province.upper()
            assert address.postal_code == original_address.postal_code
            assert address.country_code == original_address.country_code.upper()
            assert address.is_residential is expected_residential_indicator
        elif test_method == "normalize":
            assert type(returned_address) is Address
            assert returned_address.city_locality == original_address.city_locality.upper()
            assert returned_address.state_province == original_address.state_province.upper()
            assert returned_address.postal_code == original_address.postal_code
            assert returned_address.country_code == original_address.country_code.upper()
            assert returned_address.is_residential is expected_residential_indicator
    elif locale == "international":
        if test_method == "validate":
            canada_valid_avs_assertions(
                original_address=original_address,
                validated_address=returned_address,
                expected_residential_indicator=expected_residential_indicator,
            )
        if test_method == "normalize":
            canada_valid_normalize_assertions(
                original_address=original_address,
                normalized_address=returned_address,
                expected_residential_indicator=expected_residential_indicator,
            )


def canada_valid_avs_assertions(
    original_address: Address,
    validated_address: AddressValidateResult,
    expected_residential_indicator,
) -> None:
    """
    A set of common assertions that are regularly made on the canadian_address
    used for testing `validate_address`.
    """
    address = validated_address.normalized_address
    assert type(validated_address) is AddressValidateResult
    assert validated_address.is_valid is True
    assert type(address) is Address
    assert len(validated_address.info) == 0
    assert len(validated_address.warnings) == 0
    assert len(validated_address.errors) == 0
    assert address is not None
    assert address.city_locality == original_address.city_locality
    assert address.state_province == original_address.state_province.title()
    assert address.postal_code == "M6 K 3 C3"
    assert address.country_code == original_address.country_code.upper()
    assert address.is_residential is expected_residential_indicator


def us_valid_normalize_assertions(
    original_address: Address,
    normalized_address: Address,
    expected_residential_indicator,
) -> None:
    """
    A set of common assertions that are regularly made on the commercial US address
    used for `normalized_address` testing.
    """
    assert type(normalized_address) is Address
    assert normalized_address.city_locality == original_address.city_locality.upper()
    assert normalized_address.state_province == original_address.state_province.upper()
    assert normalized_address.postal_code == original_address.postal_code
    assert normalized_address.country_code == original_address.country_code.upper()
    assert normalized_address.is_residential is expected_residential_indicator


def canada_valid_normalize_assertions(
    original_address: Address,
    normalized_address: Address,
    expected_residential_indicator,
) -> None:
    """
    A set of common assertions that are regularly made on the canadian_address
    used for testing `validate_address`.
    """
    assert type(normalized_address) is Address
    assert normalized_address.city_locality == original_address.city_locality
    assert normalized_address.state_province == original_address.state_province.title()
    assert normalized_address.postal_code == "M6 K 3 C3"
    assert normalized_address.country_code == original_address.country_code.upper()
    assert normalized_address.is_residential is expected_residential_indicator
