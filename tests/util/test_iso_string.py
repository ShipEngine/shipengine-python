"""Testing the IsoString class object."""
import datetime

from shipengine_sdk.util.iso_string import IsoString


class TestIsoString:
    _test_iso_string_no_tz: str = "2021-06-10T21:00:00.000"

    def test_to_string(self) -> None:
        iso_str = IsoString(self._test_iso_string_no_tz).to_string()

        assert type(iso_str) is str

    def test_to_datetime_object(self) -> None:
        iso_str = IsoString(self._test_iso_string_no_tz).to_datetime_object()

        assert type(iso_str) is datetime.datetime

    def test_static_valid_iso_check(self) -> None:
        assert IsoString.is_valid_iso_string(self._test_iso_string_no_tz) is True

    def test_static_valid_iso_check_failure(self) -> None:
        assert IsoString.is_valid_iso_string("2021-06-10T21:00:00.000K") is False
