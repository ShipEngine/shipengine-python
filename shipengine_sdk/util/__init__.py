"""Testing a string manipulation helper function."""

from shipengine_sdk.util.sdk_assertions import (
    api_key_validation_error_assertions,
    is_api_key_valid,
    is_retries_valid,
)


def snake_to_camel(snake_case_string: str) -> str:
    """
    Takes in a `snake_case` string and returns a `camelCase` string.

    :params str snake_case_string: The snake_case string to be converted
    into camelCase.
    :returns: camelCase string
    :rtype: str
    """
    initial, *temp = snake_case_string.split("_")
    return "".join([initial.lower(), *map(str.title, temp)])
