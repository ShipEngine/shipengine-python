"""Data objects to be used in the `track_package` and `track` methods."""
import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from dataclasses_json import LetterCase, dataclass_json  # type: ignore

from ...errors import ShipEngineError
from ...services.get_carrier_accounts import GetCarrierAccounts
from ...shipengine_config import ShipEngineConfig
from ...util.iso_string import IsoString
from .. import Carrier, CarrierAccount


class Shipment:
    config: ShipEngineConfig
    shipment_id: Optional[str] = None
    account_id: Optional[str] = None
    carrier_account: Optional[CarrierAccount] = None
    carrier: Carrier
    estimated_delivery_date: Union[IsoString, str]
    actual_delivery_date: Union[IsoString, str]

    def __init__(
        self, shipment: Dict[str, Any], actual_delivery_date: IsoString, config: ShipEngineConfig
    ) -> None:
        """This object represents a given Shipment."""
        self.config = config
        self.shipment_id = shipment["shipmentID"] if "shipmentID" in shipment else None
        self.account_id = shipment["carrierAccountID"] if "carrierAccountID" in shipment else None

        if self.account_id is not None:
            self.carrier_account = self._get_carrier_account(
                carrier=shipment["carrierCode"], account_id=self.account_id
            )

        if self.carrier_account is not None:
            self.carrier = self.carrier_account.carrier
        else:
            self.carrier = (
                Carrier(shipment["carrierCode"])
                if "carrierCode" in shipment
                else ShipEngineError("The carrierCode field was null from api response.")
            )

        self.estimated_delivery_date = IsoString(iso_string=shipment["estimatedDelivery"])
        self.actual_delivery_date = actual_delivery_date

    def _get_carrier_account(self, carrier: str, account_id: str) -> CarrierAccount:
        get_accounts: GetCarrierAccounts = GetCarrierAccounts()
        target_carrier: List[CarrierAccount] = list()
        carrier_accounts: List[CarrierAccount] = get_accounts.fetch_cached_carrier_accounts(
            carrier_code=carrier, config=self.config
        )

        for account in carrier_accounts:
            if account_id == account.account_id:
                target_carrier.append(account)
                return target_carrier[0]
            else:
                raise ShipEngineError(
                    message=f"accountID [{account_id}] doesn't match any of the accounts connected to your ShipEngine Account."  # noqa
                )

    def to_dict(self) -> Dict[str, Any]:
        if hasattr(self, "config"):
            del self.config
        else:
            pass  # noqa
        return (lambda o: o.__dict__)(self)

    def to_json(self) -> str:
        if hasattr(self, "config"):
            del self.config
        else:
            pass  # noqa
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)


class Package:
    """This object contains package information for a given shipment."""

    package_id: Optional[str]
    weight: Optional[Dict[str, Any]]
    dimensions: Optional[Dict[str, Any]]
    tracking_number: Optional[str]
    tracking_url: Optional[str]

    def __init__(self, package: Dict[str, Any]) -> None:
        self.package_id = package["packageID"] if "packageID" in package else None
        self.weight = package["weight"] if "weight" in package else None
        self.dimensions = package["dimensions"] if "dimensions" in package else None
        self.tracking_number = package["trackingNumber"] if "trackingNumber" in package else None
        self.tracking_url = package["trackingURL"] if "trackingURL" in package else None

    def to_dict(self) -> Dict[str, Any]:
        return (lambda o: o.__dict__)(self)

    def to_json(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TrackingQuery:
    """This object is used as an argument in the `track_package` and `track` methods."""

    carrier_code: str
    tracking_number: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Location:
    city_locality: Optional[str] = None
    state_province: Optional[str] = None
    postal_code: Optional[str] = None
    country_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class TrackingEvent:
    date_time: Union[IsoString, str]
    carrier_date_time: Union[IsoString, str]
    status: str
    description: Optional[str]
    carrier_status_code: Optional[str]
    carrier_detail_code: Optional[str]
    signer: Optional[str]
    location: Optional[Location]

    def __init__(self, event: Dict[str, Any]) -> None:
        """Tracking event object."""
        self.date_time = IsoString(iso_string=event["timestamp"])

        self.carrier_date_time = IsoString(iso_string=event["carrierTimestamp"])

        self.status = event["status"]
        self.description = event["description"] if "description" in event else None
        self.carrier_status_code = (
            event["carrierStatusCode"] if "carrierStatusCode" in event else None
        )
        self.signer = event["signer"] if "signer" in event else None
        self.location = Location.from_dict(event["location"]) if "location" in event else None

    def to_dict(self):
        return (lambda o: o.__dict__)(self)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)


class TrackPackageResult:
    shipment: Optional[Shipment]
    package: Optional[Package]
    events: Optional[List[TrackingEvent]] = list()

    def __init__(self, api_response: Dict[str, Any], config: ShipEngineConfig) -> None:
        """This object is used as the return type for the `track_package` and `track` methods."""
        self.events = list()
        result = api_response["result"]
        for event in result["events"]:
            self.events.append(TrackingEvent(event=event))

        self.shipment = (
            Shipment(
                shipment=result["shipment"],
                actual_delivery_date=self.get_latest_event().date_time,
                config=config,
            )
            if "shipment" in result
            else None
        )
        self.package = Package(result["package"]) if "package" in result else None

    def get_errors(self) -> List[TrackingEvent]:  # TODO: debug
        """Returns **only** the EXCEPTION events."""
        errors: List[TrackingEvent] = list()
        for event in self.events:
            if event.status == "EXCEPTION":
                errors.append(event)
        return errors

    def get_latest_event(self) -> TrackingEvent:  # TODO: debug
        """Returns the latest event to have occurred in the `events` list."""
        return self.events[-1]

    def has_errors(self) -> bool:  # TODO: debug
        """Returns `true` if there are any EXCEPTION events."""
        for event in self.events:
            return event.status == "EXCEPTION"

    def to_dict(self):
        if hasattr(self.shipment, "config"):
            del self.shipment.config
        else:
            pass  # noqa
        return (lambda o: o.__dict__)(self)

    def to_json(self):
        if hasattr(self.shipment, "config"):
            del self.shipment.config
        else:
            pass  # noqa
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)
