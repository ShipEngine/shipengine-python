"""Initial Docstring"""
import re

from shipengine_sdk import ShipEngine
from shipengine_sdk.errors import ValidationError
from shipengine_sdk.models import ErrorCode, ErrorSource, ErrorType
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


def validate_an_address(address: Address) -> AddressValidateResult:
    """
    Helper function that passes a config dictionary into the ShipEngine object to instantiate
    it and calls the `validate_address` method, providing it the `address` that is passed into
    this function.
    """
    return stub_shipengine_instance().validate_address(address=address)


def us_valid_address_assertions(
    original_address: Address,
    validated_address: AddressValidateResult,
    expected_residential_indicator,
) -> None:
    """A set of common assertions that are regularly made on the commercial US address used for testing."""
    address = validated_address.normalized_address
    assert type(validated_address) is AddressValidateResult
    assert validated_address.is_valid is True
    assert type(address) is Address
    assert len(validated_address.info) == 0
    assert len(validated_address.warnings) == 0
    assert len(validated_address.errors) == 0
    assert address is not None
    assert address.city_locality == original_address.city_locality.upper()
    assert address.state_province == original_address.state_province.upper()
    assert address.postal_code == original_address.postal_code
    assert address.country_code == original_address.country_code.upper()
    assert address.is_residential is expected_residential_indicator


def canada_valid_address_assertions(
    original_address: Address,
    validated_address: AddressValidateResult,
    expected_residential_indicator,
) -> None:
    """A set of common assertions that are regularly made on the canadian_address used for testing."""
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


class TestValidateAddress:
    def test_valid_residential_address(self) -> None:
        """DX-1024 - Valid residential address."""
        residential_address = valid_residential_address()
        validated_address = validate_an_address(residential_address)
        address = validated_address.normalized_address

        us_valid_address_assertions(
            original_address=residential_address,
            validated_address=validated_address,
            expected_residential_indicator=True,
        )
        assert (
            address.street[0]
            == (residential_address.street[0] + " " + residential_address.street[1])
            .replace(".", "")
            .upper()
        )

    def test_valid_commercial_address(self) -> None:
        """DX-1025 - Valid commercial address."""
        commercial_address = valid_commercial_address()
        validated_address = validate_an_address(commercial_address)
        address = validated_address.normalized_address

        us_valid_address_assertions(
            original_address=commercial_address,
            validated_address=validated_address,
            expected_residential_indicator=False,
        )
        assert (
            address.street[0]
            == (commercial_address.street[0] + " " + commercial_address.street[1])
            .replace(".", "")
            .upper()
        )

    def test_multi_line_address(self) -> None:
        """DX-1027 - Validate multiline address."""
        valid_multi_line_address = multi_line_address()
        validated_address = validate_an_address(valid_multi_line_address)
        address = validated_address.normalized_address

        us_valid_address_assertions(
            original_address=valid_multi_line_address,
            validated_address=validated_address,
            expected_residential_indicator=False,
        )
        assert (
            address.street[0]
            == (valid_multi_line_address.street[0] + " " + valid_multi_line_address.street[1])
            .replace(".", "")
            .upper()
        )
        assert address.street[1] == valid_multi_line_address.street[2].upper()

    def test_numeric_postal_code(self) -> None:
        """DX-1028 - Validate numeric postal code."""
        residential_address = valid_residential_address()
        validated_address = validate_an_address(residential_address)
        us_valid_address_assertions(
            original_address=residential_address,
            validated_address=validated_address,
            expected_residential_indicator=True,
        )
        assert re.match(r"\d", validated_address.normalized_address.postal_code)

    def test_alpha_postal_code(self):
        """DX-1029 - Alpha postal code."""
        canadian_address = valid_canadian_address()
        validated_address = validate_an_address(canadian_address)
        canada_valid_address_assertions(
            original_address=canadian_address,
            validated_address=validated_address,
            expected_residential_indicator=False,
        )

    def test_unknown_address(self):
        """DX-1026 - Validate address of unknown address."""
        address = unknown_address()
        validated_address = validate_an_address(address)
        canada_valid_address_assertions(
            original_address=address,
            validated_address=validated_address,
            expected_residential_indicator=None,
        )

    def test_address_with_non_latin_chars(self):
        """DX-1030 - non-latin characters."""
        non_latin = non_latin_address()
        validated_address = validate_an_address(non_latin)
        address = validated_address.normalized_address

        assert validated_address.is_valid is True
        assert address is not None
        assert type(address) is Address
        assert address.street[0] == "68 Kamitobatsunodacho"
        assert address.city_locality == "Kyoto-Shi Minami-Ku"
        assert address.state_province == "Kyoto"
        assert address.postal_code == non_latin.postal_code
        assert address.country_code == non_latin.country_code
        assert address.is_residential is False
        assert len(address.street) == 1

    def test_address_with_warnings(self):
        """DX-1031 - validate with warnings."""
        warnings_address = address_with_warnings()
        validated_address = validate_an_address(warnings_address)
        address = validated_address.normalized_address

        assert type(validated_address) is AddressValidateResult
        assert validated_address.is_valid is True
        assert type(address) is Address
        assert len(validated_address.info) == 0
        assert len(validated_address.warnings) != 0
        assert (
            validated_address.warnings[0]["code"]
            == ErrorCode.PARTIALLY_VERIFIED_TO_PREMISE_LEVEL.value
        )
        assert (
            validated_address.warnings[0]["message"]
            == "This address has been verified down to the house/building level (highest possible accuracy with the provided data)"  # noqa
        )
        assert len(validated_address.errors) == 0
        assert address is not None
        assert address.city_locality == validated_address.normalized_address.city_locality
        assert address.state_province == validated_address.normalized_address.state_province.title()
        assert address.postal_code == "M6K 3C3"
        assert address.country_code == validated_address.normalized_address.country_code.upper()
        assert address.is_residential is True

    def test_address_with_errors(self):
        """DX-1032 - Validate with error messages."""
        error_address = address_with_errors()
        validated_address = validate_an_address(error_address)
        address = validated_address.normalized_address

        assert type(validated_address) is AddressValidateResult
        assert validated_address.is_valid is False
        assert address is None
        assert len(validated_address.info) == 0
        assert len(validated_address.warnings) != 0
        assert validated_address.warnings[0]["message"] == "Address not found"
        assert len(validated_address.errors) != 0
        assert validated_address.errors[0]["code"] == ErrorCode.ADDRESS_NOT_FOUND.value
        assert validated_address.errors[0]["message"] == "Invalid City, State, or Zip"
        assert validated_address.errors[1]["code"] == ErrorCode.ADDRESS_NOT_FOUND.value
        assert validated_address.errors[1]["message"] == "Insufficient or Incorrect Address Data"

    def test_missing_city_state_and_postal_code(self):
        """DX-1035 - Missing city, state, and postal code."""
        try:
            address_missing_required_fields()
        except ValidationError as err:
            assert err.request_id is None
            assert err.source is ErrorSource.SHIPENGINE.value
            assert err.error_type is ErrorType.VALIDATION.value
            assert err.error_code is ErrorCode.FIELD_VALUE_REQUIRED.value
            assert (
                err.message
                == "Invalid address. Either the postal code or the city/locality and state/province must be specified."
            )  # noqa
