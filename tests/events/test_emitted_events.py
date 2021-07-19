"""Test that `RequestSentEvents` are emitted from the SDK properly."""
from datetime import datetime

from pytest_mock import MockerFixture

from shipengine_sdk import __version__
from shipengine_sdk.errors import (
    ClientTimeoutError,
    RateLimitExceededError,
    ShipEngineError,
)
from shipengine_sdk.events import (
    RequestSentEvent,
    ResponseReceivedEvent,
    ShipEngineEventListener,
)
from shipengine_sdk.models import ErrorCode, ErrorSource, ErrorType
from shipengine_sdk.models.enums import Constants

from ..util import (
    assert_on_429_exception,
    configurable_stub_shipengine_instance,
    valid_residential_address,
)


class TestEmittedEvents:
    def test_user_agent_includes_correct_sdk_version(self, mocker: MockerFixture) -> None:
        """DX-1517 - Test user agent includes correct SDK version."""
        request_sent_spy = mocker.spy(ShipEngineEventListener, "catch_request_sent_event")
        config = {
            "api_key": Constants.STUB_API_KEY.value,
            "retries": 1,
            "timeout": 10,
        }
        shipengine = configurable_stub_shipengine_instance(config=config)
        shipengine.validate_address(address=valid_residential_address())
        request_sent_return = request_sent_spy.spy_return
        assert request_sent_return.headers["User-Agent"].split(" ")[0].split("/")[1] == __version__

    def test_request_sent_event_on_retries(self, mocker: MockerFixture) -> None:
        """DX-1521 - Test that a RequestSentEvent is emitted on retries."""
        request_sent_spy = mocker.spy(ShipEngineEventListener, "catch_request_sent_event")
        config = {
            "api_key": Constants.STUB_API_KEY.value,
            "retries": 1,
            "timeout": 10,
        }
        shipengine = configurable_stub_shipengine_instance(config=config)
        try:
            shipengine.get_carrier_accounts(carrier_code="amazon_buy_shipping")
        except ShipEngineError as err:
            assert_on_429_exception(err=err, error_class=RateLimitExceededError)

            request_sent_return = request_sent_spy.spy_return
            assert request_sent_spy.call_count == 2
            assert type(request_sent_return) == RequestSentEvent
            assert request_sent_return.retry == 1
            assert type(request_sent_return.timestamp) == datetime
            assert request_sent_return.timeout == config["timeout"]
            assert request_sent_return.body["method"] == "carrier.listAccounts.v1"
            assert request_sent_return.base_uri == "https://api.shipengine.com/jsonrpc"
            assert request_sent_return.headers["Api-Key"] == Constants.STUB_API_KEY.value
            assert request_sent_return.headers["Content-Type"] == "application/json"
            assert (
                request_sent_return.message == "Retrying the ShipEngine carrier.listAccounts.v1 API"
                " at https://api.shipengine.com/jsonrpc"
            )

    def test_response_received_event_success(self, mocker: MockerFixture) -> None:
        """DX-1522 Test response received event success."""
        test_start_time = datetime.now()
        response_received_spy = mocker.spy(ShipEngineEventListener, "catch_response_received_event")
        config = {
            "api_key": Constants.STUB_API_KEY.value,
            "retries": 2,
            "timeout": 10,
        }
        shipengine = configurable_stub_shipengine_instance(config=config)
        shipengine.validate_address(address=valid_residential_address())

        response_recd_return = response_received_spy.spy_return
        assert response_received_spy.call_count == 1
        assert type(response_recd_return) == ResponseReceivedEvent
        assert (
            response_recd_return.message
            == "Received an HTTP 200 response from the ShipEngine address.validate.v1 API"
        )
        assert response_recd_return.status_code == 200
        assert response_recd_return.base_uri == "https://api.shipengine.com/jsonrpc"
        assert response_recd_return.body["method"] == "address.validate.v1"
        assert response_recd_return.retry == 0
        assert response_recd_return.elapsed < test_start_time.second
        assert response_recd_return.headers["Content-Type"].split(";")[0] == "application/json"

    def test_response_received_on_error(self, mocker: MockerFixture) -> None:
        """DX-1523 - Test response received event on error."""
        test_start_time = datetime.now()
        response_received_spy = mocker.spy(ShipEngineEventListener, "catch_response_received_event")
        config = {
            "api_key": Constants.STUB_API_KEY.value,
            "retries": 1,
            "timeout": 10,
        }
        shipengine = configurable_stub_shipengine_instance(config=config)
        try:
            shipengine.get_carrier_accounts(carrier_code="amazon_buy_shipping")
        except ShipEngineError as err:
            assert_on_429_exception(err=err, error_class=RateLimitExceededError)
            response_recd_return = response_received_spy.spy_return
            assert type(response_recd_return) == ResponseReceivedEvent
            assert (
                response_recd_return.message
                == "Retrying the ShipEngine carrier.listAccounts.v1 API at https://api.shipengine.com/jsonrpc"
            )
            assert response_recd_return.status_code == 429
            assert response_recd_return.base_uri == "https://api.shipengine.com/jsonrpc"
            assert response_recd_return.body["method"] == "carrier.listAccounts.v1"
            assert response_recd_return.retry == 1
            assert response_recd_return.elapsed < test_start_time.second
            assert (response_recd_return.timestamp - test_start_time).total_seconds() > 1

    def test_config_with_retries_disabled(self, mocker: MockerFixture) -> None:
        """DX-1527 - Tests that the SDK does not automatically retry if retries in config is set to 0."""
        request_sent_spy = mocker.spy(ShipEngineEventListener, "catch_request_sent_event")
        response_received_spy = mocker.spy(ShipEngineEventListener, "catch_response_received_event")
        shipengine = configurable_stub_shipengine_instance(
            {
                "api_key": Constants.STUB_API_KEY.value,
                "retries": 0,
                "timeout": 10,
            }
        )
        try:
            shipengine.get_carrier_accounts(carrier_code="amazon_buy_shipping")
        except ShipEngineError as err:
            assert_on_429_exception(err=err, error_class=RateLimitExceededError)
            request_sent_return = request_sent_spy.spy_return
            assert request_sent_spy.call_count == 1
            assert type(request_sent_return) == RequestSentEvent
            assert request_sent_return.retry == 0

            response_recd_return = response_received_spy.spy_return
            assert request_sent_spy.call_count == 1
            assert type(response_recd_return) == ResponseReceivedEvent
            assert response_recd_return.retry == 0

    def test_config_with_custom_retries(self, mocker: MockerFixture) -> None:
        """DX-1528 - Test config with custom retries."""
        request_sent_spy = mocker.spy(ShipEngineEventListener, "catch_request_sent_event")
        response_received_spy = mocker.spy(ShipEngineEventListener, "catch_response_received_event")
        shipengine = configurable_stub_shipengine_instance(
            {
                "api_key": Constants.STUB_API_KEY.value,
                "retries": 3,
                "timeout": 21,
            }
        )
        try:
            shipengine.get_carrier_accounts(carrier_code="amazon_buy_shipping")
        except ShipEngineError as err:
            assert_on_429_exception(err=err, error_class=RateLimitExceededError)
            request_sent_return = request_sent_spy.spy_return
            assert request_sent_spy.call_count == 4
            assert type(request_sent_return) == RequestSentEvent
            assert request_sent_return.retry == 3

            response_recd_return = response_received_spy.spy_return
            assert request_sent_spy.call_count == 4
            assert type(response_recd_return) == ResponseReceivedEvent
            assert response_recd_return.retry == 3

    def test_timeout_err_when_retry_greater_than_timeout(self, mocker: MockerFixture) -> None:
        """DX-1529 - Test timeout error when retry_after is greater than timeout."""
        request_sent_spy = mocker.spy(ShipEngineEventListener, "catch_request_sent_event")
        response_received_spy = mocker.spy(ShipEngineEventListener, "catch_response_received_event")
        config = {
            "api_key": Constants.STUB_API_KEY.value,
            "retries": 3,
            "timeout": 1,
        }
        shipengine = configurable_stub_shipengine_instance(config=config)
        try:
            shipengine.get_carrier_accounts(carrier_code="amazon_buy_shipping")
        except ShipEngineError as err:
            assert type(err) == ClientTimeoutError
            assert err.request_id is not None
            assert err.request_id.startswith("req_")
            assert (
                err.message
                == f"The request took longer than the {config['timeout']} seconds allowed."
            )
            assert err.source is ErrorSource.SHIPENGINE.value
            assert err.error_type is ErrorType.SYSTEM.value
            assert err.error_code is ErrorCode.TIMEOUT.value
            assert err.url == "https://www.shipengine.com/docs/rate-limits"

            request_sent_return = request_sent_spy.spy_return
            assert request_sent_spy.call_count == 1
            assert type(request_sent_return) == RequestSentEvent
            assert request_sent_return.retry == 0
            assert request_sent_return.timeout == 1

            response_recd_return = response_received_spy.spy_return
            assert request_sent_spy.call_count == 1
            assert type(response_recd_return) == ResponseReceivedEvent
            assert response_recd_return.retry == 0

    def test_retry_waits_correct_amount_of_time(self, mocker: MockerFixture) -> None:
        """DX-1530 - retry waits the correct amount of time."""
        test_start_time = datetime.now()
        request_sent_spy = mocker.spy(ShipEngineEventListener, "catch_request_sent_event")
        response_received_spy = mocker.spy(ShipEngineEventListener, "catch_response_received_event")
        shipengine = configurable_stub_shipengine_instance(
            {
                "api_key": Constants.STUB_API_KEY.value,
                "retries": 2,
                "timeout": 10,
            }
        )
        try:
            shipengine.get_carrier_accounts(carrier_code="amazon_buy_shipping")
        except ShipEngineError as err:
            assert_on_429_exception(err=err, error_class=RateLimitExceededError)

            request_sent_return = request_sent_spy.spy_return
            assert request_sent_spy.call_count == 3
            assert type(request_sent_return) == RequestSentEvent
            assert request_sent_return.retry == 2
            assert request_sent_return.timeout == 10

            response_recd_return = response_received_spy.spy_return
            assert request_sent_spy.call_count == 3
            assert type(response_recd_return) == ResponseReceivedEvent
            assert response_recd_return.retry == 2
            assert (
                int(str(round((test_start_time - datetime.now()).total_seconds())).strip("-")) <= 6
            )
