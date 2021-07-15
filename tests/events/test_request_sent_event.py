"""Test that `RequestSentEvents` are emitted from the SDK properly."""
from pytest_mock import MockerFixture

from shipengine_sdk.errors import RateLimitExceededError, ShipEngineError
from shipengine_sdk.events import (
    RequestSentEvent,
    ResponseReceivedEvent,
    ShipEngineEventListener,
)
from shipengine_sdk.models import Endpoints

from ..util import assert_on_429_exception, configurable_stub_shipengine_instance


class TestRequestSentEvent:
    def test_config_with_retries_disabled(self, mocker: MockerFixture) -> None:
        """DX-1527 - Tests that the SDK does not automatically retry if retries in config is set to 0."""
        request_sent_spy = mocker.spy(ShipEngineEventListener, "catch_request_sent_event")
        response_received_spy = mocker.spy(ShipEngineEventListener, "catch_response_received_event")
        shipengine = configurable_stub_shipengine_instance(
            {
                "api_key": "baz_sim",
                "base_uri": Endpoints.TEST_RPC_URL.value,
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
