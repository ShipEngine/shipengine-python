"""Exceptions that will be raised through-out the ShipEngine SDK."""
import json
from typing import Optional
from typing import Union

from shipengine_sdk.models import ErrorCode
from shipengine_sdk.models import ErrorSource
from shipengine_sdk.models import ErrorType


class ShipEngineException(Exception):
    """Base exception class that all other client exceptions will inherit from."""

    def __init__(
        self,
        message: str,
        request_id: Optional[str] = None,
        source: Optional[Union[ErrorSource, str]] = None,
        error_type: Optional[Union[ErrorType, str]] = None,
        error_code: Optional[Union[ErrorCode, str]] = None,
        url: Optional[str] = None,
    ):
        self.message = message
        self.request_id = request_id
        self.source = source
        self.error_code = error_code
        self.error_type = error_type
        self.url = url

        if self.source not in (member.value for member in ErrorSource):
            raise ValueError(
                f"source must be a member of ErrorSource enum - [{self.source}] provided."
            )

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)


class AccountStatusException(ShipEngineException):
    """An exception that indicates there is an issue with a given account's status."""


class BusinessRuleException(ShipEngineException):
    """An exception that indicates business rule logic has been violated."""


class SecurityException(ShipEngineException):
    """This exception will be raised in the event that authorization is failed."""


class SystemException(ShipEngineException):
    """This exception will be thrown on 500 server responses and fatal errors."""


class ValidationException(ShipEngineException):
    """An exception that indicates a given value does not match it's required type."""


class TimeoutException(ShipEngineException):
    """An exception that indicates the configured timeout has been reached for a given request."""

    def __init__(
        self,
        retry_after: int,
        source: Optional[ErrorSource] = None,
        request_id: Optional[str] = None,
    ):
        self.retry_after = retry_after
        self.source = source
        self.request_id = request_id
        super(TimeoutException, self).__init__(
            message=f"The request took longer than the {retry_after} seconds allowed.",
            request_id=self.request_id,
            source=self.source,
            error_type=ErrorType.SYSTEM,
            error_code=ErrorCode.TIMEOUT,
            url="https://www.shipengine.com/docs/rate-limits",
        )


class InvalidFieldValueException(ShipEngineException):
    """This error occurs when a field has been set to an invalid value."""

    def __init__(self, field_name: str, reason: str, field_value: str):
        self.field_name = field_name
        self.field_value = field_value
        super(InvalidFieldValueException, self).__init__(
            request_id=None,
            message=f"{self.field_name} - {reason}",
            source=None,
            error_type=ErrorType.VALIDATION,
            error_code=ErrorCode.INVALID_FIELD_VALUE,
        )


class RateLimitExceededException(ShipEngineException):
    """The amount of time (in SECONDS) to wait before retrying the request."""

    def __init__(
        self,
        retry_after: int,
        source: Optional[ErrorSource] = None,
        request_id: Optional[str] = None,
    ):
        self.retry_after = retry_after
        self.source = source
        self.request_id = request_id
        super(RateLimitExceededException, self).__init__(
            message="You have exceeded the rate limit.",
            request_id=self.request_id,
            source=self.source,
            error_type=ErrorType.SYSTEM,
            error_code=ErrorCode.RATE_LIMIT_EXCEEDED,
            url="https://www.shipengine.com/docs/rate-limits",
        )
