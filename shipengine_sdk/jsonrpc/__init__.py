"""
A collection of methods that provide `JSON-RPC 2.0` HTTP client
functionality for sending HTTP requests from the ShipEngine SDK.
"""
import time
from typing import Dict, Optional

from ..errors import RateLimitExceededError
from ..http_client import ShipEngineClient
from ..shipengine_config import ShipEngineConfig
from .process_request import handle_response, wrap_request


def rpc_request(
    method: str, config: ShipEngineConfig, params: Optional[Dict[str, any]] = None
) -> Dict[str, any]:
    """
    Create and send a `JSON-RPC 2.0` request over HTTP messages.
    TODO: add param and return docs
    """
    return rpc_request_loop(method, params, config)


def rpc_request_loop(method: str, params: dict, config: ShipEngineConfig) -> Dict[str, any]:
    client: ShipEngineClient = ShipEngineClient()
    api_response: Optional[Dict[str, any]] = None
    retry: int = 0
    while retry <= config.retries:
        try:
            api_response: Dict[str, any] = client.send_rpc_request(
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
