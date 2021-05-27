"""
A collection of methods that provide `JSON-RPC 2.0` HTTP client
functionality for sending HTTP requests from the ShipEngine SDK.
"""
import time
from typing import Dict, Optional

from shipengine_sdk.errors import RateLimitExceededError
from shipengine_sdk.http_client import ShipEngineClient
from shipengine_sdk.shipengine_config import ShipEngineConfig

from .process_request import handle_response, wrap_request


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
    api_response = None
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
        retry += 1
    return api_response
