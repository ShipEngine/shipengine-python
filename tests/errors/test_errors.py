"""Tests for the ShipEngine SDK Errors"""
import pytest

from shipengine_sdk.errors import AccountStatusError
from shipengine_sdk.errors import BusinessRuleError
from shipengine_sdk.errors import ClientSecurityError
from shipengine_sdk.errors import ClientTimeoutError
from shipengine_sdk.errors import InvalidFieldValueError
from shipengine_sdk.errors import RateLimitExceededError
from shipengine_sdk.errors import ShipEngineError
from shipengine_sdk.errors import ValidationError


def shipengine_error():
    raise ShipEngineError(
        request_id="req_a523b1b19bd54054b7eb953f000e7f15",
        message="The is a test exception",
        source="shipengine",
        error_type="validation",
        error_code="invalid_address",
    )


def account_status():
    raise AccountStatusError("There was an issue with your ShipEngine account.")


def business_rule_error():
    raise BusinessRuleError("Invalid postal code.")


def security_error():
    raise ClientSecurityError("Unauthorized - you API key is invalid.")


def validation_error():
    raise ValidationError("The value provided must be an integer - object provided.")


def client_timeout_error():
    raise ClientTimeoutError(300, "shipengine", "req_a523b1b19bd54054b7eb953f000e7f15")


def invalid_filed_value_error():
    raise InvalidFieldValueError("is_residential", "Value should be int but got str.", 1)


def rate_limit_exceeded_error():
    raise RateLimitExceededError(300, "shipengine", "req_a523b1b19bd54054b7eb953f000e7f15")


def test_shipengine_error():
    with pytest.raises(ShipEngineError):
        shipengine_error()


def test_account_status():
    with pytest.raises(AccountStatusError):
        account_status()


def test_business_rule_error():
    with pytest.raises(BusinessRuleError):
        business_rule_error()


def test_security_error():
    with pytest.raises(ClientSecurityError):
        security_error()


def test_validation_error():
    with pytest.raises(ValidationError):
        validation_error()


def test_timeout_error():
    with pytest.raises(ClientTimeoutError):
        client_timeout_error()


def test_invalid_filed_value_error():
    with pytest.raises(InvalidFieldValueError):
        invalid_filed_value_error()


def test_rate_limit_exceeded_error():
    with pytest.raises(RateLimitExceededError):
        rate_limit_exceeded_error()
