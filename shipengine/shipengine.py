"""The entrypoint to the ShipEngine API SDK."""
from typing import Any, Dict, List, Union

from shipengine.enums import Endpoints

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

    def create_label_from_rate_id(
        self, rate_id: str, params: Dict[str, Any], config: Union[str, Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        When retrieving rates for shipments using the /rates endpoint, the returned information contains a rateId
        property that can be used to generate a label without having to refill in the shipment information repeatedly.
        See: https://shipengine.github.io/shipengine-openapi/#operation/create_label_from_rate

        :param str rate_id: The rate_id you wish to create a shipping label for.
        :param Dict[str, Any] params: A dictionary of label params that will dictate the label display and
        level of verification.
        :param Union[str, Dict[str, Any], ShipEngineConfig] config: Method level configuration to set new values
        for properties of the global ShipEngineConfig object.
        :returns Dict[str, Any]: A label that corresponds the to shipment details for the rate_id provided.
        """
        config = self.config.merge(new_config=config)
        return self.client.post(endpoint=f"v1/labels/rates/{rate_id}", params=params, config=config)

    def create_label_from_shipment(
        self, shipment: Dict[str, Any], config: Union[str, Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Purchase and print a shipping label for a given shipment.
        See: https://shipengine.github.io/shipengine-openapi/#operation/create_label

        :param Dict[str, Any] shipment: A dictionary of shipment details for the label creation.
        :param Union[str, Dict[str, Any], ShipEngineConfig] config: Method level configuration to set new values
        for properties of the global ShipEngineConfig object.
        :returns Dict[str, Any]: A label that corresponds the to shipment details provided.
        """
        config = self.config.merge(new_config=config)
        return self.client.post(endpoint="v1/labels", params=shipment, config=config)

    def get_rates_from_shipment(
        self, shipment: Dict[str, Any], config: Union[str, Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Given some shipment details and rate options, this endpoint returns a list of rate quotes.
        See: https://shipengine.github.io/shipengine-openapi/#operation/calculate_rates

        :param Dict[str, Any] shipment: A dictionary of shipment details for the label creation.
        :param Union[str, Dict[str, Any], ShipEngineConfig] config: Method level configuration to set new values
        for properties of the global ShipEngineConfig object.
        :returns Dict[str, Any]: A label that corresponds the to shipment details provided.
        """
        config = self.config.merge(new_config=config)
        return self.client.post(
            endpoint=Endpoints.GET_RATE_FROM_SHIPMENT.value, params=shipment, config=config
        )

    def list_carriers(self, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Fetch the carrier accounts connected to your ShipEngine Account.

        :param Union[str, Dict[str, Any], ShipEngineConfig] config: Method level configuration to set new values
        for properties of the global ShipEngineConfig object.
        :returns Dict[str, Any]: The carrier accounts associated with a given ShipEngine Account.
        """
        config = self.config.merge(new_config=config)
        return self.client.get(endpoint=Endpoints.LIST_CARRIERS.value, config=config)

    def track_package_by_label_id(
        self, label_id: str, config: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Retrieve a given shipping label's tracking information with a label_id.
        See: https://shipengine.github.io/shipengine-openapi/#operation/get_tracking_log_from_label

        :param str label_id: The label_id for a shipment you wish to get tracking information for.
        (Best option if you create labels via ShipEngine API)
        :param Union[str, Dict[str, Any], ShipEngineConfig] config: Method level configuration to set new values
        for properties of the global ShipEngineConfig object.
        :returns Dict[str, Any]: Tracking information corresponding to the label_id provided.
        """
        config = self.config.merge(new_config=config)
        return self.client.get(endpoint=f"v1/labels/{label_id}/track", config=config)

    def track_package_by_carrier_code_and_tracking_number(
        self, carrier_code: str, tracking_number: str, config: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Retrieve the label's tracking information with Carrier Code and Tracking Number.
        See: https://shipengine.github.io/shipengine-openapi/#operation/get_tracking_log

        :param str carrier_code: The carrier_code for the carrier servicing the shipment.
        :param Union[str, Dict[str, Any], ShipEngineConfig] config: Method level configuration to set new values
        for properties of the global ShipEngineConfig object.
        :returns Dict[str, Any]: Tracking information corresponding to the carrier_code and tracking_number provided.
        """
        config = self.config.merge(new_config=config)
        return self.client.get(
            endpoint=f"v1/tracking?carrier_code={carrier_code}&tracking_number={tracking_number}",
            config=config,
        )

    def validate_addresses(
        self, address: List[Dict[str, Any]], config: Union[str, Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Address validation ensures accurate addresses and can lead to reduced shipping costs by preventing address
        correction surcharges. ShipEngine cross references multiple databases to validate addresses and identify
        potential deliverability issues.
        See: https://shipengine.github.io/shipengine-openapi/#operation/validate_address

        :param List[Dict[str, Any]] address: A list containing the address(es) to be validated.
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
