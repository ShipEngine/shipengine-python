"""The entrypoint to the ShipEngine API SDK."""
from typing import Any, Dict, List, Optional, Union

from .models import CarrierAccount, TrackingQuery, TrackPackageResult
from .models.address import Address, AddressValidateResult
from .services.address_validation import normalize, validate
from .services.get_carrier_accounts import GetCarrierAccounts
from .services.track_package import track
from .shipengine_config import ShipEngineConfig


class ShipEngine:
    config: ShipEngineConfig
    """
    Global configuration for the ShipEngine API client, such as timeouts,
    retries, page size, etc. This configuration applies to all method calls,
    unless specifically overridden when calling a method.
    """

    def __init__(self, config: Union[str, Dict[str, Any], ShipEngineConfig]) -> None:
        """
        Exposes the functionality of the ShipEngine API.

        The `api_key` you pass in can be either a ShipEngine sandbox
        or production API Key. (sandbox keys start with "TEST_")
        """

        if type(config) is str:
            self.config = ShipEngineConfig({"api_key": config})
        elif type(config) is dict:
            self.config = ShipEngineConfig(config)

    def validate_address(
        self, address: Address, config: Optional[Union[Dict[str, Any], ShipEngineConfig]] = None
    ) -> AddressValidateResult:
        """
        Validate an address in nearly any countryCode in the world.

        :param Address address: The address to be validate.
        :param ShipEngineConfig config: The global ShipEngine configuration object.
        :returns: :class:`AddressValidateResult`: The response from ShipEngine API including the
        validated and normalized address.
        """
        config = self.config.merge(new_config=config)
        return validate(address=address, config=config)

    def normalize_address(
        self, address: Address, config: Optional[Union[Dict[str, Any], ShipEngineConfig]] = None
    ) -> Address:
        """Normalize a given address into a standardized format used by carriers."""
        config = self.config.merge(new_config=config)
        return normalize(address=address, config=config)

    def get_carrier_accounts(
        self,
        carrier_code: Optional[str] = None,
        config: Optional[Union[Dict[str, Any], ShipEngineConfig]] = None,
    ) -> List[CarrierAccount]:
        """Fetch a list of the carrier accounts connected to your ShipEngine Account."""
        config = self.config.merge(new_config=config)
        get_accounts = GetCarrierAccounts()
        return get_accounts.fetch_carrier_accounts(config=config, carrier_code=carrier_code)

    def track_package(
        self,
        tracking_data: Union[str, TrackingQuery],
        config: Optional[Union[Dict[str, Any], ShipEngineConfig]] = None,
    ) -> TrackPackageResult:
        """
        Track a package by `tracking_number` and `carrier_code` via the **TrackingQuery** object, by using just the
        **package_id**.
        """
        config = self.config.merge(new_config=config)
        return track(tracking_data=tracking_data, config=config)
