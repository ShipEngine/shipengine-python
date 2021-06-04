"""ShipEngine SDK."""
__version__ = "0.0.1"

import logging
from logging import NullHandler

# SDK imports here
from .shipengine import ShipEngine
from .shipengine_config import ShipEngineConfig

logging.getLogger(__name__).addHandler(NullHandler())
