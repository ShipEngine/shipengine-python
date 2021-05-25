"""Assertion helper functions."""
from shipengine_sdk.errors import InvalidFieldValueError, ValidationError
from shipengine_sdk.models import ErrorCode, ErrorSource, ErrorType


def is_api_key_valid(config: dict) -> None:
    """Check if API Key is set and is not empty or whitespace."""
    if "api_key" not in config or config["api_key"] == "":
        raise ValidationError(
            message="A ShipEngine API key must be specified.",
            source=ErrorSource.SHIPENGINE.value,
            error_type=ErrorType.VALIDATION.value,
            error_code=ErrorCode.FIELD_VALUE_REQUIRED.value,
        )


def is_retries_less_than_zero(config: dict) -> None:
    """Checks that config.retries is less than zero."""
    if "retries" in config and config["retries"] < 0:
        raise InvalidFieldValueError(
            field_name="retries",
            reason="Retries must be zero or greater.",
            field_value=config["retries"],
        )


def api_key_validation_error_assertions(e: ValidationError):
    """Helper test function that has common assertions pertaining to ValidationErrors."""
    assert type(e) is ValidationError
    assert e.request_id is None
    assert e.error_type is ErrorType.VALIDATION.value
    assert e.error_code is ErrorCode.FIELD_VALUE_REQUIRED.value
    assert e.source is ErrorSource.SHIPENGINE.value
    assert e.message == "A ShipEngine API key must be specified."
