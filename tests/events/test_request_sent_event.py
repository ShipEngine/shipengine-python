"""Test that `RequestSentEvents` are emitted from the SDK properly."""
from pytest_mock import MockerFixture

# from shipengine_sdk.events import ShipEngineEventListener

# from ..util import stub_shipengine_config


class TestRequestSentEvent:
    def test_config_with_retries_disabled(self, mocker: MockerFixture) -> None:
        """Tests that the SDK does not automatically retry if retries in config is set to 0."""
        # spy = mocker.spy(ShipEngineEventListener, "update")
        # shipengine = stub_shipengine_config()
