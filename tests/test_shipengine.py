"""Testing the ShipEngine object."""
import pytest

from shipengine_sdk import __version__
from shipengine_sdk import ShipEngine
from shipengine_sdk.errors import ValidationError
from shipengine_sdk.util.sdk_assertions import api_key_validation_error_assertions


def shipengine_no_api_key():
    """Return an error from no API Key."""
    return ShipEngine(dict(retries=2))


def shipengine_empty_api_key():
    """Return an error from empty API Key."""
    return ShipEngine(config="")


def shipengine_whitespace_in_api_key():
    """Return an error from whitespace in API Key."""
    return ShipEngine(config=" ")


class TestShipEngine:
    def test_version(self) -> None:
        """Test the package version of the ShipEngine SDK."""
        assert __version__ == "0.0.1"

    def test_no_api_key_provided(self) -> None:
        """DX-1440 - No API Key at instantiation."""
        try:
            shipengine_no_api_key()
        except ValidationError as e:
            with pytest.raises(ValidationError):
                shipengine_no_api_key()
            api_key_validation_error_assertions(e)

    def test_empty_api_key_provided(self):
        """DX-1441 - Empty API Key at instantiation."""
        try:
            shipengine_empty_api_key()
        except ValidationError as e:
            with pytest.raises(ValidationError):
                shipengine_empty_api_key()
            api_key_validation_error_assertions(e)
