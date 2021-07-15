"""
A collection of methods that provide `JSON-RPC 2.0` HTTP client
functionality for sending HTTP requests from the ShipEngine SDK.
"""
import time
from typing import Any, Dict, Optional

from ..errors import RateLimitExceededError
from ..http_client import ShipEngineClient
from ..shipengine_config import ShipEngineConfig
from .process_request import handle_response, wrap_request


def rpc_request(
    method: str, config: ShipEngineConfig, params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Create and send a `JSON-RPC 2.0` request over HTTP messages."""
    return rpc_request_loop(method, params, config)


def rpc_request_loop(
    method: str, params: Optional[Dict[str, Any]], config: ShipEngineConfig
) -> Dict[str, Any]:
    client: ShipEngineClient = ShipEngineClient(config=config)
    retry: int = 0
    api_response = None
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
