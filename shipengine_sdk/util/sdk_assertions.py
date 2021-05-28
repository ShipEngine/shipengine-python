"""Assertion helper functions."""
import re

from shipengine_sdk.errors import (
    ClientSystemError,
    ClientTimeoutError,
    InvalidFieldValueError,
    RateLimitExceededError,
    ValidationError,
)
from shipengine_sdk.models import ErrorCode, ErrorSource, ErrorType


def is_api_key_valid(config: dict) -> None:
    """
    Check if API Key is set and is not empty or whitespace.

    :param dict config: The config dictionary passed into `ShipEngineConfig`.
    :returns: None, only raises exceptions.
    :rtype: None
    """
    message = "A ShipEngine API key must be specified."
    if "api_key" not in config or config["api_key"] == "":
        raise ValidationError(
            message=message,
            source=ErrorSource.SHIPENGINE.value,
            error_type=ErrorType.VALIDATION.value,
            error_code=ErrorCode.FIELD_VALUE_REQUIRED.value,
        )

    if re.match(r"\s", config["api_key"]):
        raise ValidationError(
            message=message,
            source=ErrorSource.SHIPENGINE.value,
            error_type=ErrorType.VALIDATION.value,
            error_code=ErrorCode.FIELD_VALUE_REQUIRED.value,
        )


def is_retries_valid(config: dict) -> None:
    """
    Checks that config.retries is a valid value.

    :param dict config: The config dictionary passed into `ShipEngineConfig`.
    :returns: None, only raises exceptions.
    :rtype: None
    """
    if "retries" in config and config["retries"] < 0:
        raise InvalidFieldValueError(
            field_name="retries",
            reason="Retries must be zero or greater.",
            field_value=config["retries"],
            source=ErrorSource.SHIPENGINE.value,
        )


def is_timeout_valid(config: dict) -> None:
    """
    Checks that config.timeout is valid value.

    :param dict config: The config dictionary passed into `ShipEngineConfig`.
    :returns: None, only raises exceptions.
    :rtype: None
    """
    if "timeout" in config and config["timeout"] < 0:
        raise InvalidFieldValueError(
            field_name="timeout",
            reason="Timeout must be zero or greater.",
            field_value=config["timeout"],
            source=ErrorSource.SHIPENGINE.value,
        )


def api_key_validation_error_assertions(error) -> None:
    """
    Helper test function that has common assertions pertaining to ValidationErrors.

    :param error: The error to execute assertions on.
    :returns: None, only executes assertions.
    :rtype: None
    """
    assert type(error) is ValidationError
    assert error.request_id is None
    assert error.error_type is ErrorType.VALIDATION.value
    assert error.error_code is ErrorCode.FIELD_VALUE_REQUIRED.value
    assert error.source is ErrorSource.SHIPENGINE.value
    assert error.message == "A ShipEngine API key must be specified."


def timeout_validation_error_assertions(error) -> None:
    """Helper test function that has common assertions pertaining to InvalidFieldValueError."""
    assert type(error) is InvalidFieldValueError
    assert error.request_id is None
    assert error.error_type is ErrorType.VALIDATION.value
    assert error.error_code is ErrorCode.INVALID_FIELD_VALUE.value
    assert error.source is ErrorSource.SHIPENGINE.value


def is_response_404(status_code: int, response_body: dict) -> None:
    """Check if status_code is 404 and raises an error if so."""
    if "error" in response_body:
        error = response_body["error"]
        error_data = error["data"]
        if status_code == 404:
            raise ClientSystemError(
                message=error["message"],
                request_id=response_body["id"],
                source=error_data["source"],
                error_type=error_data["type"],
                error_code=error_data["code"],
            )


def is_response_429(status_code: int, response_body: dict, config) -> None:
    """Check if status_code is 429 and raises an error if so."""
    if "error" in response_body and status_code == 429:
        error = response_body["error"]
        retry_after = error["data"]["retryAfter"]
        if retry_after > config.timeout:
            raise ClientTimeoutError(
                retry_after=config.timeout,
                source=ErrorSource.SHIPENGINE.value,
                request_id=response_body["id"],
            )
        else:
            raise RateLimitExceededError(
                retry_after=retry_after,
                source=ErrorSource.SHIPENGINE.value,
                request_id=response_body["id"],
            )


def is_response_500(status_code: int, response_body: dict) -> None:
    """Check if the status code is 500 and raises an error if so."""
    if status_code == 500:
        error = response_body["error"]
        error_data = error["data"]
        raise ClientSystemError(
            message=error["message"],
            request_id=response_body["id"],
            source=error_data["source"],
            error_type=error_data["type"],
            error_code=error_data["code"],
        )
