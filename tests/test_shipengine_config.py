"""Testing the ShipEngineConfig object."""
import pytest

from shipengine_sdk import ShipEngineConfig
from shipengine_sdk.errors import ValidationError
from shipengine_sdk.models import ErrorCode
from shipengine_sdk.models import ErrorSource
from shipengine_sdk.models import ErrorType
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


class TestShipEngineConfig:
    def test_no_api_key_provided(self):
        """DX-1440 - No API Key at instantiation"""
        try:
            config_with_no_api_key()
        except ValidationError as e:
            with pytest.raises(ValidationError):
                config_with_no_api_key()
            assert type(e) is ValidationError
            assert e.request_id is None
            assert e.error_type is ErrorType.VALIDATION.value
            assert e.error_code is ErrorCode.FIELD_VALUE_REQUIRED.value
            assert e.source is ErrorSource.SHIPENGINE.value
            assert e.message == "A ShipEngine API key must be specified."

    def test_empty_api_key_provided(self):
        """DX-1441 - Empty API Key at instantiation."""
        try:
            config_with_empty_api_key()
        except ValidationError as e:
            api_key_validation_error_assertions(e)
            with pytest.raises(ValidationError):
                config_with_empty_api_key()
