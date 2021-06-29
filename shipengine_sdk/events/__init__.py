"""
ShipEngine event emission via Observer Pattern. The ShipEngine SDK emits when an
HTTP request is sent and when an HTTP response is received for said request.
"""
from .shipengine_event import ShipEngineEvent


class Publisher(ShipEngineEvent):
    pass


class Subscriber(ShipEngineEvent):
    pass
