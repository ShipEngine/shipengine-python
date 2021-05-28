"""Initial Docstring"""

from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import LetterCase, dataclass_json


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
