"""This event gets emitted everytime the **ShipEngineClient** sends a request to ShipEngine API."""
from typing import Any, Dict, List

from . import ShipEngineEvent


class RequestSentEvent(ShipEngineEvent):
    REQUEST_SENT = "request_sent"

    def __init__(
        self,
        request_id: str,
        message: str,
        url: str,
        headers: List[str],
        body: Dict[str, Any],
        retry: int,
        timeout: int,
    ) -> None:
        super().__init__(event_type=self.REQUEST_SENT, message=message)
        self.request_id = request_id
        self.url = url
        self.headers = headers
        self.body = body
        self.retry = retry
        self.timeout = timeout
