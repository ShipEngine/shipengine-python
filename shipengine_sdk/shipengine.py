"""The entrypoint to the ShipEngine API SDK."""
from typing import Any, Dict, Union

from shipengine_sdk.enums import Endpoints

from .http_client import ShipEngineClient
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
        self.client = ShipEngineClient()

        if type(config) is str:
            self.config = ShipEngineConfig({"api_key": config})
        elif type(config) is dict:
            self.config = ShipEngineConfig(config)

    def create_label_from_rate(
        self, rate_id: str, params: Dict[str, Any], config: Union[str, Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        When retrieving rates for shipments using the /rates endpoint, the returned information contains a rateId
        property that can be used to generate a label without having to refill in the shipment information repeatedly.
        See: https://shipengine.github.io/shipengine-openapi/#operation/create_label_from_rate

        :param str rate_id: The rate_id you wish to create a shipping label for.
        :params Dict[str, Any] params: A list of label params that will dictate the label display and
        level of verification.
        :param Union[str, Dict[str, Any], ShipEngineConfig] config: Method level configuration to set new values
        for properties of the global ShipEngineConfig object.
        :returns Dict[str, Any]: A label that corresponds the to shipment details for a rate_id you provided.
        """
        config = self.config.merge(new_config=config)
        return self.client.post(endpoint=f"v1/labels/rates/{rate_id}", params=params, config=config)

    def create_label_from_shipment(
        self, params: Dict[str, Any], config: Union[str, Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Purchase and print a shipping label for a given shipment.
        See: https://shipengine.github.io/shipengine-openapi/#operation/create_label
        # TODO: Add docstring type annotations.
        """
        config = self.config.merge(new_config=config)
        return self.client.post(endpoint="v1/labels", params=params, config=config)

    def get_rates_from_shipment(
        self, params: Dict[str, Any], config: Union[str, Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Given some shipment details and rate options, this endpoint returns a list of rate quotes.
        See: https://shipengine.github.io/shipengine-openapi/#operation/calculate_rates
        # TODO: Add docstring type annotations.
        """
        config = self.config.merge(new_config=config)
        return self.client.post(endpoint="v1/rates", params=params, config=config)

    def list_carriers(self, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Fetch the carrier accounts connected to your ShipEngine Account."""
        config = self.config.merge(new_config=config)
        return self.client.get(endpoint=Endpoints.LIST_CARRIERS.value, config=config)

    def validate_addresses(
        self, address: Dict[str, Any], config: Union[str, Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Address validation ensures accurate addresses and can lead to reduced shipping costs by preventing address
        correction surcharges. ShipEngine cross references multiple databases to validate addresses and identify
        potential deliverability issues.
        See: https://shipengine.github.io/shipengine-openapi/#operation/validate_address

        :param Dict[str, Any] address: The address to be validate.
        :param Union[str, Dict[str, Any], ShipEngineConfig] config: Method level configuration to set new values
        for properties of the global ShipEngineConfig object.
        :returns: Dict[str, Any]: The response from ShipEngine API including the validated and normalized address.
        """
        config = self.config.merge(new_config=config)
        return self.client.post(
            endpoint=Endpoints.ADDRESSES_VALIDATE.value, params=address, config=config
        )

    def void_label_by_label_id(
        self, label_id: str, config: Union[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Void label with a Label Id.
        See: https://shipengine.github.io/shipengine-openapi/#operation/void_label

        :param str label_id: The label_id of the label you wish to void.
        :param Union[str, Dict[str, Any], ShipEngineConfig] config: Method level configuration to set new values
        for properties of the global ShipEngineConfig object.
        :returns Dict[str, Any]: The response from ShipEngine API confirming the label was successfully voided or
        unable to be voided.
        """
        config = self.config.merge(new_config=config)
        return self.client.put(endpoint=f"v1/labels/{label_id}/void", config=config)
