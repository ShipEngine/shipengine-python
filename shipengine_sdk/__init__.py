"""ShipEngine SDK."""

__version__ = "0.0.1"

import logging
from logging import NullHandler

# SDK imports here

logging.getLogger(__name__).addHandler(NullHandler())
