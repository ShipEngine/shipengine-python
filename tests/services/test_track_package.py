"""Testing the `track_package` method of the ShipEngine SDK."""
from shipengine_sdk.models import TrackingQuery
from tests.util.test_helpers import configurable_stub_shipengine_instance, stub_config


class TestTrackPackage:
    def test_track_by_tracking_number_and_carrier_code(self) -> None:
        """DX-1084 - Test track by tracking number and carrier code."""
        shipengine = configurable_stub_shipengine_instance(stub_config())
        tracking_data = TrackingQuery(carrier_code="fedex", tracking_number="abcFedExDelivered")
        tracking_result = shipengine.track_package(tracking_data=tracking_data)

        assert tracking_data.carrier_code == tracking_result.shipment.carrier.code
        assert tracking_data.tracking_number == tracking_result.package.tracking_number
        assert tracking_result.package.tracking_url is not None
        assert type(tracking_result.package.tracking_url) is str
