"""Initial Docstring"""

from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import LetterCase, dataclass_json

from shipengine_sdk.util.sdk_assertions import is_postal_code_valid, is_street_valid


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Address:
    street: List[str]
    city_locality: str
    state_province: str
    postal_code: str
    country_code: str
    is_residential: bool = False
    name: str = ""
    phone: str = ""
    company: str = ""

    def __post_init__(self):
        is_street_valid(self.street)
        is_postal_code_valid(self.postal_code)


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class AddressValidateResult:
    is_valid: Optional[bool]
    request_id: str
    normalized_address: Optional[Address]
    messages: List
    # info: List
    # warnings: List
    # errors: List
