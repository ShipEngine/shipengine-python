"""Enumeration of valid carrier providers."""
from enum import Enum


class Carriers(Enum):
    """An enumeration of valid carrier providers."""

    FEDEX = "fedex"
    """FedEx - Federal Express"""

    UPS = "ups"
    """UPS - United Parcel Service"""

    USPS = "usps"
    """USPS - United State Postal Service"""

    STAMPS_COM = "stamps_com"
    """USPS services via Stamps.com"""

    DHL_EXPRESS = "dhl_express"
    """DHL Express"""

    DHL_GLOBAL_MAIL = "dhl_global_mail"
    """DHL ECommerce"""

    CANADA_POST = "canada_post"
    """Canada Post"""

    AUSTRALIA_POST = "australia_post"
    """Australia Post"""

    FIRSTMILE = "firstmile"
    """First Mile"""

    ASENDIA = "asendia"
    """Asendia"""

    ONTRAC = "ontrac"
    """OnTrac"""

    APC = "apc"
    """APC"""

    NEWGISTICS = "newgistics"
    """Newgistics"""

    GLOBEGISTICS = "globegistics"
    """Globegistics"""

    RR_DONNELLEY = "rr_donnelley"
    """RR Donnell"""

    IMEX = "imex"
    """IMEX"""

    ACCESS_WORLDWIDE = "access_worldwide"
    """Access Worldwide"""

    PUROLATOR_CA = "purolator_ca"
    """Purolator Canada"""

    SENDLE = "sendle"
    """Sendle"""
