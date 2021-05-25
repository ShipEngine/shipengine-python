"""Testing the ShipEngineConfig object."""
import pytest

from shipengine_sdk import ShipEngineConfig
from shipengine_sdk.errors import InvalidFieldValueError, ValidationError
from shipengine_sdk.models import ErrorCode, ErrorSource, ErrorType
from shipengine_sdk.util import api_key_validation_error_assertions


def config_with_no_api_key():
    """Return an error from no API Key."""
    return ShipEngineConfig(dict(retries=2))


def config_with_empty_api_key():
    """Return an error from empty API Key."""
    return ShipEngineConfig(dict(api_key=""))


def config_with_whitespace_in_api_key():
    """Return an error from whitespace in API Key."""
    return ShipEngineConfig(dict(api_key=" "))


def config_with_invalid_retries():
    """Return an error from an invalid retry value being passed in"""
    return ShipEngineConfig(dict(api_key="baz", retries=-3))


class TestShipEngineConfig:
    def test_no_api_key_provided(self) -> None:
        """DX-1440 - No API Key at instantiation"""
        try:
            config_with_no_api_key()
        except Exception as e:
            api_key_validation_error_assertions(e)
            with pytest.raises(ValidationError):
                config_with_no_api_key()

    def test_empty_api_key_provided(self) -> None:
        """DX-1441 - Empty API Key at instantiation."""
        try:
            config_with_empty_api_key()
        except Exception as e:
            api_key_validation_error_assertions(e)
            with pytest.raises(ValidationError):
                config_with_empty_api_key()

    def test_invalid_retries_provided(self):
        """DX-1442 - Invalid retries at instantiation."""
        try:
            config_with_invalid_retries()
        except InvalidFieldValueError as e:
            assert type(e) is InvalidFieldValueError
            assert e.request_id is None
            assert e.error_type is ErrorType.VALIDATION.value
            assert e.error_code is ErrorCode.INVALID_FIELD_VALUE.value
            assert e.source is ErrorSource.SHIPENGINE.value
            assert e.message == "retries - Retries must be zero or greater."
            with pytest.raises(InvalidFieldValueError):
                config_with_invalid_retries()
