"""Enumeration of valid carrier names."""
from enum import Enum


class CarrierNames(Enum):
    """An enumeration valid carrier names."""

    FEDEX = "FedEx"
    """FedEx - Federal Express"""

    UPS = "United Parcel Service"
    """UPS - United Parcel Service"""

    USPS = "U.S. Postal Service"
    """USPS - United State Postal Service"""

    STAMPS_COM = "Stamps.com"
    """USPS services via Stamps.com"""

    DHL_EXPRESS = "DHL Express"
    """DHL Express"""

    DHL_GLOBAL_MAIL = "DHL ECommerce"
    """DHL ECommerce"""

    CANADA_POST = "Canada Post"
    """Canada Post"""

    AUSTRALIA_POST = "Australia Post"
    """Australia Post"""

    FIRSTMILE = "First Mile"
    """First Mile"""

    ASENDIA = "Asendia"
    """Asendia"""

    ONTRAC = "OnTrac"
    """OnTrac"""

    APC = "APC"
    """APC"""

    NEWGISTICS = "Newgistics"
    """Newgistics"""

    GLOBEGISTICS = "Globegistics"
    """Globegistics"""

    RR_DONNELLEY = "RR Donnelley"
    """RR Donnell"""

    IMEX = "IMEX"
    """IMEX"""

    ACCESS_WORLDWIDE = "Access Worldwide"
    """Access Worldwide"""

    PUROLATOR_CA = "Purolator Canada"
    """Purolator Canada"""

    SENDLE = "Sendle"
    """Sendle"""
