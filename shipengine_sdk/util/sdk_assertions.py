"""Initial Docstring"""
from shipengine_sdk.errors import InvalidFieldValueError
from shipengine_sdk.errors import ValidationError
from shipengine_sdk.models import ErrorCode
from shipengine_sdk.models import ErrorSource
from shipengine_sdk.models import ErrorType


def is_api_key_valid(config: dict) -> None:
    if "api_key" not in config or config["api_key"] == "":
        raise ValidationError(
            message="A ShipEngine API key must be specified.",
            source=ErrorSource.SHIPENGINE.value,
            error_type=ErrorType.VALIDATION.value,
            error_code=ErrorCode.FIELD_VALUE_REQUIRED.value,
        )


def is_retries_less_than_zero(config: dict) -> None:
    if "retries" in config and config["retries"] < 0:
        raise InvalidFieldValueError(
            field_name="retries",
            reason="Retries must be zero or greater.",
            field_value=config["retries"],
        )
