"""A synchronous HTTP Client for the ShipEngine SDK."""
import json
import os
import platform
from datetime import datetime
from typing import Any, Dict, Optional

import requests
from requests import PreparedRequest, Request, RequestException, Response, Session
from requests.adapters import HTTPAdapter
from requests.auth import AuthBase
from requests.packages.urllib3.util.retry import Retry

from shipengine_sdk import __version__

from ..errors import ShipEngineError
from ..events import (
    Dispatcher,
    EventOptions,
    RequestSentEvent,
    ResponseReceivedEvent,
    ShipEngineEvent,
    emit_event,
)
from ..jsonrpc.process_request import handle_response, wrap_request
from ..models import ErrorCode, ErrorSource, ErrorType
from ..models.enums import Events
from ..shipengine_config import ShipEngineConfig
from ..util.sdk_assertions import check_response_for_errors


def base_url(config) -> str:
    return config.base_uri if os.getenv("CLIENT_BASE_URI") is None else os.getenv("CLIENT_BASE_URI")


def generate_event_message(
    retry: int,
    method: str,
    base_uri: str,
    status_code: Optional[int] = None,
    message_type: Optional[str] = None,
) -> str:
    if message_type == "received":
        if retry > 0:
            f"Retrying the ShipEngine {method} API at {base_uri}"
        else:
            return f"Received an HTTP {status_code} response from the ShipEngine {method} API"

    if retry == 0:
        return ShipEngineEvent.new_event_message(
            method=method, base_uri=base_uri, message_type="base_message"
        )
    else:
        return ShipEngineEvent.new_event_message(
            method=method, base_uri=base_uri, message_type="retry_message"
        )


def request_headers(user_agent: str, api_key: str) -> Dict[str, Any]:
    return {
        "User-Agent": user_agent,
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Api-Key": api_key,
    }


class ShipEngineAuth(AuthBase):
    def __init__(self, api_key: str) -> None:
        """Auth Base appends `Api-Key` header to all requests."""
        self.api_key: str = api_key

    def __call__(self, request: Request, *args, **kwargs) -> Request:
        request.headers["Api-Key"] = self.api_key
        return request


class ShipEngineClient:
    _DISPATCHER: Dispatcher = Dispatcher()

    def __init__(self, config: ShipEngineConfig) -> None:
        """A `JSON-RPC 2.0` HTTP client used to send all HTTP requests from the SDK."""
        self._DISPATCHER.register(
            event=Events.ON_REQUEST_SENT.value, subscriber=config.event_listener
        )
        self._DISPATCHER.register(
            event=Events.ON_RESPONSE_RECEIVED.value, subscriber=config.event_listener
        )
        self.session = requests.session()

    def send_rpc_request(
        self, method: str, params: Optional[Dict[str, Any]], retry: int, config: ShipEngineConfig
    ) -> Dict[str, Any]:
        """
        Send a `JSON-RPC 2.0` request via HTTP Messages to ShipEngine API. If the response
         * is successful, the result is returned. Otherwise, an error is thrown.
        """
        client: Session = self._request_retry_session(retries=config.retries)
        base_uri = base_url(config=config)

        request_body: Dict[str, Any] = wrap_request(method=method, params=params)
        req_headers = request_headers(user_agent=self._derive_user_agent(), api_key=config.api_key)
        req: Request = Request(
            method="POST",
            url=base_uri,
            data=json.dumps(request_body),
            headers=req_headers,
            auth=ShipEngineAuth(config.api_key),
        )
        prepared_req: PreparedRequest = req.prepare()

        request_event_message = generate_event_message(
            retry=retry, method=method, base_uri=base_uri
        )

        request_event_data = EventOptions(
            message=request_event_message,
            id=request_body["id"],
            base_uri=base_uri,
            request_headers=req_headers,
            body=request_body,
            retry=retry,
            timeout=config.timeout,
        )
        request_sent_event = emit_event(
            emitted_event_type=RequestSentEvent.REQUEST_SENT,
            event_data=request_event_data,
            dispatcher=self._DISPATCHER,
        )

        try:
            resp: Response = client.send(request=prepared_req, timeout=config.timeout)
        except RequestException as err:
            raise ShipEngineError(
                message=f"An unknown error occurred while calling the ShipEngine {method} API:\n {err.response}",
                source=ErrorSource.SHIPENGINE.value,
                error_type=ErrorType.SYSTEM.value,
                error_code=ErrorCode.UNSPECIFIED.value,
            )

        resp_body: Dict[str, Any] = resp.json()
        status_code: int = resp.status_code

        response_received_message = generate_event_message(
            retry=retry,
            method=method,
            base_uri=base_uri,
            status_code=status_code,
            message_type="received",
        )
        response_event_data = EventOptions(
            message=response_received_message,
            id=request_body["id"],
            base_uri=base_uri,
            status_code=status_code,
            response_headers=resp.headers,
            body=request_body,
            retry=retry,
            elapsed=(request_sent_event.timestamp - datetime.now()).total_seconds(),
        )

        # Emit `ResponseReceivedEvent` to registered Subscribers.
        emit_event(
            emitted_event_type=ResponseReceivedEvent.RESPONSE_RECEIVED,
            event_data=response_event_data,
            dispatcher=self._DISPATCHER,
        )

        check_response_for_errors(status_code=status_code, response_body=resp_body, config=config)
        return handle_response(resp.json())

    def _request_retry_session(
        self, retries: int = 1, backoff_factor=1, status_force_list=(429, 500, 502, 503, 504)
    ) -> Session:
        """A requests `Session()` that has retries enforced."""
        retry: Retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_force_list,
        )
        adapter: HTTPAdapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter=adapter)
        self.session.mount("https://", adapter=adapter)
        return self.session

    @staticmethod
    def _derive_user_agent() -> str:
        """
        Derive a User-Agent header from the environment. This is the user-agent that will
        be set on every request via the ShipEngine Client.

        :returns: A user-agent string that will be set in the `ShipEngineClient` request headers.
        :rtype: str
        """
        sdk_version: str = f"shipengine-python/{__version__}"
        python_version: str = platform.python_version()
        python_implementation: str = platform.python_implementation()

        return f"{sdk_version} {python_implementation}-v{python_version}"
