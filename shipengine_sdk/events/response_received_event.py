"""Initial Docstring"""
from typing import Any, Dict, List

from . import ShipEngineEvent


class ResponseReceivedEvent(ShipEngineEvent):
    RESPONSE_RECEIVED = "response_received"

    def __init__(
        self,
        message: str,
        request_id: str,
        url: str,
        status_code: int,
        headers: List[str],
        body: Dict[str, Any],
        retry: int,
        elapsed: str,
    ) -> None:
        super().__init__(event_type=self.RESPONSE_RECEIVED, message=message)
        self.request_id = request_id
        self.url = url
        self.status_code = status_code
        self.headers = headers
        self.body = body
        self.retry = retry
        self.elapsed = elapsed
