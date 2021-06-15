"""Assertion helper functions."""
import re
from typing import Any, Dict, List

from ..errors import (
    ClientSystemError,
    ClientTimeoutError,
    InvalidFieldValueError,
    RateLimitExceededError,
    ShipEngineError,
    ValidationError,
)
from ..models.enums import Country, ErrorCode, ErrorSource, ErrorType

validation_message = "Invalid address. Either the postal code or the city/locality and state/province must be specified."  # noqa


def is_street_valid(street: List[str]) -> None:
    """Checks that street is not empty and that it is not too mAny address lines."""
    if len(street) == 0:
        raise ValidationError(
            message="Invalid address. At least one address line is required.",
            source=ErrorSource.SHIPENGINE.value,
            error_type=ErrorType.VALIDATION.value,
            error_code=ErrorCode.FIELD_VALUE_REQUIRED.value,
        )
    elif len(street) > 3:
        raise ValidationError(
            message="Invalid address. No more than 3 street lines are allowed.",
            source=ErrorSource.SHIPENGINE.value,
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
            source=ErrorSource.SHIPENGINE.value,
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
            source=ErrorSource.SHIPENGINE.value,
            error_type=ErrorType.VALIDATION.value,
            error_code=ErrorCode.FIELD_VALUE_REQUIRED.value,
        )


def is_postal_code_valid(postal_code: str) -> None:
    """Checks that the given postal code is alpha-numeric. A match would be '78756-123', '02215' or 'M6K 3C3'"""
    pattern = re.compile(r"^[a-zA-Z0-9\s-]*$")

    if not pattern.match(postal_code) or postal_code == "":
        raise ValidationError(
            message=validation_message,
            source=ErrorSource.SHIPENGINE.value,
            error_type=ErrorType.VALIDATION.value,
            error_code=ErrorCode.FIELD_VALUE_REQUIRED.value,
        )


def is_country_code_valid(country: str) -> None:
    """Check if the given country code is valid."""
    if country not in (member.value for member in Country):
        raise ValidationError(
            message=f"Invalid address: [{country}] is not a valid country code.",
            source=ErrorSource.SHIPENGINE.value,
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
            source=ErrorSource.SHIPENGINE.value,
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


def is_response_404(status_code: int, response_body: Dict[str, Any], config) -> None:
    """Check if status_code is 404 and raises an error if so."""
    if "error" in response_body and status_code == 404:
        error = response_body["error"]
        error_data = error["data"]
        raise ClientSystemError(
            message=error["message"],
            request_id=response_body["id"],
            source=error_data["source"],
            error_type=error_data["type"],
            error_code=error_data["code"],
        )
    elif status_code == 404:
        raise ShipEngineError(
            message=f"Resource not found, please check the base_uri you have set and try again. [{config.base_uri}] is currently set.",  # noqa
            source=ErrorSource.SHIPENGINE.value,
            error_type=ErrorType.SYSTEM.value,
            error_code=ErrorCode.NOT_FOUND.value,
        )


def is_response_429(status_code: int, response_body: Dict[str, Any], config) -> None:
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


def is_response_500(status_code: int, response_body: Dict[str, Any]) -> None:
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


def does_normalized_address_have_errors(result) -> None:
    """
    Assertions to check if the returned normalized address has Any errors. If errors
    are present an exception is thrown.

    :param AddressValidateResult result: The address validation response from ShipEngine API.
    """
    if len(result.errors) > 1:
        error_list = list()
        for err in result.errors:
            error_list.append(err["message"])

        str_errors = "\n".join(error_list)

        raise ShipEngineError(
            message=f"Invalid address.\n{str_errors}",
            request_id=result.request_id,
            source=ErrorSource.SHIPENGINE.value,
            error_type=ErrorType.ERROR.value,
            error_code=ErrorCode.INVALID_ADDRESS.value,
        )
    elif len(result.errors) == 1:
        raise ShipEngineError(
            message=f"Invalid address. {result.errors[0]['message']}",
            request_id=result.request_id,
            source=ErrorSource.SHIPENGINE.value,
            error_type=ErrorType.ERROR.value,
            error_code=result.errors[0]["code"],
        )
    elif result.is_valid is False:
        raise ShipEngineError(
            message="Invalid address - The address provided could not be normalized.",
            request_id=result.request_id,
            source=ErrorSource.SHIPENGINE.value,
            error_type=ErrorType.ERROR.value,
            error_code=ErrorCode.INVALID_ADDRESS.value,
        )


def is_package_id_valid(package_id: str) -> None:
    """Checks that package_id is valid."""
    pattern = re.compile(r"^pkg_[1-9a-zA-Z]+$")

    if not pattern.match(package_id):
        raise ValidationError(message=f"[{package_id}] is not a valid package ID.")
