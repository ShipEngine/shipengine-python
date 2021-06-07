"""Test the normalize address method of the ShipEngine SDK."""
from shipengine_sdk.models import Address

from ..util.test_data import (
    normalize_an_address,
    valid_address_assertions,
    valid_commercial_address,
    valid_residential_address,
)


class TestNormalizeAddress:
    TEST_METHOD: str = "normalize"

    def test_normalize_valid_residential_address(self) -> None:
        """DX-1041 - Normalize valid residential address."""
        residential_address = valid_residential_address()
        normalized = normalize_an_address(residential_address)

        valid_address_assertions(
            test_method=self.TEST_METHOD,
            locale="domestic",
            original_address=residential_address,
            returned_address=normalized,
            expected_residential_indicator=True,
        )
        assert type(normalized) is Address

    def test_normalize_valid_commercial_address(self) -> None:
        """DX-1042 - Normalize valid commercial address."""
        commercial_address = valid_commercial_address()
        normalized = normalize_an_address(commercial_address)

        valid_address_assertions(
            test_method=self.TEST_METHOD,
            locale="domestic",
            original_address=commercial_address,
            returned_address=normalized,
            expected_residential_indicator=False,
        )
