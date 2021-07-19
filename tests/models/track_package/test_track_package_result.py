"""Testing the TrackPackageResult class object."""
from typing import Any, Dict

from shipengine_sdk.models import TrackingEvent, TrackPackageResult
from shipengine_sdk.models.enums import Constants

from ...util import stub_shipengine_config


def stub_track_package_data() -> Dict[str, Any]:
    """
    Return a dictionary that mimics the track_package response
    from ShipEngine API.
    """
    return {
        "jsonrpc": "2.0",
        "id": "req_1de9ca85b8544c1c91cd17abc43cbb5e",
        "result": {
            "shipment": {
                "carrierCode": "fedex",
                "carrierAccountId": Constants.CARRIER_ACCOUNT_ID_STUB.value,
                "shipmentId": "shp_tJUaQJz3Twz57iL",
                "estimatedDelivery": "2021-06-15T21:00:00.000Z",
            },
            "package": {
                "packageId": "pkg_1FedexDeLiveredException",
                "trackingNumber": "2A4g3tJUaQJz3Twz57iLWBciD7wZWH",
                "trackingUrl": "https://www.fedex.com/track/2A4g3tJUaQJz3Twz57iLWBciD7wZWH",
                "weight": {"value": 76, "unit": "kilogram"},
                "dimensions": {"length": 36, "width": 36, "height": 23, "unit": "inch"},
            },
            "events": [
                {
                    "timestamp": "2021-06-10T19:00:00.000Z",
                    "carrierTimestamp": "2021-06-11T01:00:00",
                    "status": "accepted",
                    "description": "Dropped-off at shipping center",
                    "carrierStatusCode": "ACPT-2",
                    "carrierDetailCode": "PU7W",
                },
                {
                    "timestamp": "2021-06-11T01:00:00.000Z",
                    "carrierTimestamp": "2021-06-11T07:00:00",
                    "status": "in_transit",
                    "description": "En-route to distribution center hub",
                    "carrierStatusCode": "ER00P",
                },
                {
                    "timestamp": "2021-06-11T20:00:00.000Z",
                    "carrierTimestamp": "2021-06-12T02:00:00",
                    "status": "unknown",
                    "description": "Mechanically sorted",
                    "carrierStatusCode": "MMSa",
                    "carrierDetailCode": "00004134918400045",
                },
                {
                    "timestamp": "2021-06-12T10:00:00.000Z",
                    "carrierTimestamp": "2021-06-12T16:00:00",
                    "status": "in_transit",
                    "description": "On vehicle for delivery",
                    "carrierStatusCode": "OFD-22",
                    "carrierDetailCode": "91R-159E",
                },
                {
                    "timestamp": "2021-06-12T17:00:00.000Z",
                    "carrierTimestamp": "2021-06-12T23:00:00",
                    "status": "exception",
                    "description": "Weather delay",
                    "carrierStatusCode": "EX026",
                    "carrierDetailCode": "XX00016",
                    "location": {
                        "cityLocality": "Pittsburgh",
                        "stateProvince": "PA",
                        "postalCode": "15218",
                        "countryCode": "US",
                    },
                },
                {
                    "timestamp": "2021-06-13T02:00:00.000Z",
                    "carrierTimestamp": "2021-06-13T08:00:00",
                    "status": "exception",
                    "description": "Equipment failure",
                    "carrierStatusCode": "EX038",
                    "carrierDetailCode": "XX00184",
                    "location": {
                        "cityLocality": "Pittsburgh",
                        "stateProvince": "PA",
                        "postalCode": "15218",
                        "countryCode": "US",
                    },
                },
                {
                    "timestamp": "2021-06-13T10:00:00.000Z",
                    "carrierTimestamp": "2021-06-13T16:00:00",
                    "status": "in_transit",
                    "description": "On vehicle for delivery",
                    "carrierStatusCode": "OFD-22",
                    "carrierDetailCode": "91R-159E",
                },
                {
                    "timestamp": "2021-06-13T20:00:00.000Z",
                    "carrierTimestamp": "2021-06-14T02:00:00",
                    "status": "delivered",
                    "description": "Delivered",
                    "carrierStatusCode": "DV99-0004",
                    "signer": "John P. Doe",
                    "location": {
                        "cityLocality": "Pittsburgh",
                        "stateProvince": "PA",
                        "postalCode": "15218",
                        "countryCode": "US",
                        "coordinates": {"latitude": 40.4504687, "longitude": -79.9352761},
                    },
                },
            ],
        },
    }


def stub_track_package_result() -> TrackPackageResult:
    """Return a valid stub TrackPackageResult object."""
    return TrackPackageResult(
        api_response=stub_track_package_data(), config=stub_shipengine_config()
    )


class TestTrackPackageResult:
    def test_get_errors(self) -> None:
        result = stub_track_package_result()
        err = result.get_errors()
        assert type(err) is list
        assert len(err) == 2

    def test_has_errors(self) -> None:
        result = stub_track_package_result()
        assert result.has_errors() is True

    def test_get_latest_event(self) -> None:
        result = stub_track_package_result()
        assert type(result.get_latest_event()) is TrackingEvent

    def test_track_package_result_to_dict(self) -> None:
        result = stub_track_package_result()
        assert type(result.to_dict()) is dict

    def test_track_package_result_to_json(self) -> None:
        result = stub_track_package_result()
        assert type(result.to_json()) is str
