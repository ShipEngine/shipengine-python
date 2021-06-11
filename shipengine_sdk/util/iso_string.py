"""Initial Docstring"""
import re
from datetime import datetime


class IsoString:
    def __init__(self, iso_string: str) -> None:
        """
        A string representing a Date, DateTime, or DateTime with Timezone. The object
        also has a method to return a `datetime.datetime` object, which is the native
        datetime object in python as of 3.7.

        This class object takes in an **ISO-8601** string. Learn more here: https://en.wikipedia.org/wiki/ISO_8601

        :param str iso_string: An `ISO-8601` string. Learn more here: https://en.wikipedia.org/wiki/ISO_8601
        """
        self.iso_string = iso_string

    def to_datetime_object(self) -> datetime:
        return datetime.strptime(self.iso_string, "%Y-%m-%dT%H:%M:%S.%fZ")

    def has_timezone(self) -> bool:
        if self.is_valid_iso_string(self.iso_string):
            return False if self.is_valid_iso_string_no_tz(self.iso_string) else True

    @staticmethod
    def is_valid_iso_string_no_tz(iso_str: str):
        pattern = re.compile(
            r"^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?([+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$"  # noqa
        )
        if pattern.match(iso_str):
            return True
        else:
            return False

    @staticmethod
    def is_valid_iso_string(iso_str: str):
        pattern = re.compile(
            r"^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$"  # noqa
        )
        if pattern.match(iso_str):
            return True
        else:
            return False
