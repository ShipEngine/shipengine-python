"""CarrierAccount class object and immutable carrier object."""
import json
from typing import Dict

from ...errors import InvalidFieldValueError, ShipEngineError
from ..enums import Carriers, does_member_value_exist, get_carrier_name_value

# @dataclass_json(letter_case=LetterCase.CAMEL)
# @dataclass(frozen=True)
# class Carrier:
#     """This immutable class object represents a given Carrier provider e.g. `FedEx`, `UPS`, `USPS`."""
#     name: str
#     code: str
#
#     def __post_init__(self) -> None:
#         """An immutable Carrier object. e.g. `FedEx`, `UPS`, `USPS`."""
#         if not does_member_value_exist(self.name, CarrierNames):
#             raise ShipEngineError(f"Carrier [{self.name}] not currently supported.")
#
#         if not does_member_value_exist(self.code, Carriers):
#             raise ShipEngineError(f"Carrier [{self.code}] not currently supported.")
#
#
# @dataclass_json(letter_case=LetterCase.CAMEL)
# @dataclass(frozen=True)
# class CarrierAccount:
#     """This class represents a given account with a Carrier provider e.g. `FedEx`, `UPS`, `USPS`."""
#     carrier: Union[str, Carrier]
#     account_id: str
#     account_number: str
#     name: str
#
#     def __post_init__(self) -> None:
#         if not does_member_value_exist()


class Carrier:
    def __init__(self, code: str) -> None:
        """This class represents a given account with a Carrier provider e.g. `FedEx`, `UPS`, `USPS`."""
        if not does_member_value_exist(code, Carriers):
            raise ShipEngineError(f"Carrier [{code}] not currently supported.")
        else:
            self.name = get_carrier_name_value(code.upper())
            self.code = code

    def to_dict(self):
        return (lambda o: o.__dict__)(self)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)


class CarrierAccount:
    carrier: Carrier

    def __init__(self, account_information: Dict[str, any]) -> None:
        """This class represents a given account with a Carrier provider e.g. `FedEx`, `UPS`, `USPS`."""
        self._set_carrier(account_information["carrierCode"])
        self.account_id = account_information["accountID"]
        self.account_number = account_information["accountNumber"]

    def _set_carrier(self, carrier: str) -> None:
        if does_member_value_exist(carrier, Carriers):
            self.carrier = Carrier(code=carrier)
            self.name = self.carrier.name
        else:
            InvalidFieldValueError(
                field_name="carrier",
                reason=f"Carrier [{carrier}] is currently not supported.",
                field_value=carrier,
            )

    def to_dict(self):
        return (lambda o: o.__dict__)(self)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)
