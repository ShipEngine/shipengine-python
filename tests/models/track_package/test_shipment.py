"""Testing the Shipment class object."""
from typing import Any, Dict

import pytest

from shipengine_sdk.errors import ShipEngineError
from shipengine_sdk.models import Shipment
from shipengine_sdk.util.iso_string import IsoString

from ...util import stub_shipengine_config


def stub_valid_shipment_data() -> Dict[str, Any]:
    """
    Return a dictionary that mimics the Shipment data that would
    be returned by ShipEngine API.
    """
    return {
        "carrierCode": "fedex",
        "carrierAccountID": "car_kfUjTZSEAQ8gHeT",
        "shipmentID": "shp_yuh3GkfUjTZSEAQ",
        "estimatedDelivery": "2021-06-15T21:00:00.000Z",
    }


def stub_invalid_shipment_data() -> Dict[str, Any]:
    """
    Return a dictionary that mimics the Shipment data that would
    be returned by ShipEngine API, where the `carrierAccountID` is invalid.
    """
    return {
        "carrierCode": "fedex",
        "carrierAccountID": "car_kfUoSHIPENGINEQ8gHeT",
        "shipmentID": "shp_yuh3GkfUjTZSEAQ",
        "estimatedDelivery": "2021-06-15T21:00:00.000Z",
    }


def stub_invalid_account_id_shipment_instantiation() -> Shipment:
    """Return a test Shipment object that has an invalid `carrierAccountID`.."""
    return Shipment(
        shipment=stub_invalid_shipment_data(),
        actual_delivery_date=IsoString("2021-06-10T21:00:00.000"),
        config=stub_shipengine_config(),
    )


def stub_valid_shipment_instantiation() -> Shipment:
    """Return a valid test Shipment object."""
    return Shipment(
        shipment=stub_valid_shipment_data(),
        actual_delivery_date=IsoString("2021-06-10T21:00:00.000"),
        config=stub_shipengine_config(),
    )


class TestShipment:
    def test_get_carrier_account_failure_via_invalid_account_id(self) -> None:
        with pytest.raises(ShipEngineError):
            stub_invalid_account_id_shipment_instantiation()

    def test_shipment_to_dict(self) -> None:
        shipment = stub_valid_shipment_instantiation()
        assert type(shipment.to_dict()) is dict

    def test_shipment_to_json(self) -> None:
        shipment = stub_valid_shipment_instantiation()
        assert type(shipment.to_json()) is str
