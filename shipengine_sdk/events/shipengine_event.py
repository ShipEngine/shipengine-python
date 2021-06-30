"""
ShipEngine event emission via Observer Pattern. The ShipEngine SDK emits when an
HTTP request is sent and when an HTTP response is received for said request.
"""
import json
from datetime import datetime
from typing import Any, Dict

from .. import ShipEngineConfig
from ..errors import ShipEngineError
from ..models.enums import Events
from . import Publisher, RequestSentEvent, ResponseReceivedEvent


class ShipEngineEvent:
    timestamp: str

    def __init__(self, event_type: str, message: str) -> None:
        self.timestamp = datetime.now().isoformat()
        self.type = event_type
        self.message = message

    @staticmethod
    def emit_event(emitted_event_type: str, event_data: Dict[str, Any], config: ShipEngineConfig):
        publisher = Publisher([Events.ON_REQUEST_SENT.value, Events.ON_RESPONSE_RECEIVED.value])
        publisher.register(event=Events.ON_REQUEST_SENT.value, subscriber=config.event_listener)
        publisher.register(
            event=Events.ON_RESPONSE_RECEIVED.value, subscriber=config.event_listener
        )

        if emitted_event_type == RequestSentEvent.REQUEST_SENT:
            request_sent_event = RequestSentEvent(
                message=event_data["message"],
                request_id=event_data["request_id"],
                url=event_data["base_uri"],
                headers=event_data["request_headers"],
                body=event_data["body"],
                retry=event_data["retry"],
                timeout=event_data["timeout"],
            )

            publisher.dispatch(event=request_sent_event, event_name=Events.ON_REQUEST_SENT.value)
            return request_sent_event
        elif emitted_event_type == ResponseReceivedEvent.RESPONSE_RECEIVED:
            response_received_event = ResponseReceivedEvent(
                message=event_data["message"],
                request_id=event_data["request_id"],
                url=event_data["base_uri"],
                status_code=event_data["status_code"],
                headers=event_data["request_headers"],
                body=event_data["body"],
                retry=event_data["retry"],
                elapsed=event_data["elapsed"],
            )

            publisher.dispatch(
                event=response_received_event, event_name=Events.ON_RESPONSE_RECEIVED.value
            )
            return response_received_event
        else:
            raise ShipEngineError(
                f"Event type [{emitted_event_type}] is not a valid type of event."
            )

    def to_dict(self):
        return (lambda o: o.__dict__)(self)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)
