"""Testing the `track_package` method of the ShipEngine SDK."""

# class TestTrackPackage:
#     def test_track_by_tracking_number_and_carrier_code(self) -> None:
#         """DX-1084 - Test track by tracking number and carrier code."""
#         shipengine = configurable_stub_shipengine_instance(stub_config())
#         tracking_data = TrackingQuery(
#                 carrier_code="fedex",
#                 tracking_number="abcFedExDelivered"
#         )
#         tracking_result = shipengine.track_package(tracking_data=tracking_data)
#
#         assert tracking_data.carrier_code == tracking_result.shipment.carrier.code
