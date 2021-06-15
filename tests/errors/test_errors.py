"""Tests for the ShipEngine SDK Errors"""
import pytest

from shipengine_sdk.errors import (
    AccountStatusError,
    BusinessRuleError,
    ClientSecurityError,
    ClientTimeoutError,
    InvalidFieldValueError,
    RateLimitExceededError,
    ShipEngineError,
    ValidationError,
)


def shipengine_error_defaults() -> ShipEngineError:
    """Return a ShipEngineError that only has a message string passed in."""
    raise ShipEngineError(message="Testing the defaults for this error.")


def shipengine_error():
    """Return a ShipEngineError that have all fields populated by valid values."""
    raise ShipEngineError(
        request_id="req_a523b1b19bd54054b7eb953f000e7f15",
        message="The is a test exception",
        source="shipengine",
        error_type="validation",
        error_code="invalid_address",
        url="https://google.com",
    )


def shipengine_error_with_no_error_type() -> ShipEngineError:
    """Return a ShipEngineError that only has the error_type set to None."""
    raise ShipEngineError(
        request_id="req_a523b1b19bd54054b7eb953f000e7f15",
        message="The is a test exception",
        source="shipengine",
        error_type=None,
        error_code="invalid_address",
    )


def shipengine_error_with_bad_error_type() -> ShipEngineError:
    """Return a ShipEngineError that has an invalid error_type."""
    raise ShipEngineError(
        request_id="req_a523b1b19bd54054b7eb953f000e7f15",
        message="The is a test exception",
        source="shipengine",
        error_type="tracking",
        error_code="invalid_address",
    )


def shipengine_error_with_bad_error_source() -> ShipEngineError:
    """Return a ShipEngineError that has an invalid error_source."""
    raise ShipEngineError(
        request_id="req_a523b1b19bd54054b7eb953f000e7f15",
        message="The is a test exception",
        source="wayne_enterprises",
        error_type="validation",
        error_code="invalid_address",
    )


def shipengine_error_with_bad_error_code() -> ShipEngineError:
    """Return a ShipEngineError that has an invalid error_code."""
    raise ShipEngineError(
        request_id="req_a523b1b19bd54054b7eb953f000e7f15",
        message="The is a test exception",
        source="shipengine",
        error_type="validation",
        error_code="failure",
    )


def account_status() -> AccountStatusError:
    raise AccountStatusError("There was an issue with your ShipEngine account.")


def business_rule_error() -> BusinessRuleError:
    raise BusinessRuleError("Invalid postal code.")


def security_error() -> ClientSecurityError:
    raise ClientSecurityError("Unauthorized - you API key is invalid.")


def validation_error() -> ValidationError:
    raise ValidationError("The value provided must be an integer - object provided.")


def client_timeout_error() -> ClientTimeoutError:
    raise ClientTimeoutError(300, "shipengine", "req_a523b1b19bd54054b7eb953f000e7f15")


def invalid_filed_value_error() -> InvalidFieldValueError:
    raise InvalidFieldValueError("is_residential", "Value should be int but got str.", 1)


def rate_limit_exceeded_error() -> RateLimitExceededError:
    raise RateLimitExceededError(300, "shipengine", "req_a523b1b19bd54054b7eb953f000e7f15")


class TestShipEngineErrors:
    def test_shipengine_error(self) -> None:
        with pytest.raises(ShipEngineError):
            shipengine_error()

    def test_shipengine_error_with_bad_error_type(self) -> None:
        with pytest.raises(ValueError):
            shipengine_error_with_bad_error_type()

    def test_shipengine_error_with_bad_error_source(self) -> None:
        with pytest.raises(ValueError):
            shipengine_error_with_bad_error_source()

    def test_shipengine_error_with_bad_error_code(self) -> None:
        with pytest.raises(ValueError):
            shipengine_error_with_bad_error_code()

    def test_account_status(self) -> None:
        with pytest.raises(AccountStatusError):
            account_status()

    def test_business_rule_error(self) -> None:
        with pytest.raises(BusinessRuleError):
            business_rule_error()

    def test_security_error(self) -> None:
        with pytest.raises(ClientSecurityError):
            security_error()

    def test_validation_error(self) -> None:
        with pytest.raises(ValidationError):
            validation_error()

    def test_timeout_error(self) -> None:
        with pytest.raises(ClientTimeoutError):
            client_timeout_error()

    def test_invalid_filed_value_error(self) -> None:
        with pytest.raises(InvalidFieldValueError):
            invalid_filed_value_error()

    def test_rate_limit_exceeded_error(self) -> None:
        with pytest.raises(RateLimitExceededError):
            rate_limit_exceeded_error()

    def test_error_defaults(self) -> None:
        """Test the error class default values."""
        with pytest.raises(ShipEngineError):
            shipengine_error_defaults()

    def test_to_dict_method(self) -> None:
        """Test the to_dict convenience method."""
        try:
            shipengine_error()
        except ShipEngineError as err:
            d = err.to_dict()
            assert type(d) is dict

    def test_to_json_method(self) -> None:
        """Test the to_json convenience method."""
        try:
            shipengine_error()
        except ShipEngineError as err:
            j = err.to_json()
            assert type(j) is str
