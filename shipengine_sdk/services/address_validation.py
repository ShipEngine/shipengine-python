"""Validate a single address or multiple addresses."""
from shipengine_sdk.jsonrpc import rpc_request
from shipengine_sdk.models.address import Address, AddressValidateResult
from shipengine_sdk.models.enums import RPCMethods
from shipengine_sdk.shipengine_config import ShipEngineConfig


def validate(address: Address, config: ShipEngineConfig) -> AddressValidateResult:
    """
    Validate a single address via the `address/validate` remote procedure.

    :param Address address: The address to be validate.
    :param ShipEngineConfig config: The global ShipEngine configuration object.
    :returns: :class:`AddressValidateResult`: The response from ShipEngine API including the
    validated and normalized address.
    """
    api_response: dict = rpc_request(
        method=RPCMethods.ADDRESS_VALIDATE.value,
        config=config,
        params={"address": address.to_dict()},
    )
    result = api_response["result"]
    return AddressValidateResult(
        is_valid=result["isValid"],
        request_id=api_response["id"],
        normalized_address=Address.from_dict(result["normalizedAddress"])
        if "normalizedAddress" in result
        else None,
        messages=result["messages"],
    )


def normalize(address: Address, config: ShipEngineConfig) -> Address:
    validation_result = validate(address=address, config=config)
    return validation_result.normalized_address
