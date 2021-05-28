"""ShipEngine SDK Enumerations"""
from enum import Enum

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
