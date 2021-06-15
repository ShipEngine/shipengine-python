"""Testing the TrackingEvent class object."""
from typing import Any, Dict

from shipengine_sdk.models import TrackingEvent


def stub_event_data() -> Dict[str, Any]:
    """Return a dictionary that mimics a tracking event object in a response from ShipEngine API."""
    return {
        "timestamp": "2021-06-13T13:00:00.000Z",
        "carrierTimestamp": "2021-06-13T19:00:00",
        "status": "accepted",
        "description": "Dropped-off at shipping center",
        "carrierStatusCode": "ACPT-2",
    }


def stub_tracking_event() -> TrackingEvent:
    """Return a valid stub TrackingEvent object."""
    return TrackingEvent(stub_event_data())


class TestTrackingEvent:
    def test_tracking_event_to_dict(self) -> None:
        tracking_event = stub_tracking_event()
        assert type(tracking_event.to_dict()) is dict

    def test_tracking_event_to_json(self) -> None:
        tracking_event = stub_tracking_event()
        assert type(tracking_event.to_json()) is str
