"""Test the instantiation of the Address object and it's validations."""
import pytest

from shipengine_sdk.errors import ValidationError
from shipengine_sdk.models import ErrorCode, ErrorSource, ErrorType
from tests.util.test_helpers import address_with_too_many_lines, empty_address_lines


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
        """DX-1033/DX-1051 - No address lines in the street list."""
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
