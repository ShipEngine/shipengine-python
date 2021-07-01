"""A Python library for ShipEngine API."""
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
    EventOptions,
    RequestSentEvent,
    ResponseReceivedEvent,
    ShipEngineEvent,
    emit_event,
)
from ..jsonrpc.process_request import handle_response, wrap_request
from ..models import ErrorCode, ErrorSource, ErrorType
from ..shipengine_config import ShipEngineConfig
from ..util.sdk_assertions import is_response_404, is_response_429, is_response_500


def base_url(config) -> str:
    return config.base_uri if os.getenv("CLIENT_BASE_URI") is None else os.getenv("CLIENT_BASE_URI")


def check_for_errors(status_code: int, response_body: Dict[str, Any], config) -> None:
    is_response_404(status_code=status_code, response_body=response_body, config=config)
    is_response_429(status_code=status_code, response_body=response_body, config=config)
    is_response_500(status_code=status_code, response_body=response_body)


def generate_event_message(retry: int, method: str, base_uri: str) -> str:
    if retry == 0:
        return ShipEngineEvent.new_event_message(
            method=method, base_uri=base_uri, message_type="base_message"
        )
    else:
        return ShipEngineEvent.new_event_message(
            method=method, base_uri=base_uri, message_type="retry_message"
        )


def request_headers(user_agent: str) -> Dict[str, Any]:
    return {
        "User-Agent": user_agent,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


class ShipEngineAuth(AuthBase):
    def __init__(self, api_key: str) -> None:
        """Auth Base appends `Api-Key` header to all requests."""
        self.api_key: str = api_key

    def __call__(self, request: Request, *args, **kwargs) -> Request:
        request.headers["Api-Key"] = self.api_key
        return request


class ShipEngineClient:
    _BASE_URI: str = ""

    def __init__(self) -> None:
        """A `JSON-RPC 2.0` HTTP client used to send all HTTP requests from the SDK."""
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

        # base_uri: Optional[str] = (
        #     config.base_uri
        #     if os.getenv("CLIENT_BASE_URI") is None
        #     else os.getenv("CLIENT_BASE_URI")
        # )

        # request_headers: Dict[str, Any] = {
        #     "User-Agent": self._derive_user_agent(),
        #     "Content-Type": "application/json",
        #     "Accept": "application/json",
        # }

        request_body: Dict[str, Any] = wrap_request(method=method, params=params)
        req_headers = request_headers(self._derive_user_agent())
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
            config=config,
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

        response_event_data = EventOptions(
            message=request_event_message,
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
            config=config,
        )

        check_for_errors(status_code=status_code, response_body=resp_body, config=config)
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
        os_kernel: str = platform.platform(terse=True)
        python_version: str = platform.python_version()
        python_implementation: str = platform.python_implementation()

        return f"{sdk_version} {os_kernel} {python_version} {python_implementation}"
