"""Models to be used throughout the ShipEngine SDK."""
import json
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import LetterCase, dataclass_json

from ...util import (
    is_city_valid,
    is_country_code_valid,
    is_postal_code_valid,
    is_state_valid,
    is_street_valid,
)


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Address:
    street: List[str]
    city_locality: str
    state_province: str
    postal_code: str
    country_code: str
    is_residential: Optional[bool] = None
    name: str = ""
    phone: str = ""
    company: str = ""

    def __post_init__(self) -> None:
        is_street_valid(self.street)
        is_city_valid(self.city_locality)
        is_state_valid(self.state_province)
        is_postal_code_valid(self.postal_code)
        is_country_code_valid(self.country_code)


class AddressValidateResult:
    is_valid: Optional[bool]
    request_id: str
    normalized_address: Optional[Address]
    info: Optional[List]
    warnings: Optional[List]
    errors: Optional[List]

    def __init__(
        self,
        is_valid: Optional[bool],
        request_id: str,
        normalized_address: Optional[Address],
        messages: List,
        info: Optional[List] = None,
        warnings: Optional[List] = None,
        errors: Optional[List] = None,
    ) -> None:
        self.is_valid = is_valid
        self.request_id = request_id
        self.normalized_address = normalized_address
        self.info = list() if info is None else info
        self.warnings = list() if warnings is None else warnings
        self.errors = list() if errors is None else errors
        self.__extract_messages(messages)

    def __extract_messages(self, messages):
        for message in messages:
            if message["type"] == "error":
                del message["type"]
                self.errors.append(message)
            elif message["type"] == "info":
                del message["type"]
                self.info.append(message)
            elif message["type"] == "warning":
                del message["type"]
                self.warnings.append(message)

    def to_dict(self):
        return (lambda o: o.__dict__)(self)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)
