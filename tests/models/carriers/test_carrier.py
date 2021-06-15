"""Test the Carrier class object."""
from shipengine_sdk.errors import ShipEngineError
from shipengine_sdk.models import Carrier


class TestCarrier:
    def test_invalid_carrier(self) -> None:
        try:
            Carrier(code="royal_mail")
        except ShipEngineError as err:
            assert err.message == "Carrier [royal_mail] not currently supported."

    def test_to_json(self) -> None:
        carrier = Carrier(code="fedex")
        assert type(carrier.to_json()) is str
