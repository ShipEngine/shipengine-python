"""
Fetch the carrier account connected to a given ShipEngine Account
based on the API Key passed into the ShipEngine SDK.
"""
from typing import List, Optional

from .. import ShipEngineConfig
from ..jsonrpc import rpc_request
from ..models import CarrierAccount, RPCMethods


class GetCarrierAccounts:
    cached_accounts: List = list()

    def fetch_carrier_accounts(
        self, config: ShipEngineConfig, carrier_code: Optional[str] = None
    ) -> List[CarrierAccount]:
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
        self.cached_accounts = list()
        for account in accounts:
            carrier_account = CarrierAccount(account)
            self.cached_accounts.append(carrier_account)

        return self.cached_accounts

    def fetch_cached_carrier_accounts(
        self, config: ShipEngineConfig, carrier_code: Optional[str]
    ) -> List[CarrierAccount]:
        accounts = self.cached_accounts
        return (
            accounts
            if len(self.cached_accounts) > 0
            else self.fetch_carrier_accounts(config=config, carrier_code=carrier_code)
        )

    def get_cached_accounts_by_carrier_code(self, carrier_code: Optional[str]):
        accounts = list()
        if carrier_code is not None:
            return self.cached_accounts
        else:
            for account in self.cached_accounts:
                if account.carrier.code == carrier_code:
                    accounts.append(account)
            return accounts
