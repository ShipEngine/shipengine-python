"""Test the instantiation of the Address object and it's validations."""
import pytest

from shipengine_sdk.errors import ValidationError
from shipengine_sdk.models import ErrorCode, ErrorSource, ErrorType
from shipengine_sdk.models.address import Address


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


def address_line_assertions(err: ValidationError, variant: str) -> None:
    """"""
    assert type(err) is ValidationError
    assert err.request_id is None
    assert err.source is ErrorSource.SHIPENGINE.value
    assert err.error_type is ErrorType.VALIDATION.value

    if variant == "empty_address_lines":
        assert err.message == "Invalid address. At least one address line is required."
        assert err.error_code is ErrorCode.FIELD_VALUE_REQUIRED.value
    elif variant == "too_many_address_lines":
        assert err.message == "Invalid address. No more than 3 street lines are allowed."
        assert err.error_code is ErrorCode.INVALID_FIELD_VALUE.value


class TestAddress:
    def test_no_address_lines(self):
        """DX-1033 - Too many address lines in the street list."""
        try:
            empty_address_lines()
        except ValidationError as err:
            address_line_assertions(err, "empty_address_lines")
            with pytest.raises(ValidationError):
                empty_address_lines()

    def test_address_with_too_many_lines(self):
        """DX-1034 - Too many address lines."""
        try:
            address_with_too_many_lines()
        except ValidationError as err:
            address_line_assertions(err, "too_many_address_lines")
