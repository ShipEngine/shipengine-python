"""Testing the `track_package` method of the ShipEngine SDK."""
from typing import List

from shipengine_sdk.errors import ClientSystemError, ShipEngineError, ValidationError
from shipengine_sdk.models import (
    ErrorCode,
    ErrorSource,
    ErrorType,
    TrackingEvent,
    TrackingQuery,
    TrackPackageResult,
)

from ..util import configurable_stub_shipengine_instance, stub_config


def assertions_on_delivered_after_exception_or_multiple_attempts(
    tracking_result: TrackPackageResult,
) -> None:
    track_package_assertions(tracking_result=tracking_result)
    does_delivery_date_match(tracking_result)
    assert_events_in_order(tracking_result.events)
    assert len(tracking_result.events) == 8
    assert tracking_result.events[0].status == "accepted"
    assert tracking_result.events[1].status == "in_transit"
    assert tracking_result.events[2].status == "in_transit"
    assert tracking_result.events[3].status == "exception"
    assert tracking_result.events[4].status == "exception"
    assert tracking_result.events[5].status == "attempted_delivery"
    assert tracking_result.events[6].status == "attempted_delivery"
    assert tracking_result.events[7].status == "delivered"
    assert tracking_result.events[-1].status == "delivered"


def does_delivery_date_match(tracking_result: TrackPackageResult) -> None:
    """Check that the delivery dates for a given tracking response match."""
    assert (
        tracking_result.shipment.actual_delivery_date.to_datetime_object()
        == tracking_result.events[-1].date_time.to_datetime_object()
    )


def assert_events_in_order(events: List) -> None:
    """
    Checks that the order of events is correct in that they should be ordered with
    the newest event at the bottom of the list.
    """
    previous_date_time = events[0].date_time
    for event in events:
        assert event.date_time.to_datetime_object() >= previous_date_time.to_datetime_object()
        previous_date_time = event.date_time


def track_package_assertions(tracking_result: TrackPackageResult) -> None:
    """Common `track_package` assertions."""
    carrier_account_carrier_code = tracking_result.shipment.carrier_account.carrier["code"]
    carrier_code = tracking_result.shipment.carrier["code"]
    estimated_delivery = tracking_result.shipment.estimated_delivery_date

    assert carrier_account_carrier_code is not None
    assert type(carrier_account_carrier_code) is str
    assert carrier_code is not None
    assert type(carrier_code) is str
    assert estimated_delivery.has_timezone() is True


def date_time_assertions(event: TrackingEvent) -> None:
    """Check that date_time has a timezone."""
    assert event.date_time is not None
    assert event.carrier_date_time is not None
    assert event.date_time.has_timezone() is True
    assert event.carrier_date_time.has_timezone() is False


