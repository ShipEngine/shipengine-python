"""Test the normalize address method of the ShipEngine SDK."""
import re

from shipengine_sdk.errors import ShipEngineError, ValidationError
from shipengine_sdk.models import Address, ErrorCode, ErrorSource, ErrorType

from ..util.test_helpers import (
    address_missing_required_fields,
    address_with_errors,
    address_with_single_error,
    address_with_warnings,
    multi_line_address,
    non_latin_address,
    normalize_an_address,
    unknown_address,
    valid_address_assertions,
    valid_canadian_address,
    valid_commercial_address,
    valid_residential_address,
)


class TestNormalizeAddress:
    TEST_METHOD: str = "normalize"

    def test_normalize_valid_residential_address(self) -> None:
        """DX-1041 - Normalize valid residential address."""
        residential_address = valid_residential_address()
        normalized = normalize_an_address(residential_address)

        valid_address_assertions(
            test_method=self.TEST_METHOD,
            locale="domestic",
            original_address=residential_address,
            returned_address=normalized,
            expected_residential_indicator=True,
        )

    def test_normalize_valid_commercial_address(self) -> None:
        """DX-1042 - Normalize valid commercial address."""
        commercial_address = valid_commercial_address()
        normalized = normalize_an_address(commercial_address)

        valid_address_assertions(
            test_method=self.TEST_METHOD,
            locale="domestic",
            original_address=commercial_address,
            returned_address=normalized,
            expected_residential_indicator=False,
        )

    def test_normalize_unknown_address(self) -> None:
        """DX-1043 - Normalize unknown address."""
        address = unknown_address()
        normalized = normalize_an_address(address)

        valid_address_assertions(
            test_method=self.TEST_METHOD,
            locale="international",
            original_address=address,
            returned_address=normalized,
            expected_residential_indicator=None,
        )

    def test_normalize_multi_line_address(self) -> None:
        """DX-1044 - Normalize multi-line address."""
        multi_line = multi_line_address()
        normalized = normalize_an_address(multi_line)

        valid_address_assertions(
            test_method=self.TEST_METHOD,
            locale="domestic",
            original_address=multi_line,
            returned_address=normalized,
            expected_residential_indicator=False,
        )
        assert (
            normalized.street[0]
            == (multi_line.street[0] + " " + multi_line.street[1]).replace(".", "").upper()
        )
        assert normalized.street[1] == multi_line.street[2].upper()

    def test_normalize_numeric_postal_code(self) -> None:
        """DX-1045 - Normalize address with numeric postal code."""
        address = valid_residential_address()
        normalized = normalize_an_address(address)

        valid_address_assertions(
            test_method=self.TEST_METHOD,
            locale="domestic",
            original_address=address,
            returned_address=normalized,
            expected_residential_indicator=True,
        )
        assert re.match(r"\d", normalized.postal_code)

    def test_normalize_alpha_postal_code(self) -> None:
        """DX-1046 - Normalize address with alpha-numeric postal code."""
        address = valid_canadian_address()
        normalized = normalize_an_address(address)

        valid_address_assertions(
            test_method=self.TEST_METHOD,
            locale="international",
            original_address=address,
            returned_address=normalized,
            expected_residential_indicator=False,
        )

    def test_normalize_non_latin_chars(self) -> None:
        """DX-1047 - Normalize address with non-latin characters."""
        non_latin = non_latin_address()
        normalized = normalize_an_address(non_latin)

        assert type(normalized) is Address
        assert normalized.street[0] == "68 Kamitobatsunodacho"
        assert normalized.city_locality == "Kyoto-Shi Minami-Ku"
        assert normalized.state_province == "Kyoto"
        assert normalized.postal_code == non_latin.postal_code
        assert normalized.country_code == non_latin.country_code
        assert normalized.is_residential is False
        assert len(normalized.street) == 1

    def test_normalize_with_warnings(self) -> None:
        """DX-1048 - Normalize address with warnings."""
        warning_address = address_with_warnings()
        normalized = normalize_an_address(warning_address)

        assert type(normalized) is Address
        assert normalized is not None
        assert normalized.city_locality == warning_address.city_locality
        assert normalized.state_province == warning_address.state_province.title()
        assert normalized.postal_code == "M6K 3C3"
        assert normalized.country_code == warning_address.country_code.upper()
        assert normalized.is_residential is True

    def test_normalize_with_single_error_message(self) -> None:
        """DX-1049 - Normalize address with single error message."""
        single_error = address_with_single_error()
        try:
            normalize_an_address(single_error)
        except ShipEngineError as err:
            assert err.request_id is not None
            assert err.request_id.startswith("req_") is True
            assert err.source is ErrorSource.SHIPENGINE.value
            assert err.error_type is ErrorType.ERROR.value
            assert err.error_code == ErrorCode.MINIMUM_POSTAL_CODE_VERIFICATION_FAILED.value
            assert err.message == "Invalid address. Insufficient or inaccurate postal code"

    def test_normalize_with_multiple_errors(self) -> None:
        """DX-1050 - Normalize address with multiple error messages."""
        errors_address = address_with_errors()
        try:
            normalize_an_address(errors_address)
        except ShipEngineError as err:
            assert err.request_id is not None
            assert err.request_id.startswith("req_") is True
            assert err.source is ErrorSource.SHIPENGINE.value
            assert err.error_type is ErrorType.ERROR.value
            assert err.error_code is ErrorCode.INVALID_ADDRESS.value
            assert (
                err.message
                == "Invalid address.\nInvalid City, State, or Zip\nInsufficient or Incorrect Address Data"
            )

    def test_normalize_missing_city_state_and_postal_code(self) -> None:
        """DX-1053 & DX-1054 - Missing city, state, and postal code."""
        try:
            address_missing_required_fields()
        except ValidationError as err:
            assert err.request_id is None
            assert err.source is ErrorSource.SHIPENGINE.value
            assert err.error_type is ErrorType.VALIDATION.value
            assert err.error_code is ErrorCode.FIELD_VALUE_REQUIRED.value
            assert (
                err.message
                == "Invalid address. Either the postal code or the city/locality and state/province must be specified."  # noqa
            )
