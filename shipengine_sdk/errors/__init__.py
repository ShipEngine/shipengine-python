"""Errors that will be raised through-out the ShipEngine SDK."""
import json
from typing import Optional
from typing import Union

from shipengine_sdk.models import ErrorCode
from shipengine_sdk.models import ErrorSource
from shipengine_sdk.models import ErrorType


class ShipEngineError(Exception):
    """Base exception class that all other client errors will inherit from."""

    def __init__(
        self,
        message: str,
        request_id: Optional[str] = None,
        source: Optional[str] = None,
        error_type: Optional[str] = None,
        error_code: Optional[str] = None,
        url: Optional[str] = None,
    ):
        self.message = message
        self.request_id = request_id
        self.source = source
        self.error_code = error_code
        self.error_type = error_type
        self.url = url
        self._are_enums_valid()

    def _are_enums_valid(self):
        if self.source is None:
            return self
        elif self.source not in (member.value for member in ErrorSource):
            raise ValueError(
                f"Error source must be a member of ErrorSource enum - [{self.source}] provided."
            )

        if self.error_type is None:
            return self
        elif self.error_type not in (member.value for member in ErrorType):
            raise ValueError(
                f"Error type must be a member of ErrorType enum - [{self.error_type}] provided."
            )

        if self.error_code is None:
            return self
        elif self.error_code not in (member.value for member in ErrorCode):
            raise ValueError(
                f"Error type must be a member of ErrorCode enum - [{self.error_code}] provided."
            )

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)


class AccountStatusError(ShipEngineError):
    """An exception that indicates there is an issue with a given account's status."""


class BusinessRuleError(ShipEngineError):
    """An exception that indicates business rule logic has been violated."""


class ClientSecurityError(ShipEngineError):
    """This exception will be raised in the event that authorization is failed."""


class ClientSystemError(ShipEngineError):
    """This exception will be thrown on 500 server responses and fatal errors."""


class ValidationError(ShipEngineError):
    """An exception that indicates a given value does not match it's required type."""


class ClientTimeoutError(ShipEngineError):
    """An exception that indicates the configured timeout has been reached for a given request."""

    def __init__(
        self,
        retry_after: int,
        source: Optional[str] = None,
        request_id: Optional[str] = None,
    ):
        self.retry_after = retry_after
        self.source = source
        self.request_id = request_id
        super(ClientTimeoutError, self).__init__(
            message=f"The request took longer than the {retry_after} seconds allowed.",
            request_id=self.request_id,
            source=self.source,
            error_type=ErrorType.SYSTEM.value,
            error_code=ErrorCode.TIMEOUT.value,
            url="https://www.shipengine.com/docs/rate-limits",
        )


class InvalidFieldValueError(ShipEngineError):
    """This error occurs when a field has been set to an invalid value."""

    def __init__(self, field_name: str, reason: str, field_value):
        self.field_name = field_name
        self.field_value = field_value
        super(InvalidFieldValueError, self).__init__(
            request_id=None,
            message=f"{self.field_name} - {reason}",
            source=None,
            error_type=ErrorType.VALIDATION.value,
            error_code=ErrorCode.INVALID_FIELD_VALUE.value,
        )


class RateLimitExceededError(ShipEngineError):
    """The amount of time (in SECONDS) to wait before retrying the request."""

    def __init__(
        self,
        retry_after: int,
        source: Optional[str] = None,
        request_id: Optional[str] = None,
    ):
        self.retry_after = retry_after
        self.source = source
        self.request_id = request_id
        super(RateLimitExceededError, self).__init__(
            message="You have exceeded the rate limit.",
            request_id=self.request_id,
            source=self.source,
            error_type=ErrorType.SYSTEM.value,
            error_code=ErrorCode.RATE_LIMIT_EXCEEDED.value,
            url="https://www.shipengine.com/docs/rate-limits",
        )