class TestTrackPackage:
    _PACKAGE_ID_FEDEX_ACCEPTED: str = "pkg_1FedExAccepted"
    _PACKAGE_ID_FEDEX_DELIVERED: str = "pkg_1FedExDeLivered"
    _PACKAGE_ID_FEDEX_DELIVERED_EXCEPTION: str = "pkg_1FedexDeLiveredException"

    def test_track_by_tracking_number_and_carrier_code(self) -> None:
        """DX-1084 - Test track by tracking number and carrier code."""
        shipengine = configurable_stub_shipengine_instance(stub_config())
        tracking_data = TrackingQuery(carrier_code="fedex", tracking_number="abcFedExDelivered")
        tracking_result = shipengine.track_package(tracking_data=tracking_data)

        assert tracking_data.carrier_code == tracking_result.shipment.carrier["code"]
        assert tracking_data.tracking_number == tracking_result.package.tracking_number
        # assert tracking_result.package.tracking_url is not None
        # assert type(tracking_result.package.tracking_url) is str

    def test_track_by_package_id(self) -> None:
        """DX-1086 - Test track by package ID."""
        package_id = self._PACKAGE_ID_FEDEX_ACCEPTED
        shipengine = configurable_stub_shipengine_instance(stub_config())
        tracking_result = shipengine.track_package(tracking_data=package_id)

        assert tracking_result.package.package_id == package_id
        assert tracking_result.package.tracking_number is not None
        # assert tracking_result.package.tracking_url is not None
        assert tracking_result.shipment.shipment_id is not None
        assert tracking_result.shipment.account_id is not None

    def test_initial_scan_tracking_event(self) -> None:
        """DX-1088 - Test initial scan tracking event."""
        package_id = self._PACKAGE_ID_FEDEX_ACCEPTED
        shipengine = configurable_stub_shipengine_instance(stub_config())
        tracking_result = shipengine.track_package(tracking_data=package_id)

        track_package_assertions(tracking_result=tracking_result)
        assert len(tracking_result.events) == 1
        assert tracking_result.events[0].status == "accepted"

    def test_out_for_delivery_tracking_event(self) -> None:
        """DX-1089 - Test out for delivery tracking event."""
        package_id = "pkg_1FedExAttempted"
        shipengine = configurable_stub_shipengine_instance(stub_config())
        tracking_result = shipengine.track_package(tracking_data=package_id)

        track_package_assertions(tracking_result=tracking_result)
        assert len(tracking_result.events) == 5
        assert tracking_result.events[0].status == "accepted"
        assert tracking_result.events[1].status == "in_transit"

    def test_multiple_delivery_attempts(self) -> None:
        """DX-1090 - Test multiple delivery attempt events."""
        package_id = "pkg_1FedexDeLiveredAttempted"
        shipengine = configurable_stub_shipengine_instance(stub_config())
        tracking_result = shipengine.track_package(tracking_data=package_id)

        track_package_assertions(tracking_result=tracking_result)
        assert len(tracking_result.events) == 5
        assert_events_in_order(tracking_result.events)
        assert tracking_result.events[0].status == "accepted"
        assert tracking_result.events[1].status == "in_transit"
        assert tracking_result.events[2].status == "attempted_delivery"
        assert tracking_result.events[3].status == "attempted_delivery"
        assert tracking_result.events[4].status == "delivered"

    def test_delivered_on_first_try(self) -> None:
        """DX-1091 - Test delivered on first try tracking event."""
        package_id = self._PACKAGE_ID_FEDEX_DELIVERED
        shipengine = configurable_stub_shipengine_instance(stub_config())
        tracking_result = shipengine.track_package(tracking_data=package_id)

        track_package_assertions(tracking_result=tracking_result)
        assert (
            tracking_result.shipment.actual_delivery_date.to_datetime_object()
            == tracking_result.events[4].date_time.to_datetime_object()
        )
        does_delivery_date_match(tracking_result)
        assert_events_in_order(tracking_result.events)
        assert len(tracking_result.events) == 5
        assert tracking_result.events[0].status == "accepted"
        assert tracking_result.events[1].status == "in_transit"
        assert tracking_result.events[4].status == "delivered"
        assert tracking_result.events[-1].status == "delivered"

    def test_delivered_with_signature(self) -> None:
        """DX-1092 - Test track delivered with signature event."""
        package_id = self._PACKAGE_ID_FEDEX_DELIVERED
        shipengine = configurable_stub_shipengine_instance(stub_config())
        tracking_result = shipengine.track_package(tracking_data=package_id)

        track_package_assertions(tracking_result=tracking_result)
        does_delivery_date_match(tracking_result)
        assert_events_in_order(tracking_result.events)
        assert len(tracking_result.events) == 5
        assert tracking_result.events[0].status == "accepted"
        assert tracking_result.events[1].status == "in_transit"
        assert tracking_result.events[3].status == "in_transit"
        assert tracking_result.events[4].status == "delivered"
        assert tracking_result.events[-1].status == "delivered"
        assert tracking_result.events[-1].signer is not None
        assert type(tracking_result.events[-1].signer) is str

    def test_delivered_after_multiple_attempts(self) -> None:
        """DX-1093 - Test delivered after multiple attempts tracking event."""
        package_id = self._PACKAGE_ID_FEDEX_DELIVERED_EXCEPTION
        shipengine = configurable_stub_shipengine_instance(stub_config())
        tracking_result = shipengine.track_package(tracking_data=package_id)
        assertions_on_delivered_after_exception_or_multiple_attempts(tracking_result)

    def test_delivered_after_exception(self) -> None:
        """DX-1094 - Test delivered after exception tracking event."""
        package_id = self._PACKAGE_ID_FEDEX_DELIVERED_EXCEPTION
        shipengine = configurable_stub_shipengine_instance(stub_config())
        tracking_result = shipengine.track_package(tracking_data=package_id)
        assertions_on_delivered_after_exception_or_multiple_attempts(tracking_result)

    def test_single_exception_tracking_event(self) -> None:
        """DX-1095 - Test single exception tracking event."""
        package_id = "pkg_1FedexException"
        shipengine = configurable_stub_shipengine_instance(stub_config())
        tracking_result = shipengine.track_package(tracking_data=package_id)

        track_package_assertions(tracking_result=tracking_result)
        assert_events_in_order(tracking_result.events)
        assert len(tracking_result.events) == 3
        assert tracking_result.events[0].status == "accepted"
        assert tracking_result.events[1].status == "in_transit"
        assert tracking_result.events[2].status == "exception"

    def test_track_with_multiple_exceptions(self) -> None:
        """DX-1096 - Test track with multiple exceptions."""
        package_id = self._PACKAGE_ID_FEDEX_DELIVERED_EXCEPTION
        shipengine = configurable_stub_shipengine_instance(stub_config())
        tracking_result = shipengine.track_package(tracking_data=package_id)

        track_package_assertions(tracking_result=tracking_result)
        assert_events_in_order(tracking_result.events)
        assert len(tracking_result.events) == 8
        assert tracking_result.events[0].status == "accepted"
        assert tracking_result.events[4].status == "exception"
        assert tracking_result.events[5].status == "attempted_delivery"
        assert tracking_result.events[7].status == "delivered"
        assert tracking_result.events[-1].status == "delivered"

    def test_multiple_locations_in_tracking_event(self) -> None:
        """DX-1097 - Test track package with multiple locations in tracking event."""
        package_id = "pkg_Attempted"
        shipengine = configurable_stub_shipengine_instance(stub_config())
        tracking_result = shipengine.track_package(tracking_data=package_id)

        track_package_assertions(tracking_result=tracking_result)
        assert_events_in_order(tracking_result.events)
        assert tracking_result.events[0].location is None
        print(tracking_result.events[1].location)
        assert tracking_result.events[1].location.latitude is None
        assert tracking_result.events[1].location.longitude is None
        assert type(tracking_result.events[2].location.latitude) is float
        assert type(tracking_result.events[2].location.longitude) is float
        assert type(tracking_result.events[4].location.latitude) is float
        assert type(tracking_result.events[4].location.longitude) is float

    def test_carrier_date_time_without_timezone(self) -> None:
        """DX-1098 - Test track package where carrierDateTime has no timezone."""
        package_id = "pkg_Attempted"
        shipengine = configurable_stub_shipengine_instance(stub_config())
        tracking_result = shipengine.track_package(tracking_data=package_id)

        track_package_assertions(tracking_result=tracking_result)
        assert_events_in_order(tracking_result.events)
        assert len(tracking_result.events) == 5
        for event in tracking_result.events:
            date_time_assertions(event=event)

    def test_invalid_tracking_number(self) -> None:
        """DX-1099 - Test track package with an invalid tracking number."""
        tracking_data = TrackingQuery(carrier_code="fedex", tracking_number="abc123")
        shipengine = configurable_stub_shipengine_instance(stub_config())
        try:
            shipengine.track_package(tracking_data=tracking_data)
        except ShipEngineError as err:
            assert type(err) is ClientSystemError
            assert err.request_id is not None
            assert err.request_id.startswith("req_")
            assert err.source == ErrorSource.CARRIER.value
            assert err.error_type == ErrorType.BUSINESS_RULES.value
            assert err.error_code == ErrorCode.INVALID_IDENTIFIER.value
            assert (
                err.message
                == f"{tracking_data.tracking_number} is not a valid fedex tracking number."
            )

    def test_invalid_package_id_prefix(self) -> None:
        """DX-1100 - Test track package with invalid package_id prefix."""
        package_id = "car_1FedExAccepted"
        shipengine = configurable_stub_shipengine_instance(stub_config())
        try:
            shipengine.track_package(tracking_data=package_id)
        except ShipEngineError as err:
            assert type(err) is ValidationError
            assert err.request_id is None
            assert err.source is ErrorSource.SHIPENGINE.value
            assert err.error_type is ErrorType.VALIDATION.value
            assert err.error_code is ErrorCode.INVALID_IDENTIFIER.value
            assert err.message == f"[{package_id[0:4]}] is not a valid package ID prefix."

    def test_invalid_package_id(self) -> None:
        """DX-1101 - Test track package with invalid package_id."""
        package_id = "pkg_12!@3a s567"
        shipengine = configurable_stub_shipengine_instance(stub_config())
        try:
            shipengine.track_package(tracking_data=package_id)
        except ShipEngineError as err:
            assert type(err) is ValidationError
            assert err.request_id is None
            assert err.source is ErrorSource.SHIPENGINE.value
            assert err.error_type is ErrorType.VALIDATION.value
            assert err.error_code is ErrorCode.INVALID_IDENTIFIER.value
            assert err.message == f"[{package_id}] is not a valid package ID."

    def test_package_id_not_found(self) -> None:
        """DX-1102 - Test track package where package ID cannot be found."""
        package_id = "pkg_123"
        shipengine = configurable_stub_shipengine_instance(stub_config())
        try:
            shipengine.track_package(tracking_data=package_id)
        except ShipEngineError as err:
            assert type(err) is ClientSystemError
            assert err.request_id is not None
            assert err.request_id.startswith("req_")
            assert err.source == ErrorSource.SHIPENGINE.value
            assert err.error_type == ErrorType.VALIDATION.value
            assert err.error_code == ErrorCode.INVALID_IDENTIFIER.value
            assert err.message == f"Package ID {package_id} does not exist."

    def test_server_side_error(self) -> None:
        """DX-1103 - Test track package server-side error."""
        tracking_data = TrackingQuery(carrier_code="fedex", tracking_number="500 Server Error")
        shipengine = configurable_stub_shipengine_instance(stub_config())
        try:
            shipengine.track_package(tracking_data=tracking_data)
        except ShipEngineError as err:
            assert type(err) is ClientSystemError
            assert err.request_id is not None
            assert err.request_id.startswith("req_")
            assert err.source == ErrorSource.SHIPENGINE.value
            assert err.error_type == ErrorType.SYSTEM.value
            assert err.error_code == ErrorCode.UNSPECIFIED.value
            assert err.message == "Unable to process this request. A downstream API error occurred."
