"""Test the CarrierAccount class object."""
from typing import Any, Dict

from shipengine_sdk.errors import InvalidFieldValueError
from shipengine_sdk.models import CarrierAccount


def stub_carrier_account_object() -> Dict[str, Any]:
    """
    Return a dictionary that mimics the data this object would be passed
    from the returned ShipEngine API response.
    """
    return {
        "accountID": "car_1knseddGBrseWTiw",
        "accountNumber": "1169350",
        "carrierCode": "royal_mail",
        "name": "United Parcel Service",
    }


class TestCarrierAccount:
    def test_carrier_account_with_invalid_carrier(self) -> None:
        k = stub_carrier_account_object()
        try:
            CarrierAccount(account_information=k)
        except InvalidFieldValueError as err:
            assert err.message == f"Carrier [{k['carrierCode']}] is currently not supported."

    def test_carrier_account_to_dict(self) -> None:
        k = stub_carrier_account_object()
        carrier_account = CarrierAccount(account_information=k)

        assert type(carrier_account.to_dict()) is dict

    def test_carrier_account_to_json(self) -> None:
        k = stub_carrier_account_object()
        carrier_account = CarrierAccount(account_information=k)

        assert type(carrier_account.to_json()) is str
