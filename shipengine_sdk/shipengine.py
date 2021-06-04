"""The entrypoint to the ShipEngine API SDK."""
from typing import Dict, Union

from .models.address import Address, AddressValidateResult
from .services.address_validation import validate
from .shipengine_config import ShipEngineConfig


class ShipEngine:
    config: ShipEngineConfig
    """
    Global configuration for the ShipEngine API client, such as timeouts,
    retries, page size, etc. This configuration applies to all method calls,
    unless specifically overridden when calling a method.
    """

    def __init__(self, config: Union[str, Dict[str, any], ShipEngineConfig]) -> None:
        """
        Exposes the functionality of the ShipEngine API.

        The `api_key` you pass in can be either a ShipEngine sandbox
        or production API Key. (sandbox keys start with "TEST_")
        """

        if type(config) is str:
            self.config: ShipEngineConfig = ShipEngineConfig({"api_key": config})
        elif type(config) is dict:
            self.config: ShipEngineConfig = ShipEngineConfig(config)

    def validate_address(
        self, address: Address, config: Union[Dict[str, any], ShipEngineConfig] = None
    ) -> AddressValidateResult:
        """
        Validate an address in nearly any countryCode in the world.

        :param Address address: The address to be validate.
        :param ShipEngineConfig config: The global ShipEngine configuration object.
        :returns: :class:`AddressValidateResult`: The response from ShipEngine API including the
        validated and normalized address.
        """
        config: ShipEngineConfig = self.config.merge(new_config=config)
        return validate(address, config)
