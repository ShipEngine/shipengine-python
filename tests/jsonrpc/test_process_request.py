"""Testing the process request and response functions."""
import pytest

from shipengine_sdk.errors import (
    AccountStatusError,
    BusinessRuleError,
    ClientSecurityError,
    ClientSystemError,
    ShipEngineError,
    ValidationError,
)
from shipengine_sdk.jsonrpc import handle_response, wrap_request
from shipengine_sdk.models import ErrorCode, ErrorSource, ErrorType, RPCMethods


def handle_response_errors(error_source: str, error_code: str, error_type: str):
    return handle_response(
        {
            "jsonrpc": "2.0",
            "id": "req_0938jf40398j4f09s8hfd",
            "error": {
                "code": 12345,
                "message": "Test message from the test suite.",
                "data": {"source": error_source, "type": error_type, "code": error_code},
            },
        }
    )


class TestProcessRequest:
    """Test the handle request and response functionality."""

    def test_wrap_request_with_no_params(self) -> None:
        """Unit test for the `wrap_request` method used by the client."""
        request_body = wrap_request(method=RPCMethods.ADDRESS_VALIDATE.value, params=None)
        assert "params" not in request_body

    def test_account_status_handling(self) -> None:
        """Unit test for the `handle_response` method account status error case."""
        with pytest.raises(AccountStatusError):
            handle_response_errors(
                error_source=ErrorSource.SHIPENGINE.value,
                error_type=ErrorType.ACCOUNT_STATUS.value,
                error_code=ErrorCode.TERMS_NOT_ACCEPTED.value,
            )

    def test_security_error_case(self) -> None:
        """Unit test for the `handle_response` method security error case."""
        with pytest.raises(ClientSecurityError):
            handle_response_errors(
                error_source=ErrorSource.SHIPENGINE.value,
                error_type=ErrorType.SECURITY.value,
                error_code=ErrorCode.UNAUTHORIZED.value,
            )

    def test_validation_error_case(self) -> None:
        """Unit test for the `handle_response` method validation error case."""
        with pytest.raises(ValidationError):
            handle_response_errors(
                error_source=ErrorSource.SHIPENGINE.value,
                error_type=ErrorType.VALIDATION.value,
                error_code=ErrorCode.INVALID_FIELD_VALUE.value,
            )

    def test_business_rule_error_case(self) -> None:
        """Unit test for the `handle_response` method business rule error case."""
        with pytest.raises(BusinessRuleError):
            handle_response_errors(
                error_source=ErrorSource.SHIPENGINE.value,
                error_type=ErrorType.BUSINESS_RULES.value,
                error_code=ErrorCode.TRACKING_NOT_SUPPORTED.value,
            )

    def test_system_error_case(self) -> None:
        """Unit test for the `handle_response` method system error case."""
        with pytest.raises(ClientSystemError):
            handle_response_errors(
                error_source=ErrorSource.SHIPENGINE.value,
                error_type=ErrorType.SYSTEM.value,
                error_code=ErrorCode.UNSPECIFIED.value,
            )

    def test_shipengine_error_case(self) -> None:
        """Unit test for the `handle_response` method shipengine error case."""
        with pytest.raises(ShipEngineError):
            handle_response_errors(
                error_source=ErrorSource.SHIPENGINE.value,
                error_type=ErrorType.AUTHORIZATION.value,
                error_code=ErrorCode.TERMS_NOT_ACCEPTED.value,
            )
