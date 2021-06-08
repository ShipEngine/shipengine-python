"""Test the normalize address method of the ShipEngine SDK."""
import re

from ..util.test_data import (
    multi_line_address,
    normalize_an_address,
    unknown_address,
    valid_address_assertions,
    valid_canadian_address,
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

    def test_normalize_unknown_address(self) -> None:
        """DX-1043 - Normalize unknown address."""
        address = unknown_address()
        normalized = normalize_an_address(address)

        valid_address_assertions(
            test_method=self.TEST_METHOD,
            locale="international",
            original_address=address,
            returned_address=normalized,
            expected_residential_indicator=None,
        )

    def test_normalize_multi_line_address(self):
        """DX-1044 - Normalize multi-line address."""
        multi_line = multi_line_address()
        normalized = normalize_an_address(multi_line)

        valid_address_assertions(
            test_method=self.TEST_METHOD,
            locale="domestic",
            original_address=multi_line,
            returned_address=normalized,
            expected_residential_indicator=False,
        )
        assert (
            normalized.street[0]
            == (multi_line.street[0] + " " + multi_line.street[1]).replace(".", "").upper()
        )
        assert normalized.street[1] == multi_line.street[2].upper()

    def test_normalize_numeric_postal_code(self) -> None:
        """DX-1045 - Normalize address with numeric postal code."""
        address = valid_residential_address()
        normalized = normalize_an_address(address)

        valid_address_assertions(
            test_method=self.TEST_METHOD,
            locale="domestic",
            original_address=address,
            returned_address=normalized,
            expected_residential_indicator=True,
        )
        assert re.match(r"\d", normalized.postal_code)

    def test_normalize_alpha_postal_code(self) -> None:
        """DX-1046 - Normalize address with alpha-numeric postal code."""
        address = valid_canadian_address()
        normalized = normalize_an_address(address)

        valid_address_assertions(
            test_method=self.TEST_METHOD,
            locale="international",
            original_address=address,
            returned_address=normalized,
            expected_residential_indicator=False,
        )
