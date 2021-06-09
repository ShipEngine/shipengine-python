"""ShipEngine SDK Enumerations"""
from enum import Enum

from .carriers import CarrierNames, Carriers
from .country import Country
from .error_code import ErrorCode
from .error_source import ErrorSource
from .error_type import ErrorType


class Endpoints(Enum):
    """API Endpoint URI's used throughout the ShipEngine SDK."""

    TEST_RPC_URL = "https://simengine.herokuapp.com/jsonrpc"
    SHIPENGINE_RPC_URL = "https://api.shipengine.com/jsonrpc"


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
