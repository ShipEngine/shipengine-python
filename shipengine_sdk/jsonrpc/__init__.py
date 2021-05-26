"""
A collection of methods that provide `JSON-RPC 2.0` HTTP client
functionality for sending HTTP requests from the ShipEngine SDK.
"""
import os
import time
from typing import Dict, Optional, Union
from uuid import uuid4

from shipengine_sdk import ShipEngineConfig
from shipengine_sdk.errors import RateLimitExceededError
from shipengine_sdk.http_client import ShipEngineClient


def rpc_request(
    method: str, config: ShipEngineConfig, params: Optional[Dict[str, any]] = None
) -> dict:
    """
    Create and send a `JSON-RPC 2.0` request over HTTP messages.
    TODO: add param and return docs
    """
    return rpc_request_loop(method, params, config)


def rpc_request_loop(method: str, params: dict, config: ShipEngineConfig) -> dict:
    client = ShipEngineClient()
    retry: int = 0
    while retry <= config.retries:
        try:
            api_response = client.send_rpc_request(
                method=method, params=params, retry=retry, config=config
            )
        except Exception as err:
            if (
                retry < config.retries
                and type(err) is RateLimitExceededError
                and err.retry_after < config.timeout
            ):
                time.sleep(err.retry_after)
            else:
                raise err
    return api_response  # TODO: pick up here


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
