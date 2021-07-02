"""Validate a single address or multiple addresses."""
from typing import Any, Dict

from ..jsonrpc import rpc_request
from ..models.address import Address, AddressValidateResult
from ..models.enums import RPCMethods
from ..shipengine_config import ShipEngineConfig
from ..util import does_normalized_address_have_errors


def validate(address: Address, config: ShipEngineConfig) -> AddressValidateResult:
    """
    Validate a single address via the `address/validate` remote procedure.

    :param Address address: The address to be validate.
    :param ShipEngineConfig config: The global ShipEngine configuration object.
    :returns: :class:`AddressValidateResult`: The response from ShipEngine API including the
    validated and normalized address.
    """
    api_response: Dict[str, Any] = rpc_request(
        method=RPCMethods.ADDRESS_VALIDATE.value,
        config=config,
        params={"address": address.to_dict()},  # type: ignore
    )
    result: Dict[str, Any] = api_response["result"]
    return AddressValidateResult(
        is_valid=result["isValid"],
        request_id=api_response["id"],
        normalized_address=Address.from_dict(result["normalizedAddress"])
        if "normalizedAddress" in result and result["normalizedAddress"] is not None
        else None,
        messages=result["messages"],
    )


def normalize(address: Address, config: ShipEngineConfig) -> Address:
    """
    Normalize a given address into a standardized format.

    :param Address address: The address to be validate.
    :param ShipEngineConfig config: The global ShipEngine configuration object.
    :returns: :class:`Address`: The normalized address returned from ShipEngine API.
    """
    validation_result: AddressValidateResult = validate(address=address, config=config)
    does_normalized_address_have_errors(result=validation_result)
    return validation_result.normalized_address
