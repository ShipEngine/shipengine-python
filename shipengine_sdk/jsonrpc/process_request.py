"""Functions that help with process requests and handle responses."""
from typing import Dict, Optional
from uuid import uuid4

from shipengine_sdk.errors import (
    AccountStatusError,
    BusinessRuleError,
    ClientSecurityError,
    ClientSystemError,
    ShipEngineError,
    ValidationError,
)
from shipengine_sdk.models import ErrorType


def wrap_request(method: str, params: Optional[Dict[str, any]]) -> dict:
    """
    Wrap request per `JSON-RPC 2.0` spec.

    :param str method: The RPC Method to be sent to the RPC Server to
    invoke a specific remote procedure.
    :param params: The request data for the RPC request. This argument
    is optional and can either be a dictionary or None.
    :type params: Optional[Dict[str, any]]
    """
    if params is None:
        return dict(id=f"req_{str(uuid4()).replace('-', '')}", jsonrpc="2.0", method=method)
    else:
        return dict(
            id=f"req_{str(uuid4()).replace('-', '')}", jsonrpc="2.0", method=method, params=params
        )


def handle_response(response_body: dict) -> dict:
    """Handles the response from ShipEngine API."""
    if "result" in response_body:
        return response_body

    error = response_body["error"]
    error_data = error["data"]
    error_type = error_data["type"]
    if error_type is ErrorType.ACCOUNT_STATUS.value:
        raise AccountStatusError(
            message=error["message"],
            request_id=response_body["id"],
            source=error_data["source"],
            error_type=error_data["type"],
            error_code=error_data["code"],
        )
    elif error_type is ErrorType.SECURITY.value:
        raise ClientSecurityError(
            message=error["message"],
            request_id=response_body["id"],
            source=error_data["source"],
            error_type=error_data["type"],
            error_code=error_data["code"],
        )
    elif error_type is ErrorType.VALIDATION.value:
        raise ValidationError(
            message=error["message"],
            request_id=response_body["id"],
            source=error_data["source"],
            error_type=error_data["type"],
            error_code=error_data["code"],
        )
    elif error_type is ErrorType.BUSINESS_RULES.value:
        raise BusinessRuleError(
            message=error["message"],
            request_id=response_body["id"],
            source=error_data["source"],
            error_type=error_data["type"],
            error_code=error_data["code"],
        )
    elif error_type is ErrorType.SYSTEM.value:
        raise ClientSystemError(
            message=error["message"],
            request_id=response_body["id"],
            source=error_data["source"],
            error_type=error_data["type"],
            error_code=error_data["code"],
        )
    else:
        raise ShipEngineError(
            message=error["message"],
            request_id=response_body["id"],
            source=error_data["source"],
            error_type=error_data["type"],
            error_code=error_data["code"],
        )
