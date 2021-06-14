"""CarrierAccount class object and immutable carrier object."""
import json
from typing import Any, Dict

from ...errors import InvalidFieldValueError, ShipEngineError
from ..enums import Carriers, does_member_value_exist, get_carrier_name_value


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

    def __init__(self, account_information: Dict[str, Any]) -> None:
        """This class represents a given account with a Carrier provider e.g. `FedEx`, `UPS`, `USPS`."""
        self._set_carrier(account_information["carrierCode"])
        self.account_id = account_information["accountID"]
        self.account_number = account_information["accountNumber"]

    def _set_carrier(self, carrier: str) -> None:
        if does_member_value_exist(carrier, Carriers):
            self.carrier = Carrier(code=carrier).to_dict()
            self.name = self.carrier["name"]
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
