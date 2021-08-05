"""A synchronous HTTP Client for the ShipEngine SDK."""
import json
import os
import platform
import time
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests
from requests import PreparedRequest, Request, RequestException, Response, Session
from requests.adapters import HTTPAdapter
from requests.auth import AuthBase
from requests.packages.urllib3.util.retry import Retry

from shipengine import __version__

from ..enums import ErrorCode, ErrorSource, ErrorType, HTTPVerbs
from ..errors import RateLimitExceededError, ShipEngineError
from ..shipengine_config import ShipEngineConfig
from ..util import check_response_for_errors


def base_url(config) -> str:
    return config.base_uri if os.getenv("CLIENT_BASE_URI") is None else os.getenv("CLIENT_BASE_URI")


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
    def __init__(self) -> None:
        """A `JSON-RPC 2.0` HTTP client used to send all HTTP requests from the SDK."""
        self.session = requests.session()

    def get(self, endpoint: str, config: ShipEngineConfig) -> Dict[str, Any]:
        """Send an HTTP GET request."""
        return self._request_loop(
            http_method=HTTPVerbs.GET.value, endpoint=endpoint, params=None, config=config
        )

    def post(
        self, endpoint: str, config: ShipEngineConfig, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Send an HTTP POST request."""
        return self._request_loop(
            http_method=HTTPVerbs.POST.value, endpoint=endpoint, params=params, config=config
        )

    def delete(self, endpoint: str, config: ShipEngineConfig):
        """Send an HTTP DELETE request."""
        return self._request_loop(
            http_method=HTTPVerbs.DELETE.value, endpoint=endpoint, params=None, config=config
        )

    def put(self, endpoint: str, config: ShipEngineConfig, params: Optional[Dict[str, Any]] = None):
        """Send an HTTP PUT request."""
        return self._request_loop(
            http_method=HTTPVerbs.PUT.value, endpoint=endpoint, params=params, config=config
        )

    def _request_loop(
        self,
        http_method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]],
        config: ShipEngineConfig,
    ) -> Dict[str, Any]:
        retry: int = 0
        while retry <= config.retries:
            try:
                api_response = self._send_request(
                    http_method=http_method,
                    endpoint=endpoint,
                    body=params,
                    retry=retry,
                    config=config,
                )
            except Exception as err:
                if (
                    retry < config.retries
                    and type(err) is RateLimitExceededError
                    and err.retry_after < config.timeout
                ):
                    time.sleep(err.retry_after)
                    retry += 1
                    continue
                else:
                    raise err
            return api_response

    def _send_request(
        self,
        http_method: str,
        endpoint: str,
        body: Optional[Dict[str, Any]],
        retry: int,
        config: ShipEngineConfig,
    ) -> Dict[str, Any]:
        """
        Send a `JSON-RPC 2.0` request via HTTP Messages to ShipEngine API. If the response
         * is successful, the result is returned. Otherwise, an error is thrown.
        """
        base_uri = base_url(config=config)
        client: Session = self._request_retry_session(retries=config.retries, url_base=base_uri)

        req_headers = request_headers(user_agent=self._derive_user_agent(), api_key=config.api_key)
        req: Request = Request(
            method=http_method,
            url=urljoin(base_uri, endpoint),
            data=json.dumps(body),
            headers=req_headers,
            auth=ShipEngineAuth(config.api_key),
        )
        prepared_req: PreparedRequest = req.prepare()

        try:
            resp: Response = client.send(request=prepared_req, timeout=config.timeout)
        except RequestException as err:
            raise ShipEngineError(
                message=f"An unknown error occurred while calling the ShipEngine {http_method} API:\n {err.response}",
                error_source=ErrorSource.SHIPENGINE.value,
                error_type=ErrorType.SYSTEM.value,
                error_code=ErrorCode.UNSPECIFIED.value,
            )

        resp_body: Dict[str, Any] = resp.json()
        status_code: int = resp.status_code

        check_response_for_errors(
            status_code=status_code,
            response_body=resp_body,
            response_headers=resp.headers,
            config=config,
        )
        return resp_body

    def _request_retry_session(
        self,
        url_base: str,
        retries: int = 1,
        backoff_factor=1,
        status_force_list=(429, 500, 502, 503, 504),
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
        self.session.url_base = url_base
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
        platform_os = platform.system()
        os_version = platform.release()
        python_version: str = platform.python_version()
        python_implementation: str = platform.python_implementation()

        return f"shipengine-python/{sdk_version} {platform_os}/{os_version} {python_implementation}/{python_version}"
