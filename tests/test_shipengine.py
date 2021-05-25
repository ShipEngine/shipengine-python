"""Testing the ShipEngine object."""
import pytest

from shipengine_sdk import __version__
from shipengine_sdk import ShipEngineConfig
from shipengine_sdk.errors import ValidationError
from shipengine_sdk.models import ErrorCode
from shipengine_sdk.models import ErrorSource
from shipengine_sdk.models import ErrorType


def shipengine_no_api_key():
    return ShipEngineConfig(dict(retries=2))


class TestShipEngine:
    def test_version(self) -> None:
        """Test the package version of the ShipEngine SDK."""
        assert __version__ == "0.0.1"

    def test_no_api_key_provided(self) -> None:
        """DX-1440 - No API Key at instantiation"""
        try:
            shipengine_no_api_key()
        except ValidationError as e:
            with pytest.raises(ValidationError):
                shipengine_no_api_key()
            assert type(e) is ValidationError
            assert e.request_id is None
            assert e.error_type is ErrorType.VALIDATION.value
            assert e.error_code is ErrorCode.FIELD_VALUE_REQUIRED.value
            assert e.source is ErrorSource.SHIPENGINE.value
            assert e.message == "A ShipEngine API key must be specified."
