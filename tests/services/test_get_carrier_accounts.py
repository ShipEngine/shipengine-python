"""Tests for the GetCarrierAccounts service in the ShipEngine SDK."""
from shipengine_sdk.models import Carriers

from ..util.test_helpers import stub_get_carrier_accounts


class TestGetCarrierAccounts:
    def test_multiple_accounts_of_same_carrier(self):
        """DX-1077 - Multiple accounts of the same carrier."""
        accounts = stub_get_carrier_accounts()

        assert len(accounts) == 5
        assert accounts[0]["carrier"]["code"] == Carriers.UPS.value
        assert accounts[0]["account_id"] != accounts[1]["account_id"]
        assert accounts[1]["carrier"]["code"] == Carriers.FEDEX.value
        assert accounts[2]["carrier"]["code"] == Carriers.FEDEX.value
        assert accounts[3]["carrier"]["code"] == Carriers.USPS.value
        assert accounts[4]["carrier"]["code"] == Carriers.STAMPS_COM.value

        for account in accounts:
            assert account["account_id"].startswith("car_")
            assert account["name"] is not None
