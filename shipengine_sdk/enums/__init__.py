"""ShipEngine SDK Enumerations"""
from enum import Enum

from .country import Country
from .error_code import ErrorCode
from .error_source import ErrorSource
from .error_type import ErrorType
from .regex_patterns import RegexPatterns


class BaseURL(Enum):
    """API Endpoint URI's used throughout the ShipEngine SDK."""

    SHIPENGINE_RPC_URL = "https://api.shipengine.com/"


class Constants(Enum):
    """Test API Key for use with Simengine."""

    STUB_API_KEY = "TEST_vMiVbICUjBz4BZjq0TRBLC/9MrxY4+yjvb1G1RMxlJs"


class HTTPVerbs(Enum):
    """A collection of HTTP verbs used in requests to ShipEngine API."""

    GET = "GET"
    DELETE = "DELETE"
    POST = "POST"
    PUT = "PUT"


class Endpoints(Enum):
    """A collection of RPC Methods used throughout the ShipEngine SDK."""

    ADDRESSES_VALIDATE = "v1/addresses/validate"
    GET_RATE_FROM_SHIPMENT = "v1/rates"
    LIST_CARRIERS = "v1/carriers"


def does_member_value_exist(m: str, enum_to_search) -> bool:
    """
    Checks if a member value exists on an Enum.

    :param str m: The member value to validate.
    :param enum_to_search: The enumeration to check the member value against.
    """
    return False if m not in (member.value for member in enum_to_search) else True
