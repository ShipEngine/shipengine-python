"""Testing the ShipEngineConfig object."""
import pytest

from shipengine_sdk import ShipEngineConfig
from shipengine_sdk.errors import ValidationError
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
    def test_no_api_key_provided(self) -> None:
        """DX-1440 - No API Key at instantiation"""
        try:
            config_with_no_api_key()
        except ValidationError as e:
            api_key_validation_error_assertions(e)
            with pytest.raises(ValidationError):
                config_with_no_api_key()

    def test_empty_api_key_provided(self) -> None:
        """DX-1441 - Empty API Key at instantiation."""
        try:
            config_with_empty_api_key()
        except ValidationError as e:
            api_key_validation_error_assertions(e)
            with pytest.raises(ValidationError):
                config_with_empty_api_key()
