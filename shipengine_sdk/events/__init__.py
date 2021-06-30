"""
ShipEngine event emission via Observer Pattern. The ShipEngine SDK emits when an
HTTP request is sent and when an HTTP response is received for said request.
"""
import json
from typing import Callable, List, Optional, Union

from .request_sent_event import RequestSentEvent
from .response_received_event import ResponseReceivedEvent
from .shipengine_event import ShipEngineEvent
from .shipengine_event_listener import ShipEngineEventListener


class Publisher:
    def __init__(self, events: List[str]) -> None:
        self.events = {event: dict() for event in events}

    def get_subscribers(self, event: Optional[str] = None):
        return self.events[event]

    def register(self, event, subscriber, callback: Optional[Callable] = None):
        if callback is None:
            callback = getattr(subscriber, "update")
        self.get_subscribers(event)[subscriber] = callback

    def unregister(self, event, subscriber):
        del self.get_subscribers(event)[subscriber]

    def dispatch(self, event, event_name: str = None):
        for subscriber, callback in self.get_subscribers(event_name).items():
            callback(event)


class Subscriber:
    def __init__(self, name=None) -> None:
        if name is not None:
            self.name = name
        else:
            self.name = "Event Subscriber"

    @staticmethod
    def update(event: Union[RequestSentEvent, ResponseReceivedEvent]):
        return event

    def to_dict(self):
        return (lambda o: o.__dict__)(self)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)
