"""ShipEngine SDK Enumerations"""
from enum import Enum

from .error_code import ErrorCode
from .error_source import ErrorSource
from .error_type import ErrorType


class Endpoints(Enum):
    TEST_RPC_URL = "https://simengine.herokuapp.com/jsonrpc"
    SHIPENGINE_RPC_URL = "https://api.shipengine.com/jsonrpc"
