"""Testing the ShipEngineConfig object."""
import pytest

from shipengine_sdk import ShipEngineConfig
from shipengine_sdk.errors import ValidationError
from shipengine_sdk.models import ErrorCode
from shipengine_sdk.models import ErrorSource
from shipengine_sdk.models import ErrorType


def config_with_no_api_key():
    return ShipEngineConfig(dict(retries=2))


class TestShipEngineConfig:
    def test_no_api_key(self):
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
