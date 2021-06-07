"""Test the normalize address method of the ShipEngine SDK."""
from shipengine_sdk.models import Address

from ..util.test_data import (
    normalize_an_address,
    us_valid_normalize_assertions,
    valid_residential_address,
)


class TestNormalizeAddress:
    def test_normalize_valid_residential_address(self) -> None:
        """DX-1041 - Normalize valid residential address."""
        residential_address = valid_residential_address()
        normalized = normalize_an_address(residential_address)

        us_valid_normalize_assertions(
            original_address=residential_address,
            normalized_address=normalized,
            expected_residential_indicator=True,
        )
        assert type(normalized) is Address
