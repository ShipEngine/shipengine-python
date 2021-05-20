"""Exceptions that will be raised through-out the ShipEngine SDK."""


class ShipEngineException(Exception):
    """Base exception class that all other client exceptions will inherit from."""

    def __init__(self, request_id: str, message: str, source, error_type, error_code, url):
        self.request_id = request_id
        self.message = message
        self.source = source
        self.error_code = error_code
        self.error_type = error_type
        self.url = url


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


class InvalidFieldValueException(ShipEngineException):
    """"""


class RateLimitExceededException(ShipEngineException):
    """"""
