"""
Fetch the carrier account connected to a given ShipEngine Account
based on the API Key passed into the ShipEngine SDK.
"""
from typing import List, Optional

from ..jsonrpc import rpc_request
from ..models import CarrierAccount, RPCMethods
from ..shipengine_config import ShipEngineConfig

cached_accounts: List = list()


class GetCarrierAccounts:
    @staticmethod
    def fetch_carrier_accounts(
        config: ShipEngineConfig, carrier_code: Optional[str] = None
    ) -> List[CarrierAccount]:
        global cached_accounts
        if carrier_code is not None:
            api_response = rpc_request(
                method=RPCMethods.LIST_CARRIERS.value,
                config=config,
                params={"carrierCode": carrier_code},
            )
        else:
            api_response = rpc_request(
                method=RPCMethods.LIST_CARRIERS.value,
                config=config,
            )

        accounts = api_response["result"]["carrierAccounts"]
        cached_accounts = list()
        for account in accounts:
            carrier_account = CarrierAccount(account)
            cached_accounts.append(carrier_account)

        return cached_accounts

    def fetch_cached_carrier_accounts(
        self, config: ShipEngineConfig, carrier_code: Optional[str]
    ) -> List[CarrierAccount]:
        global cached_accounts
        accounts = cached_accounts
        return (
            accounts
            if len(cached_accounts) > 0
            else self.fetch_carrier_accounts(config=config, carrier_code=carrier_code)
        )

    @staticmethod
    def get_cached_accounts_by_carrier_code(carrier_code: Optional[str]) -> List[CarrierAccount]:
        global cached_accounts
        accounts = list()
        if carrier_code is None:
            return cached_accounts
        else:
            for account in cached_accounts:
                if account.carrier["code"] == carrier_code:
                    accounts.append(account)
            return accounts
