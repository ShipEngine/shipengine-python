"""ShipEngine SDK Enumerations"""
from enum import Enum

from .carriers import CarrierNames, Carriers
from .country import Country
from .error_code import ErrorCode
from .error_source import ErrorSource
from .error_type import ErrorType
from .regex_patterns import RegexPatterns


class Constants(Enum):
    """Test API Key for use with Simengine."""

    API_KEY = "TEST_vMiVbICUjBz4BZjq0TRBLC/9MrxY4+yjvb1G1RMxlJs"
    CARRIER_ACCOUNT_ID_STUB = "car_41GrQHn5uouiPZc2TNE6PU29tZU9ud"


class Endpoints(Enum):
    """API Endpoint URI's used throughout the ShipEngine SDK."""

    TEST_RPC_URL = "https://shipengine-web-api.herokuapp.com/jsonrpc"
    SHIPENGINE_RPC_URL = "https://api.shipengine.com/jsonrpc"


class Events(Enum):
    """ShipEngine Events emitted by the SDK when a request is sent or when a response is received."""

    ON_REQUEST_SENT = "on_request_sent"
    ON_RESPONSE_RECEIVED = "on_response_received"


class RPCMethods(Enum):
    """A collection of RPC Methods used throughout the ShipEngine SDK."""

    ADDRESS_VALIDATE = "address.validate.v1"
    CREATE_TAG = "create.tag.v1"
    LIST_CARRIERS = "carrier.listAccounts.v1"
    TRACK_PACKAGE = "package.track.v1"


def does_member_value_exist(m: str, enum_to_search) -> bool:
    """
    Checks if a member value exists on an Enum.

    :param str m: The member value to validate.
    :param enum_to_search: The enumeration to check the member value against.
    """
    return False if m not in (member.value for member in enum_to_search) else True


def get_carrier_name_value(upper_carrier_code: str):
    for k in CarrierNames:
        if upper_carrier_code == k.name:
            return k.value
