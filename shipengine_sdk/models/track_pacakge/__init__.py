"""Data objects to be used in the `track_package` and `track` methods."""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

from dataclasses_json import LetterCase, dataclass_json

from ...errors import ShipEngineError
from ...services.get_carrier_accounts import GetCarrierAccounts
from ...shipengine_config import ShipEngineConfig
from ...util.iso_string import IsoString
from .. import Carrier, CarrierAccount


class Shipment:
    config: ShipEngineConfig
    shipment_id: Optional[str]
    account_id: Optional[str]
    carrier_account: Optional[CarrierAccount]
    carrier: Carrier
    estimated_delivery_date: datetime
    actual_delivery_date: datetime

    def __init__(
        self, shipment: Dict[str, any], actual_delivery_date: datetime, config: ShipEngineConfig
    ) -> None:
        """This object represents a given Shipment."""
        self.config = config
        self.shipment_id = shipment["shipmentID"] if "shipmentID" in shipment else None
        self.account_id = shipment["carrierAccountID"] if "carrierAccountID" in shipment else None
        self.carrier_account = (
            self._get_carrier_account(carrier=shipment["carrierCode"], account_id=self.account_id)
            if "carrierCode" in shipment
            else None
        )

        if self.carrier_account is not None:
            self.carrier = self.carrier_account.carrier
        else:
            self.carrier = (
                Carrier(shipment["carrierCode"])
                if "carrierCode" in shipment
                else ShipEngineError("The carrierCode field was null from api response.")
            )

        self.estimated_delivery_date = IsoString(
            iso_string=shipment["estimatedDelivery"]
        ).to_datetime_object()
        self.actual_delivery_date = actual_delivery_date

    def _get_carrier_account(self, carrier: str, account_id: str) -> CarrierAccount:
        get_accounts = GetCarrierAccounts()
        target_carrier = list()
        carrier_accounts = get_accounts.fetch_cached_carrier_accounts(
            carrier_code=carrier, config=self.config
        )

        for account in carrier_accounts:
            if account_id == account["account_id"]:
                target_carrier.append(account)
                return target_carrier[0]
            else:
                raise ShipEngineError(
                    message=f"accountID [{account_id}] doesn't amtch any of the accounts connected to your "
                    + "ShipEngine Account."
                )


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Package:
    """This object contains package information for a given shipment."""

    package_id: Optional[str]
    weight: Optional[Dict[str, any]]
    dimensions: Optional[Dict[str, any]]
    tracking_number: Optional[str]
    tracking_url: Optional[str]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TrackingQuery:
    """This object is used as an argument in the `track_package` and `track` methods."""

    carrier_code: str
    tracking_number: str


@dataclass
class TrackPackageResult:
    shipment: Optional[Shipment]
    package: Optional[Package]
    events: Optional[List[str]]
