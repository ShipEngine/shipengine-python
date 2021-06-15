"""Tests for the GetCarrierAccounts service in the ShipEngine SDK."""
from shipengine_sdk.errors import ClientSystemError
from shipengine_sdk.models import Carriers, ErrorCode, ErrorSource, ErrorType
from shipengine_sdk.services.get_carrier_accounts import GetCarrierAccounts

from ..util.test_helpers import stub_get_carrier_accounts


class TestGetCarrierAccounts:
    def test_no_accounts_setup(self) -> None:
        """DX-1075 - No accounts setup yet."""
        accounts = stub_get_carrier_accounts(carrier_code="sendle")

        assert type(accounts) is list
        assert len(accounts) == 0

    def test_multiple_accounts(self) -> None:
        """DX-1076 - Multiple carrier accounts."""
        accounts = stub_get_carrier_accounts()

        assert len(accounts) == 5
        assert accounts[0].carrier["code"] == Carriers.UPS.value
        assert accounts[1].carrier["code"] == Carriers.FEDEX.value
        assert accounts[2].carrier["code"] == Carriers.FEDEX.value
        assert accounts[3].carrier["code"] == Carriers.USPS.value
        assert accounts[4].carrier["code"] == Carriers.STAMPS_COM.value

        for account in accounts:
            assert account.account_id.startswith("car_")
            assert account.name is not None
            assert account.account_number is not None
            assert account.carrier is not None
            assert account.carrier["code"] is not None
            assert type(account.carrier["code"]) == str
            assert account.carrier["name"] is not None
            assert type(account.carrier["name"]) == str

    def test_multiple_accounts_of_same_carrier(self):
        """DX-1077 - Multiple accounts of the same carrier."""
        accounts = stub_get_carrier_accounts()

        assert len(accounts) == 5
        assert accounts[0].carrier["code"] == Carriers.UPS.value
        assert accounts[0].account_id != accounts[1].account_id
        assert accounts[1].carrier["code"] == Carriers.FEDEX.value
        assert accounts[2].carrier["code"] == Carriers.FEDEX.value
        assert accounts[3].carrier["code"] == Carriers.USPS.value
        assert accounts[4].carrier["code"] == Carriers.STAMPS_COM.value

        for account in accounts:
            assert account.account_id.startswith("car_")
            assert account.name is not None

    def test_server_side_error(self) -> None:
        """DX-1078 - Get carrier accounts server-side error."""
        try:
            stub_get_carrier_accounts("access_worldwide")
        except ClientSystemError as err:
            assert err.request_id is not None
            assert err.request_id.startswith("req_") is True
            assert err.source == ErrorSource.SHIPENGINE.value
            assert err.error_type == ErrorType.SYSTEM.value
            assert err.error_code == ErrorCode.UNSPECIFIED.value

    def test_get_cached_accounts_by_carrier(self) -> None:
        get_accounts = GetCarrierAccounts()
        stub_get_carrier_accounts()  # fill the cache
        accounts = get_accounts.get_cached_accounts_by_carrier_code(carrier_code="fedex")

        assert len(accounts) == 2
        assert accounts[0].carrier["code"] == "fedex"
        assert accounts[1].carrier["code"] == "fedex"
