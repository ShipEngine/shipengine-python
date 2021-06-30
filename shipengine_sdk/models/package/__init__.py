"""Data objects to be used in the `track_package` and `track` methods."""
import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from dataclasses_json import LetterCase, dataclass_json

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
        self.shipment_id = shipment["shipmentId"] if "shipmentId" in shipment else None
        self.account_id = shipment["carrierAccountId"] if "carrierAccountId" in shipment else None

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

        raise ShipEngineError(
            message=f"accountId [{account_id}] doesn't match any of the accounts connected to your ShipEngine Account."  # noqa
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

    def __repr__(self):
        return f"Shipment({self.shipment_id}, {self.account_id}, {self.carrier_account}, {self.carrier}, {self.estimated_delivery_date}, {self.actual_delivery_date})"  # noqa


class Package:
    """This object contains package information for a given shipment."""

    package_id: Optional[str]
    weight: Optional[Dict[str, Any]]
    dimensions: Optional[Dict[str, Any]]
    tracking_number: Optional[str]
    tracking_url: Optional[str]

    def __init__(self, package: Dict[str, Any]) -> None:
        self.package_id = package["packageId"] if "packageId" in package else None
        self.weight = package["weight"] if "weight" in package else None
        self.dimensions = package["dimensions"] if "dimensions" in package else None
        self.tracking_number = package["trackingNumber"] if "trackingNumber" in package else None
        self.tracking_url = package["trackingUrl"] if "trackingUrl" in package else None

    def to_dict(self) -> Dict[str, Any]:
        return (lambda o: o.__dict__)(self)

    def to_json(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

    def __repr__(self):
        return f"Package({self.package_id}, {self.weight}, {self.dimensions}, {self.tracking_number}, {self.tracking_url})"  # noqa


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TrackingQuery:
    """This object is used as an argument in the `track_package` and `track` methods."""

    carrier_code: str
    tracking_number: str


class Location:
    city_locality: Optional[str]
    state_province: Optional[str]
    postal_code: Optional[str]
    country_code: Optional[str]
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    def __init__(self, location_data: Dict[str, Any]) -> None:
        self.city_locality = (
            location_data["cityLocality"] if "cityLocality" in location_data and location_data != None else None
        )
        self.state_province = (
            location_data["stateProvince"] if "stateProvince" in location_data and location_data != None else None
        )
        self.postal_code = location_data["postalCode"] if "postalCode" in location_data and location_data != None else None
        self.country_code = location_data["countryCode"] if "countryCode" in location_data and location_data != None else None

        if "coordinates" in location_data and location_data != None and location_data["coordinates"] != None:
            self.latitude = location_data["coordinates"]["latitude"]
            self.longitude = location_data["coordinates"]["longitude"]

    def to_dict(self):
        return (lambda o: o.__dict__)(self)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

    def __repr__(self):
        return f"Location({self.city_locality}, {self.state_province}, {self.postal_code}, {self.country_code}, {self.latitude}, {self.longitude})"  # noqa


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
        self.location = Location(event["location"]) if "location" in event and event["location"] != None else None

    def to_dict(self):
        return (lambda o: o.__dict__)(self)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

    def __repr__(self):
        return f"TrackingEvent({self.date_time.to_string()}, {self.date_time.to_string()}, {self.status}, {self.description}, {self.carrier_status_code}, {self.carrier_detail_code}, {self.signer}, {self.location})"  # noqa


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

    def get_errors(self) -> List[TrackingEvent]:
        """Returns **only** the exception events."""
        errors: List[TrackingEvent] = list()
        for event in self.events:
            if event.status == "exception":
                errors.append(event)
        return errors

    def get_latest_event(self) -> TrackingEvent:
        """Returns the latest event to have occurred in the `events` list."""
        return self.events[-1]

    def has_errors(self) -> bool:
        """Returns `true` if there are any exception events."""
        for event in self.events:
            if event.status == "exception":
                return True
        return False

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

    def __repr__(self):
        return f"TrackPackageResult({self.shipment}, {self.package}, {self.events})"
