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

    def has_time(self) -> bool:
        pattern = re.compile(r"[0-9]*T[0-9]*")
        return True if pattern.match(self.iso_string) is not None else False

    def has_timezone(self) -> bool:
        pattern = re.compile(r"(?<=T).*[+-][0-9]|Z$")
        if self.has_time() is True:
            return True if pattern.match(self.iso_string) is not None else False
