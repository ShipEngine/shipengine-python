"""Assertion helper functions."""
import re
from typing import Any, Dict, List

from shipengine.enums import Country, ErrorCode, ErrorSource, ErrorType

from ..errors import (
    ClientSystemError,
    ClientTimeoutError,
    InvalidFieldValueError,
    RateLimitExceededError,
    ShipEngineError,
    ValidationError,
)

validation_message = "Invalid address. Either the postal code or the city/locality and state/province must be specified."  # noqa


def is_street_valid(street: List[str]) -> None:
    """Checks that street is not empty and that it is not too mAny address lines."""
    if len(street) == 0:
        raise ValidationError(
            message="Invalid address. At least one address line is required.",
            error_source=ErrorSource.SHIPENGINE.value,
            error_type=ErrorType.VALIDATION.value,
            error_code=ErrorCode.FIELD_VALUE_REQUIRED.value,
        )
    elif len(street) > 3:
        raise ValidationError(
            message="Invalid address. No more than 3 street lines are allowed.",
            error_source=ErrorSource.SHIPENGINE.value,
            error_type=ErrorType.VALIDATION.value,
            error_code=ErrorCode.INVALID_FIELD_VALUE.value,
        )


def is_city_valid(city: str) -> None:
    """Asserts that city in not an empty string and contains valid characters."""
    latin_pattern = re.compile(r"^[a-zA-Z0-9\s\W]*$")
    non_latin_pattern = re.compile(r"[\u4e00-\u9fff]+")

    if non_latin_pattern.match(city):
        return
    elif not latin_pattern.match(city) or city == "":
        raise ValidationError(
            message=validation_message,
            error_source=ErrorSource.SHIPENGINE.value,
            error_type=ErrorType.VALIDATION.value,
            error_code=ErrorCode.FIELD_VALUE_REQUIRED.value,
        )


def is_state_valid(state: str) -> None:
    """Asserts that state is 2 capitalized letters and that it is not an empty string."""
    latin_pattern = re.compile(r"^[a-zA-Z]*$")
    non_latin_pattern = re.compile(r"[\u4e00-\u9fff]+")

    if non_latin_pattern.match(state):
        return
    elif not latin_pattern.match(state) or state == "":
        raise ValidationError(
            message=validation_message,
            error_source=ErrorSource.SHIPENGINE.value,
            error_type=ErrorType.VALIDATION.value,
            error_code=ErrorCode.FIELD_VALUE_REQUIRED.value,
        )


def is_postal_code_valid(postal_code: str) -> None:
    """Checks that the given postal code is alpha-numeric. A match would be '78756-123', '02215' or 'M6K 3C3'"""
    pattern = re.compile(r"^[a-zA-Z0-9\s-]*$")

    if not pattern.match(postal_code) or postal_code == "":
        raise ValidationError(
            message=validation_message,
            error_source=ErrorSource.SHIPENGINE.value,
            error_type=ErrorType.VALIDATION.value,
            error_code=ErrorCode.FIELD_VALUE_REQUIRED.value,
        )


def is_country_code_valid(country: str) -> None:
    """Check if the given country code is valid."""
    if country not in (member.value for member in Country):
        raise ValidationError(
            message=f"Invalid address: [{country}] is not a valid country code.",
            error_source=ErrorSource.SHIPENGINE.value,
            error_type=ErrorType.VALIDATION.value,
            error_code=ErrorCode.FIELD_VALUE_REQUIRED.value,
        )


def is_api_key_valid(config: Dict[str, Any]) -> None:
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
            error_source=ErrorSource.SHIPENGINE.value,
            error_type=ErrorType.VALIDATION.value,
            error_code=ErrorCode.FIELD_VALUE_REQUIRED.value,
        )

    if re.match(r"\s", config["api_key"]):
        raise ValidationError(
            message=message,
            error_source=ErrorSource.SHIPENGINE.value,
            error_type=ErrorType.VALIDATION.value,
            error_code=ErrorCode.FIELD_VALUE_REQUIRED.value,
        )


def is_retries_valid(config: Dict[str, Any]) -> None:
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
            error_source=ErrorSource.SHIPENGINE.value,
        )


def is_timeout_valid(config: Dict[str, Any]) -> None:
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
            error_source=ErrorSource.SHIPENGINE.value,
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
    assert error.error_source is ErrorSource.SHIPENGINE.value
    assert error.message == "A ShipEngine API key must be specified."


def timeout_validation_error_assertions(error) -> None:
    """Helper test function that has common assertions pertaining to InvalidFieldValueError."""
    assert type(error) is InvalidFieldValueError
    assert error.request_id is None
    assert error.error_type is ErrorType.VALIDATION.value
    assert error.error_code is ErrorCode.INVALID_FIELD_VALUE.value
    assert error.error_source is ErrorSource.SHIPENGINE.value


def check_response_for_errors(
    status_code: int, response_body: Dict[str, Any], response_headers, config
) -> None:
    """Checks response and status_code for 400, 404, 429, and 500 error cases and raises an approved exception."""

    if status_code == 400:
        error = response_body["errors"][0]
        raise ShipEngineError(
            message=error["message"],
            error_source=ErrorSource.SHIPENGINE.value,
            error_type=error["error_type"],
            error_code=error["error_code"],
        )

    if status_code == 404:
        error = response_body["errors"][0]
        raise ShipEngineError(
            message=error["message"],
            error_source=ErrorSource.SHIPENGINE.value,
            error_type=error["error_type"],
            error_code=error["error_code"],
        )

    # Check if status_code is 429 and raises an error if so.
    if status_code == 429:
        retry_after = response_headers["Retry-After"]
        if retry_after > config.timeout:
            raise ClientTimeoutError(
                retry_after=config.timeout,
                error_source=ErrorSource.SHIPENGINE.value,
                request_id=response_body["request_id"],
            )
        else:
            raise RateLimitExceededError(
                retry_after=retry_after,
                error_source=ErrorSource.SHIPENGINE.value,
                request_id=response_body["request_id"],
            )

    # Check if the status code is 500 and raises an error if so.
    if status_code == 500:
        error = response_body["errors"][0]
        raise ClientSystemError(
            message=error["message"],
            request_id=response_body["request_id"],
            error_source=error["error_source"],
            error_type=error["error_type"],
            error_code=error["error_code"],
        )


# def is_package_id_valid(package_id: str) -> None:
#     """Checks that package_id is valid."""
#     pattern = re.compile(r"^pkg_[1-9a-zA-Z]+$")
#
#     if not package_id.startswith("pkg_"):
#         raise ValidationError(
#                 message=f"[{package_id[0:4]}] is not a valid package ID prefix.",
#                 error_source=ErrorSource.SHIPENGINE.value,
#                 error_type=ErrorType.VALIDATION.value,
#                 error_code=ErrorCode.INVALID_IDENTIFIER.value,
#         )
#
#     if not pattern.match(package_id):
#         raise ValidationError(
#                 message=f"[{package_id}] is not a valid package ID.",
#                 error_source=ErrorSource.SHIPENGINE.value,
#                 error_type=ErrorType.VALIDATION.value,
#                 error_code=ErrorCode.INVALID_IDENTIFIER.value,
#         )
