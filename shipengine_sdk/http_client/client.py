import os

from dotenv import load_dotenv
import requests
from requests.auth import AuthBase
from requests import HTTPError

load_dotenv()

"""A Python library for ShipEngine API."""


class ShipEngineAuth(AuthBase):
    def __init__(self, api_key):
        self.api_key = api_key

    def __call__(self, request):
        request.headers["API-Key"] = self.api_key
        return request


# TODO: Refactor to use the std library http module
class BaseClient:
    _DEFAULT_BASE_URI = "https://api.shipengine.com/v1/"

    def __init__(self, api_key: str = os.getenv("SHIPENGINE_API_KEY")):
        self.api_key = api_key
        self.session = requests.Session()

    def request(self, method: str, endpoint: str, *args, **kwargs):
        kwargs["auth"] = ShipEngineAuth(self.api_key)

        try:
            response = self.session.request(
                method, self._DEFAULT_BASE_URI + endpoint.strip("/"), **args, **kwargs
            )
            return response.json(), response.status_code
        except HTTPError as e:
            return [err["message"] for err in e.response.json()]

    def get(self, endpoint, *args, **kwargs):
        return self.request("GET", endpoint, *args, **kwargs)

    def post(self, endpoint, *args, **kwargs):
        return self.request("POST", endpoint, *args, **kwargs)
