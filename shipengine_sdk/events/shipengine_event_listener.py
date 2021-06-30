"""A default event listener to consume the events emitted by the SDK."""
from typing import Union

from ..events import RequestSentEvent, Subscriber
from .response_received_event import ResponseReceivedEvent


class ShipEngineEventListener(Subscriber):
    def __init__(self, name=None) -> None:
        super().__init__(name=name)

    # You can add your own event consumption logic by adding/overriding the parent `update()` method below.
    @staticmethod
    def update(event: Union[RequestSentEvent, ResponseReceivedEvent]):
        print(event.to_dict())
