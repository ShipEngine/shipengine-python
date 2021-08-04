"""Testing the ShipEngine object."""
import pytest

from shipengine import ShipEngine
from shipengine.errors import ValidationError
from shipengine.util import api_key_validation_error_assertions


def shipengine_empty_api_key():
    return ShipEngine("")


def shipengine_no_api_key():
    return ShipEngine({"retries": 3})


class TestShipEngine:
    def test_no_api_key_provided(self) -> None:
        """DX-1440 - No API Key at instantiation."""
        try:
            shipengine_no_api_key()
        except Exception as e:
            api_key_validation_error_assertions(e)
            with pytest.raises(ValidationError):
                shipengine_no_api_key()

    def test_empty_api_key_provided(self) -> None:
        """DX-1441 - Empty API Key at instantiation."""
        try:
            shipengine_empty_api_key()
        except Exception as e:
            api_key_validation_error_assertions(e)
            with pytest.raises(ValidationError):
                shipengine_empty_api_key()
